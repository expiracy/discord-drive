import sqlite3

from storage import File


class DatabaseManager:
    def __init__(self):
        self.connection = sqlite3.connect('discord_storage.db')
        self.create_tables()

    def create_tables(self):
        cursor = self.connection.cursor()

        # Create Servers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Servers (
                guild_id INTEGER PRIMARY KEY,
                channel_id INTEGER
            )
        ''')

        # Create Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                username VARCHAR(32),
                password VARCHAR(100),
                guild_id INTEGER,
                FOREIGN KEY (guild_id) REFERENCES Servers(guild_id)
            )
        ''')

        # Create Files table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Files (
                file_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                file_name VARCHAR(100),
                content_type VARCHAR(10),
                directory_id INTEGER,
                FOREIGN KEY (directory_id) REFERENCES Directory(directory_id)
            )
        ''')

        # Create Directory table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Directory (
                directory_id INTEGER PRIMARY KEY,
                directory_name VARCHAR(100),
                parent_id INTEGER,
                FOREIGN KEY (parent_id) REFERENCES Directory(directory_id)
            )
        ''')

        # Create DirectoryChildren table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS DirectoryChildren (
                directory_id INTEGER PRIMARY KEY,
                child_id INTEGER,
                FOREIGN KEY (child_id) REFERENCES Directory(directory_id)
            )
        ''')

        # Create FileParts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS FileParts (
                file_id INTEGER,
                part_number INTEGER,
                message_id INTEGER,
                FOREIGN KEY (file_id) REFERENCES Files(file_id)
            )
        ''')

        # Commit and close the cursor
        self.connection.commit()
        cursor.close()

    def get_file_info(self, file_id):
        cursor = self.connection.cursor()

        select_statement = '''
            SELECT file_name, content_type FROM Files
            WHERE file_id = ?
        '''

        cursor.execute(select_statement, file_id)

        return cursor.fetchone()

    def get_file_parts(self, file_id):
        cursor = self.connection.cursor()

        select_statement = '''
            SELECT message_id FROM FileParts
            WHERE file_id = ?
            ORDER BY part_number ASC
        '''

        cursor.execute(select_statement, file_id)

        return list(map(lambda x: x[0], cursor.fetchall()))

    def insert_file(self, file: File, message_ids: list):
        cursor = self.connection.cursor()

        files_statement = '''
            INSERT INTO Files (file_name, content_type)
            VALUES (?, ?);
        '''

        cursor.execute(files_statement, (file.name, file.content_type))
        file_id = cursor.lastrowid

        file_parts_statement = '''
            INSERT INTO FileParts (file_id, part_number, message_id)
            VALUES (?, ?, ?);
        '''

        for part_number, message_id in enumerate(message_ids):
            cursor.execute(file_parts_statement, (file_id, part_number, message_id))

        self.connection.commit()
        cursor.close()

    def get_details(self, username, password):
        cursor = self.connection.cursor()

        users_statement = '''
            SELECT guild_id FROM Users 
            WHERE username=? AND password=?
        '''

        cursor.execute(users_statement, (username, password))

        return cursor.fetchone()


if __name__ == "__main__":
    DatabaseManager()
