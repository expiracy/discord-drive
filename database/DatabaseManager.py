import sqlite3

from storage import File


class DatabaseManager:

    def __init__(self):
        DatabaseManager.create_tables()

    @staticmethod
    def get_connection():
        return sqlite3.connect('discord_storage.db')

    @staticmethod
    def create_tables():
        connection = DatabaseManager.get_connection()
        cursor = connection.cursor()

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
                directory_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                directory_name VARCHAR(100),
                parent_id INTEGER,
                guild_id INTEGER,
                FOREIGN KEY (parent_id) REFERENCES Directory(directory_id)
                FOREIGN KEY (guild_id) REFERENCES Servers(guild_id)
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

        connection.commit()
        cursor.close()

    @staticmethod
    def get_file_info(file_id):
        cursor = DatabaseManager.get_connection().cursor()

        select_statement = '''
            SELECT file_name, content_type FROM Files
            WHERE file_id = ?
        '''

        cursor.execute(select_statement, file_id)

        res = cursor.fetchone()
        cursor.close()
        return res

    @staticmethod
    def get_file_parts(file_id):
        cursor = DatabaseManager.get_connection().cursor()

        select_statement = '''
            SELECT message_id FROM FileParts
            WHERE file_id = ?
            ORDER BY part_number ASC
        '''

        cursor.execute(select_statement, file_id)
        res = cursor.fetchall()
        cursor.close()

        return list(map(lambda x: x[0], res))

    @staticmethod
    def insert_file(file: File, message_ids: list):
        connection = DatabaseManager.get_connection()
        cursor = connection.cursor()

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

        connection.commit()
        cursor.close()

    @staticmethod
    def register_user(username, password, guild_id, channel_id):
        connection = DatabaseManager.get_connection()
        cursor = connection.cursor()

        servers_statement = '''
            INSERT OR REPLACE INTO Servers(guild_id, channel_id)
            values (?, ?);
        '''

        cursor.execute(servers_statement, (guild_id, channel_id))
        connection.commit()

        users_statement = '''
            INSERT INTO Users(username, password, guild_id)
            VALUES (?, ?, ?);
        '''

        cursor.execute(users_statement, (username, password, guild_id))
        connection.commit()
        cursor.close()

    @staticmethod
    def get_details(username, password):
        connection = DatabaseManager.get_connection()
        cursor = connection.cursor()

        users_statement = '''
            SELECT guild_id FROM Users 
            WHERE username=? AND password=?
        '''

        cursor.execute(users_statement, (username, password))

        res = cursor.fetchone()
        cursor.close()
        return res

    @staticmethod
    def add_directory(directory_name: str, parent_id: int, guild_id: int):
        connection = DatabaseManager.get_connection()
        cursor = connection.cursor()

        directory_statement = '''
            INSERT INTO Directory(directory_name, parent_id, guild_id)
            VALUES (?, ?, ?)
        '''

        args = (directory_name, parent_id, guild_id)
        if parent_id == -1:
            args = (directory_name, None, guild_id)

        cursor.execute(directory_statement, args)
        connection.commit()
        cursor.close()

    @staticmethod
    def get_root_directory(guild_id):
        connection = DatabaseManager.get_connection()
        cursor = connection.cursor()

        root_directory_statement = '''
            SELECT directory_id FROM Directory
            WHERE parent_id IS NULL AND guild_id=?
        '''

        cursor.execute(root_directory_statement, guild_id)

        res = cursor.fetchone()
        cursor.close()
        return res


if __name__ == '__main__':
    database = DatabaseManager()
