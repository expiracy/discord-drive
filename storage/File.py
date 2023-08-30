import json
import os
import sys
from io import BytesIO

import requests
from requests import Response


class File:
    def __init__(self, name, content_type):
        self.name = name
        self.parts = []
        self.content_type = content_type

    def add_part(self, part):
        self.parts.append(part)

    def split(self, file, chunk_size=int(8e6)):
        def read_chunk():
            return file.read(chunk_size)

        for chunk in iter(read_chunk, bytearray()):
            self.parts.append(chunk)

    def reassemble(self):
        file_path = f"{sys.path[1]}\\{self.name}"

        with open(file_path, "wb") as reassembled_file:
            for part in self.parts:
                reassembled_file.write(part)

        with open(file_path, "rb") as reassembled_file:
            contents = reassembled_file.read()

        os.remove(file_path)
        return BytesIO(contents)
