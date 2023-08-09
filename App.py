import json
import os

import asyncio

import quart
from quart import Quart, render_template, request, jsonify, send_file

from database.DatabaseManager import DatabaseManager
from discord_bot.StorageBot import StorageBot
from storage.File import File

ROOT = os.path.dirname(__file__)

# Initialise applications
app = Quart(
    __name__,
    static_folder="resources/static/",
    template_folder="resources/templates/"
)
app.config['MAX_CONTENT_LENGTH'] = 1e9

bot = StorageBot()
database = DatabaseManager()


@app.before_serving
async def before_serving():
    loop = asyncio.get_event_loop()
    await bot.login()
    loop.create_task(bot.connect())


@app.route("/", methods=["GET"])
async def index(**kwargs):
    return await render_template("index.html", **kwargs), 200

'''
@app.route("/api/create_folder", methods=["GET"])
async def create_folder():
    folder_name = request.args.get('name')
    success = await bot.create_folder(1136677852796952586, folder_name)
    return success, 200
'''


@app.route("/<int:guild_id>/<int:directory_id>/<int:file_id>", methods=["GET"])
async def get_file(guild_id, directory_id, file_id):
    file_info = database.get_file_info(file_id)

    if not file_info:
        return "File does not exist", 400

    root = database.get_root(guild_id)

    if not root:
        return "Server has not been registered", 400

    channel_id, _ = root

    file_name, content_type = file_info

    file = File(file_name, content_type)

    message_ids = database.get_file_parts(file_id)

    for message_id in message_ids:
        attachment = (await bot.get_message(message_id, guild_id, channel_id)).attachments[0]

        data_file_path = f"{ROOT}\\temp\\{attachment.filename}"
        await attachment.save(data_file_path)

        with open(data_file_path, "rb") as data_file:
            file.add_part(data_file.read())

        os.remove(data_file_path)

    file.reassemble(f"{ROOT}\\temp")
    file_path = f"{ROOT}\\temp\\{file.name}"

    return await send_file(file_path), 200


@app.route("/<int:guild_id>/<int:directory_id>")
async def url_handler(guild_id, directory_id):

    #TODO
    return await index(guild_id=guild_id, directory_id=directory_id)


@app.route("/api/login")
async def login_user():
    username = request.args.get("username")
    password = request.args.get("password")

    guild_id = database.get_details(username, password)
    root = database.get_root(guild_id)

    if not guild_id:
        return "login", 400

    if not root:
        return "login", 400

    channel_id, folder_id = root

    return f"{guild_id[0]}/{folder_id}", 200


@app.route("/test")
async def test():
    return "TEST"


@app.route("/login")
async def login_page():
    return await render_template("login.html"), 200


@app.route("/api/upload_files/<int:guild_id>/<int:directory_id>", methods=["POST"])
async def upload_file(guild_id, directory_id):
    request_files = (await request.files).getlist('files')

    if len(request_files) == 0:
        return "No files selected.", 400

    for request_file in request_files:

        if request_file.filename == '':
            return "One or more selected files are empty.", 400

        if not request_file:
            continue

        file_path = f"{ROOT}\\temp\\{request_file.filename}"
        await request_file.save(file_path)

        with open(file_path, 'rb') as uploaded_file:
            file = File(request_file.filename, request_file.content_type)
            file.split(uploaded_file)

        message_ids = []
        for part_number, part in enumerate(file.parts):
            data_file_path = f"{ROOT}\\temp\\{request_file.filename}_{part_number}.dat"

            with open(data_file_path, 'wb') as data_file:
                data_file.write(part)

            message_id = await bot.upload_file(data_file_path, guild_id)
            message_ids.append(message_id)

            os.remove(data_file_path)

        os.remove(file_path)

        database.insert_file(file, message_ids, directory_id)

    return "File(s) uploaded successfully", 200


if __name__ == '__main__':
    app.run(port=5000)
