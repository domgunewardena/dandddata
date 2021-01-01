import pandas as pd
from datetime import date, datetime, timedelta

import pyhdb

from sap_queries import revenue_query, covers_query, rev_df_columns, cov_df_columns
from secrets import sap_host, sap_port, sap_user, sap_password

class SAPAPI:
    
    n_drive_path = "N:/Dom/Databases/Revenue/SAP "  
    
    def __init__(self,measure):
        
        self.connection = pyhdb.connect(
            host=sap_host,
            port=sap_port,
            user=sap_user,
            password=sap_password
        )
        
        if measure=='Revenue':
            self.query = revenue_query
            self.measure = 'Revenue'
            self.measure_type = float
            self.df_columns = rev_df_columns
            
        else:
            self.query = covers_query
            self.measure = 'Covers'
            self.measure_type = int
            self.df_columns = cov_df_columns
            
        self.app_csv = 'App ' + self.measure + '.csv'
        
        self.cursor = self.get_cursor()
        self.api_result = self.api_result()
        self.app_df = self.app_df()
        
    def get_cursor(self):
        return self.connection.cursor()
    
    def api_result(self):
        
        cursor = self.cursor
        query = self.query
        
        cursor.execute(query)
        df = pd.DataFrame(cursor.fetchall())

        table_description = cursor.description
        columns = [x[0] for x in table_description]
        df.columns = columns
        
        measure = self.measure
        measure_type = self.measure_type

        df[measure] = df[measure].astype(measure_type)

        df["Calendar Week"] = df["Date"].dt.week
        df["Day of Week"] = df["Date"].dt.dayofweek + 1
        df["Day of Month"] = df["Date"].dt.day
        df["Month Num"] = df["Date"].dt.month
        df["Weekday"] = df["Date"].dt.weekday_name

        return df
    
    def app_df(self):
        
        df = self.api_result
        
        def app_df_format(self):
            
            df_columns = self.df_columns
            groupby_columns = df_columns[:-1]
            return df[df_columns].groupby(groupby_columns).sum().reset_index()


        def csv_date_filtering(df):

            def get_week(date):
                return date.isocalendar()[1]

            def get_weekdaynum(date):
                return date.isocalendar()[2]

            def get_year(date):
                return date.isocalendar()[0]

            def onedayago(date):
                return date - timedelta(1)

            def oneweekago(date):
                return date - timedelta(7)

            def fourweeksago(date):
                return date - timedelta(28)

            def oneyearago(date):
                return date - timedelta(364)

            def twelvemonthsago(date):
                if date.month==2 and date.day==29:
                    return (date-timedelta(1)).replace(year=date.year-1) 
                else:
                    return date.replace(year=date.year-1) 

            def first_day_of_week(date):
                return date - timedelta(get_weekdaynum(date)-1)

            def first_day_of_month(date):
                return date.replace(day=1)

            today = date.today()
            yesterday = onedayago(today)

            last_year_upper_bound = oneyearago(yesterday)
            last_year_lower_bound = twelvemonthsago(first_day_of_month(onedayago(first_day_of_month(today))))
            this_year_upper_bound = yesterday
            this_year_lower_bound = first_day_of_month(onedayago(first_day_of_month(onedayago(first_day_of_month(today)))))
            
            mask1 = df['Date'] <= last_year_upper_bound
            mask2 = df['Date'] >= last_year_lower_bound
            mask3 = df['Date'] <= this_year_upper_bound
            mask4 = df['Date'] >= this_year_lower_bound

            return df[(mask1 & mask2) | (mask3 & mask4)]
        
        def generate_skeleton_df(df):
        
            date_columns = ['Date','Day','OrdDay']

            skeleton_df_columns = self.df_columns.copy()
            for col in [self.measure] + date_columns:
                skeleton_df_columns.remove(col)

            skeleton_df = df[skeleton_df_columns].groupby(skeleton_df_columns).sum().reset_index()
            
            if self.measure == 'Revenue':

                rows = [
                    [
                        row[0], 
                        row[1], 
                        row[2], 
                        row[3], 
                        row[4], 
                        row[5], 
                        row[6]
                    ] for row in zip(
                        skeleton_df[skeleton_df_columns[0]],
                        skeleton_df[skeleton_df_columns[1]],
                        skeleton_df[skeleton_df_columns[2]],
                        skeleton_df[skeleton_df_columns[3]],
                        skeleton_df[skeleton_df_columns[4]],
                        skeleton_df[skeleton_df_columns[5]],
                        skeleton_df[skeleton_df_columns[6]]
                )]
                
            else:
                
                rows = [
                    [
                        row[0], 
                        row[1], 
                        row[2], 
                        row[3], 
                    ] for row in zip(
                        skeleton_df[skeleton_df_columns[0]],
                        skeleton_df[skeleton_df_columns[1]],
                        skeleton_df[skeleton_df_columns[2]],
                        skeleton_df[skeleton_df_columns[3]],
                )]

            skeleton_dates = df[date_columns].groupby(date_columns).sum().reset_index()

            date_rows = [
                [
                    row[0], 
                    row[1], 
                    row[2]
                ] for row in zip(
                    skeleton_dates[date_columns[0]],
                    skeleton_dates[date_columns[1]],
                    skeleton_dates[date_columns[2]]
            )]

            skeleton = pd.DataFrame([row + date_row for row in rows for date_row in date_rows])
            skeleton.columns = self.df_columns.copy()[:-1]
            
            return pd.merge(skeleton,df,how='outer').fillna(0)
        
        return csv_date_filtering(
            app_df_format(self)
        )       
    
    def save_csvs(self):
        
        df = self.api_result
        df.to_csv(self.measure + ".csv")
        df.to_csv(self.n_drive_path + self.measure + ".csv")
        
        df = self.app_df
        df.to_csv(self.app_csv)
        
    def send_to_database(self):
        
        import psycopg2
        from sqlalchemy import create_engine
        from secrets import postgresql_host, postgresql_database, postgresql_user, postgresql_password
        
        df = self.app_df
        
        df = df.rename(
            columns={
                'SiteName':'site_name',
                'LocationName':'location_name',
                'GenericLocation':'generic_location',
                'Session':'session',
                'OrdSession':'ord_session',
                'RevenueType':'revenue_type',
                'Wine':'wine',
                'Date':'date',
                'Day':'day',
                'OrdDay':'ord_day',
                'Revenue':'revenue',
                'Covers':'covers'
            }
        )
       
        host = postgresql_host
        database = postgresql_database
        user = postgresql_user
        password = postgresql_password

        engine_string = 'postgresql://' + user + ':' + password + '@' + host + '/' + database

        engine = create_engine(engine_string)
        con = engine.connect()

        df.to_sql(
            self.measure.lower(),
            con=con,
            index=False,
            if_exists='replace'
        )

        con.close()
