import psycopg2
from sqlalchemy import create_engine
import pandas as pd

from secrets import postgres_host, postgres_database, postgres_user, postgres_password

from postgresql_queries import create,select,column_names

class PostgreSQLDatabase():
    
    def __init__(self):
        
        self.host = postgres_host
        self.database = postgres_database
        self.user = postgres_user
        self.password = postgres_password

class PostgreSQLTable(PostgreSQLDatabase):
    
    def __init__(self):
        
        super().__init__()
        
        self.create_query = ''
        self.select_query = ''
        self.column_names = ''
        
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
        return tuples

class Tracker(PostgreSQLTable):
    
    def __init__(self):
        
        super().__init__()
        
        self.create_query = create['tracker']
        self.select_query = select['tracker']
        self.column_names = column_names['tracker']
        self.dataframe = self.to_dataframe()
        
class Pickup(PostgreSQLTable):
    
    def __init__(self):
        
        super().__init__()
        
        self.create_query = create['pickup']
        self.select_query = select['pickup']
        self.column_names = column_names['pickup']
        self.dataframe = self.to_dataframe()
        
class Trends(PostgreSQLTable):
    
    def __init__(self):
        
        super().__init__()
        
        self.create_query = create['trends']
        self.select_query = select['trends']
        self.column_names = column_names['trends']
        self.dataframe = self.to_dataframe()
        
class Future(PostgreSQLTable):
    
    def __init__(self):
        
        super().__init__()
        
        self.create_query = create['future']
        self.select_query = select['future']
        self.column_names = column_names['future']
        self.dataframe = self.to_dataframe()
        
class Revenue(PostgreSQLTable):
    
    def __init__(self):
        
        super().__init__()
        
        self.create_query = create['revenue']
        self.select_query = select['revenue']
        self.column_names = column_names['revenue']
        self.dataframe = self.to_dataframe()
        
class Covers(PostgreSQLTable):
    
    def __init__(self):
        
        super().__init__()
        
        self.create_query = create['covers']
        self.select_query = select['covers']
        self.column_names = column_names['covers']
        self.dataframe = self.to_dataframe()
