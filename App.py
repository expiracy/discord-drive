import json
import os

import discord
import asyncio
from quart import Quart, render_template, request, jsonify

from discord_bot.StorageBot import StorageBot
from storage.File import File

app = Quart(
    __name__,
    static_folder="resources/static/",
    template_folder="resources/templates/"
)

bot = StorageBot()


@app.before_serving
async def before_serving():
    loop = asyncio.get_event_loop()
    await bot.login()
    loop.create_task(bot.connect())


@app.route("/", methods=["GET"])
async def index():
    return await render_template("index.html")


@app.route("/api/create_folder", methods=["GET"])
async def create_folder():
    folder_name = request.args.get('name')
    success = await bot.create_folder(1136677852796952586, folder_name)
    return success, 200


@app.route("/api/upload_files", methods=["POST"])
async def upload_file():

    files = (await request.files).getlist('files[]')

    if len(files) == 0:
        return jsonify(error="No files selected."), 400

    for file in files:

        if file.filename == '':
            return jsonify(error="One or more selected files are empty."), 400

        if file:
            file_path = f"{os.path.dirname(__file__)}\\uploads\\{file.filename}"

            await file.save(file_path)
            message_id = await bot.upload_file(file_path, 1136677852796952586)
            os.remove(file_path)

    return jsonify(success=f"File(s) uploaded successfully"), 200


if __name__ == '__main__':
    app.run()
