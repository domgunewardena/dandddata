import pandas as pd
import pandas.io.sql as psql
import os
import psycopg2
from sqlalchemy import create_engine

postgres_host = os.environ['POSTGRESQL_HOST']
postgres_database = os.environ['POSTGRESQL_DATABASE']
postgres_user = os.environ['POSTGRESQL_USER']
postgres_password = os.environ['POSTGRESQL_PASSWORD']
postgres_url = os.environ['HEROKU_POSTGRESQL_CHARCOAL_URL']

from data.database.postgresql_queries import create,select,column_names,column_renaming_map

class PostgreSQLDatabase():
    
    def __init__(self):
        
        self.host = postgres_host
        self.database = postgres_database
        self.user = postgres_user
        self.password = postgres_password
        self.url = postgres_url

class PostgreSQLTable(PostgreSQLDatabase):
    
    def __init__(self, table):
        
        super().__init__()
        
        self.create_query = create[table]
        self.select_query = select[table]
        self.column_names = column_names[table]
        self.column_renaming_map = column_renaming_map[table]
        self.dataframe = self.to_app()
        
    def connect_remotely(self):
        
        return psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password
        )
    
    def connect_from_app(self):
        
        return psycopg2.connect(self.url, sslmode='require')
        
    def create(self):
        
        conn = self.connect_remotely()
        cur = conn.cursor()
        cur.execute(self.create_query)

        cur.close()
        conn.commit()
        conn.close()
        
    def to_dataframe(self):
        
        conn = self.connect_remotely()
        cur = conn.cursor()
        
        cur.execute(self.select_query)
        tuples = cur.fetchall()
        cur.close()
        conn.close()
        
        return pd.DataFrame(tuples, columns=self.column_names)

    def to_app(self):
        
        conn = self.connect_from_app()
        df = psql.read_sql(self.select_query, conn)
        return df.rename(columns = self.column_renaming_map)
    
    
    
#     def to_app(self):
        
#         conn = self.connect_from_app()
#         cur = conn.cursor()
        
#         cur.execute(self.select_query)
#         tuples = cur.fetchall()
#         cur.close()
#         conn.close()
        
#         return pd.DataFrame(tuples, columns=self.column_names)
