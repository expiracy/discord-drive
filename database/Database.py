import sqlite3

from storage import File


class Database:

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

        # Create DirectoryChildren table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS DirectoryChildren (
                directory_id INTEGER,
                child_id INTEGER,
                FOREIGN KEY (child_id) REFERENCES Directory(directory_id),
                FOREIGN KEY (directory_id) REFERENCES Directory(directory_id),
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

    def get_directory_folders(self, directory_id):
        self.cursor.execute('''
            SELECT directory_id, directory_name FROM Directory
            WHERE parent_id=?
        ''', (directory_id,))

        folders = self.cursor.fetchall()

        if not folders:
            return []

        return folders

    def get_directory_files(self, directory_id):
        self.cursor.execute('''
            SELECT file_id, file_name, directory_id FROM Files
            WHERE directory_id=?
            ORDER BY file_name ASC;
        ''', (directory_id,))

        files = self.cursor.fetchall()

        if not files:
            return []

        return files

    def get_directory(self, directory_id):
        return self.get_directory_files(directory_id), self.get_directory_folders(directory_id)

    def get_file_parts(self, file_id):
        file_parts_statement = '''
            SELECT message_id FROM FileParts
            WHERE file_id = ?
            ORDER BY part_number ASC;
        '''

        self.cursor.execute(file_parts_statement, (file_id,))
        message_ids = self.cursor.fetchall()

        if not message_ids:
            return []
        print(list(map(lambda x: x[0], message_ids)))
        return list(map(lambda x: x[0], message_ids))

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
        self.cursor.execute('''
            SELECT guild_id FROM Users 
            WHERE username=? AND password=?
        ''', (username, password))

        res = self.cursor.fetchone()

        if not res:
            return None

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

    def get_file_channel_id(self, guild_id):
        self.cursor.execute('''
            SELECT channel_id FROM Servers
            WHERE guild_id=?;
        ''', (guild_id,))

        file_channel_id = self.cursor.fetchone()

        if not file_channel_id:
            return None

        return file_channel_id[0]

    def get_home_directory_id(self, guild_id):

        self.cursor.execute('''
            SELECT root_directory_id FROM Servers
            WHERE guild_id=?;
        ''', (guild_id,))

        home_directory_id = self.cursor.fetchone()

        if not home_directory_id:
            return None

        return home_directory_id[0]

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

    def delete_file(self, file_id):
        # File not in DB
        if not self.get_file_info(file_id):
            return False

        self.cursor.execute('''
            DELETE FROM Files
            WHERE file_id=?;
        ''', (file_id,))

        self.cursor.execute('''
            DELETE FROM FileParts
            WHERE file_id=?;
        ''', (file_id,))

        self.connection.commit()

        return True

    def delete_directory(self, directory_id):
        if not self.get_directory(directory_id):
            return False

        files = self.get_directory_files(directory_id)

        for file_id, _, _ in files:
            self.delete_file(file_id)

        children = self.get_directory_children(directory_id)

        self.cursor.execute('''
            DELETE FROM DirectoryChildren
            WHERE directory_id=? AND child_id=?;
         ''', (self.get_directory_parent(directory_id), directory_id))

        for child_id in children:
            print(child_id, directory_id)
            self.delete_directory(child_id)

            self.cursor.execute('''
                DELETE FROM DirectoryChildren
                WHERE directory_id=? AND child_id=?;
             ''', (directory_id, child_id))

        self.cursor.execute('''
            DELETE FROM Directory
            WHERE directory_id=?;
        ''', (directory_id,))

        self.connection.commit()

        return True

    def get_directory_parent(self, directory_id):
        self.cursor.execute('''
            SELECT parent_id FROM Directory
            WHERE directory_id=?;
        ''', (directory_id,))

        parent = self.cursor.fetchone()

        if not parent:
            return None

        return parent[0]

    def get_directory_children(self, directory_id):
        self.cursor.execute('''
            SELECT child_id FROM DirectoryChildren
            WHERE directory_id=?;
        ''', (directory_id,))

        children = self.cursor.fetchall()

        if not children:
            return []

        return list(map(lambda x: x[0], children))


if __name__ == '__main__':
    database = Database()
    database.create_tables()
