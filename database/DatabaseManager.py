import sqlite3

from storage import File


class DatabaseManager:

    def __init__(self):
        self.connection = sqlite3.connect('discord_storage.db')
        self.cursor = self.connection.cursor()

    def create_tables(self):
        # Create Servers table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Servers (
                guild_id INTEGER PRIMARY KEY,
                channel_id INTEGER,
                root_directory_id INTEGER,
                FOREIGN KEY (root_directory_id) REFERENCES Directory(directory_id)
            )
        ''')

        # Create Users table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                username VARCHAR(32),
                password VARCHAR(100),
                guild_id INTEGER,
                FOREIGN KEY (guild_id) REFERENCES Servers(guild_id)
            )
        ''')

        # Create Files table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Files (
                file_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                file_name VARCHAR(100),
                content_type VARCHAR(10),
                directory_id INTEGER,
                file_timestamp TIMESTAMP,
                guild_id INTEGER,
                FOREIGN KEY (directory_id) REFERENCES Directory(directory_id)
            )
        ''')

        # Create Directory table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Directory (
                directory_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                directory_name VARCHAR(100),
                parent_id INTEGER,
                FOREIGN KEY (parent_id) REFERENCES Directory(directory_id)
            )
        ''')

        # Create DirectoryChil`dren table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS DirectoryChildren (
                directory_id INTEGER,
                child_id INTEGER,
                FOREIGN KEY (child_id) REFERENCES Directory(directory_id),
                PRIMARY KEY(directory_id, child_id)
            )
        ''')

        # Create FileParts table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS FileParts (
                file_id INTEGER,
                part_number INTEGER,
                message_id INTEGER,
                FOREIGN KEY (file_id) REFERENCES Files(file_id)
            )
        ''')

        self.connection.commit()

    def get_file_info(self, file_id):
        select_statement = '''
            SELECT file_name, content_type FROM Files
            WHERE file_id = ?;
        '''

        self.cursor.execute(select_statement, (file_id,))

        res = self.cursor.fetchone()
        return res

    def get_directory(self, directory_id):
        files_statement = '''
            SELECT file_id, file_name, directory_id FROM Files
            WHERE directory_id=?
            ORDER BY file_name ASC;
        '''

        self.cursor.execute(files_statement, (directory_id,))
        files = self.cursor.fetchall()

        directory_statement = '''
            SELECT directory_id, directory_name FROM Directory
            WHERE parent_id=?
        '''
        self.cursor.execute(directory_statement, (directory_id,))

        folders = self.cursor.fetchall()

        return files, folders

    def get_file_parts(self, file_id):
        file_parts_statement = '''
            SELECT message_id FROM FileParts
            WHERE file_id = ?
            ORDER BY part_number ASC;
        '''

        self.cursor.execute(file_parts_statement, (file_id,))
        res = self.cursor.fetchall()

        return list(map(lambda x: x[0], res))

    def insert_file(self, file: File, message_ids: list, directory_id: int, guild_id: int):
        files_statement = '''
            INSERT INTO Files (file_name, content_type, directory_id, guild_id)
            VALUES (?, ?, ?, ?);
        '''

        self.cursor.execute(files_statement, (file.name, file.content_type, directory_id, guild_id))
        file_id = self.cursor.lastrowid

        file_parts_statement = '''
            INSERT INTO FileParts (file_id, part_number, message_id)
            VALUES (?, ?, ?);
        '''

        for part_number, message_id in enumerate(message_ids):
            self.cursor.execute(file_parts_statement, (file_id, part_number, message_id))

        self.connection.commit()

    def register_user(self, username, password, guild_id, channel_id, directory_id):
        servers_statement = '''
            INSERT INTO Servers(guild_id, channel_id, root_directory_id)
            values (?, ?, ?);
        '''

        self.cursor.execute(servers_statement, (guild_id, channel_id, directory_id))
        self.connection.commit()

        users_statement = '''
            INSERT INTO Users(username, password, guild_id)
            VALUES (?, ?, ?);
        '''

        self.cursor.execute(users_statement, (username, password, guild_id))
        self.connection.commit()

    def get_details(self, username, password):
        users_statement = '''
            SELECT guild_id FROM Users 
            WHERE username=? AND password=?
        '''

        self.cursor.execute(users_statement, (username, password))

        res = self.cursor.fetchone()
        return res

    def add_directory(self, directory_name: str, parent_id):
        directory_statement = '''
            INSERT INTO Directory(directory_name, parent_id)
            VALUES (?, ?)
        '''

        self.cursor.execute(directory_statement, (directory_name, parent_id))

        directory_id = self.cursor.lastrowid
        self.connection.commit()

        return directory_id

    def get_root(self, guild_id):
        server_statement = '''
            SELECT channel_id, root_directory_id FROM Servers
            WHERE guild_id=?;
        '''

        self.cursor.execute(server_statement, (guild_id,))

        res = self.cursor.fetchone()
        return res

    def create_directory(self, directory_name, parent_id):
        directory_statement = '''
            INSERT INTO Directory(directory_name, parent_id)
            VALUES (?, ?);
        '''

        self.cursor.execute(directory_statement, (directory_name, parent_id))
        self.connection.commit()
        child_id = self.cursor.lastrowid

        children_statement = '''
            INSERT INTO DirectoryChildren
            VALUES (?, ?);
        '''

        self.cursor.execute(children_statement, (parent_id, child_id))
        self.connection.commit()

    def search(self, substring, guild_id, directory_id=None):
        search_statement = '''
            SELECT file_id, file_name, directory_id FROM Files
            WHERE file_name LIKE '%' || ? || '%' 
        '''

        if directory_id:
            search_statement += "AND directory_id=?;"
            self.cursor.execute(search_statement, (substring, directory_id))
        else:
            search_statement += "AND guild_id=?;"
            self.cursor.execute(search_statement, (substring, guild_id))

        return self.cursor.fetchall()

if __name__ == '__main__':
    database = DatabaseManager()
    database.create_tables()
