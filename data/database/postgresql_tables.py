import psycopg2
from sqlalchemy import create_engine
import pandas as pd

from data.database.secrets import postgres_host, postgres_database, postgres_user, postgres_password

from data.database.postgresql_queries import create,select,column_names

class PostgreSQLDatabase():
    
    def __init__(self):
        
        self.host = postgres_host
        self.database = postgres_database
        self.user = postgres_user
        self.password = postgres_password

class PostgreSQLTable(PostgreSQLDatabase):
    
    def __init__(self, table):
        
        super().__init__()
        
        self.create_query = create[table]
        self.select_query = select[table]
        self.column_names = column_names[table]
        self.dataframe = self.to_dataframe()
        
    def connect_to_database(self):
        
        return psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password
        )
        
    def create(self):
        
        conn = self.connect_to_database()
        cur = conn.cursor()
        cur.execute(self.create_query)

        cur.close()
        conn.commit()
        conn.close()
        
    def to_dataframe(self):
        
        conn = self.connect_to_database()
        cur = conn.cursor()
        
        cur.execute(self.select_query)
        tuples = cur.fetchall()
        cur.close()
        conn.close()
        
        return pd.DataFrame(tuples, columns=self.column_names)

revenue = PostgreSQLTable('revenue')
covers = PostgreSQLTable('covers')
# tracker = PostgreSQLTable('tracker')
# pickup = PostgreSQLTable('pickup')
# future = PostgreSQLTable('future')
# trends = PostgreSQLTable('trends')
