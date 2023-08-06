import json


class Folder:
    def __init__(self, name="", id=-1):
        self.name = name
        self.id = id
        self.children = []

    def to_json(self):
        return json.dumps(self.__dict__)