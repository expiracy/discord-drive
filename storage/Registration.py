from quart import jsonify


class Registration:
    def __init__(self, username, password, guild_id, channel_id):
        self.username = username
        self.password = password
        self.guild_id = guild_id
        self.channel_id = channel_id


    def to_json(self):
        return jsonify(
            username=self.username,
            password=self.password,
            guild_id=self.guild_id,
            channel_id=self.channel_id
        )
