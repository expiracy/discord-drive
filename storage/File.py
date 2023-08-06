import json


class File:
    def __init__(self, name, id, contents):
        self.name = name
        self.id = id
        self.content = contents

    def to_json(self):
        return json.dumps(self.__dict__)