'''Libraries'''
from peewee import PostgresqlDatabase


class DatabaseManager:
    '''Database manager class'''

    def __init__(self, database_name, user, password, host, port):
        self.database_name = database_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port

        self.db = self.connect_to_database()


    def connect_to_database(self):
        '''Create connection to database'''
        database_connection = PostgresqlDatabase(
            self.database_name,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
        )
        database_connection.connect()
        return database_connection


    def close_connection(self):
        '''Close the connection'''
        self.db.close()


    def create_tables(self, models):
        '''Create a table of models'''
        self.db.create_tables(models)
