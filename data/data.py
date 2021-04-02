import pandas as pd
import numpy as np
from datetime import date, datetime, timedelta
from math import floor

from data.date_bounds import bound_filtering, daily_bounds, wtd_bounds, mtd_bounds, weekly_bounds, monthly_bounds, four_weeks_bounds
from data.skeleton import generate_skeleton_df
from data.database.postgresql_tables import PostgreSQLTable

# rev_df = pd.read_csv("data/App Revenue.csv")
# cov_df = pd.read_csv("data/App Covers.csv")

# tracker_df = pd.read_csv('data/Tracker.csv').iloc[:,1:]
# pickup_df = pd.read_csv('data/Pickup.csv').iloc[:,1:]

# future_df = pd.read_csv("data/Future Bookings.csv")
# trends_df = pd.read_csv('data/Booking Trends.csv')

tracker = PostgreSQLTable('tracker')
pickup = PostgreSQLTable('pickup')
future = PostgreSQLTable('future')
trends = PostgreSQLTable('trends')
revenue = PostgreSQLTable('revenue')
covers = PostgreSQLTable('covers')
reviews = PostgreSQLTable('reviews')

tracker_df = tracker.dataframe
pickup_df = pickup.dataframe
trends_df = trends.dataframe
future_df = future.dataframe
# rev_df = generate_skeleton_df(revenue.dataframe, 'Revenue')
# cov_df = generate_skeleton_df(covers.dataframe, 'Covers')
rev_df = revenue.dataframe
cov_df = covers.dataframe
reviews_df = reviews.dataframe

# Add Date Columns
future_df['visit_day'] = pd.to_datetime(future_df['visit_day'])
future_df['weekday'] = pd.to_datetime(future_df['visit_day']).dt.weekday_name
rev_df['Date'] = pd.to_datetime(rev_df['Date']).dt.date
cov_df['Date'] = pd.to_datetime(cov_df['Date']).dt.date

# Generating each sales report dataframe by filtering by date bounds
daily_rev_df = bound_filtering(rev_df,daily_bounds)
daily_cov_df = bound_filtering(cov_df,daily_bounds)
wtd_rev_df = bound_filtering(rev_df,wtd_bounds)
wtd_cov_df = bound_filtering(cov_df,wtd_bounds)
mtd_rev_df = bound_filtering(rev_df,mtd_bounds)
mtd_cov_df = bound_filtering(cov_df,mtd_bounds)
weekly_rev_df = bound_filtering(rev_df,weekly_bounds)
weekly_cov_df = bound_filtering(cov_df,weekly_bounds)
monthly_rev_df = bound_filtering(rev_df,monthly_bounds)
monthly_cov_df = bound_filtering(cov_df,monthly_bounds)
four_weeks_rev_df = bound_filtering(rev_df,four_weeks_bounds)
four_weeks_cov_df = bound_filtering(cov_df,four_weeks_bounds)

sales_dataframes = {
  'daily':{
    'revenue':daily_rev_df,
    'covers':daily_cov_df
  },
  'wtd':{
    'revenue':wtd_rev_df,
    'covers':wtd_cov_df
  },
  'mtd':{
    'revenue':mtd_rev_df,
    'covers':mtd_cov_df
  },
  'weekly':{
    'revenue':weekly_rev_df,
    'covers':weekly_cov_df
  },
  'monthly':{
    'revenue':monthly_rev_df,
    'covers':monthly_cov_df
  },
  'four_weeks':{
    'revenue':four_weeks_rev_df,
    'covers':four_weeks_cov_df
  },
}


# Creating future df by week for future breakdown

def create_weeks_columns(df):
    
    today = datetime.today()    
#     today = datetime.strptime('2021-04-12','%Y-%m-%d')
    
    def weeks_ahead(date):
        monday = date - timedelta(date.weekday())
        return floor(((monday - today).days)/7)+1
    
    def weeks_label(weeks_ahead):
        return 'This Week' if weeks_ahead == 0 else 'Next Week' if weeks_ahead == 1 else str(weeks_ahead) + ' Weeks Ahead'

    df['weeks_ahead'] = df['visit_day'].apply(weeks_ahead)
    df['weeks'] = df['weeks_ahead'].apply(weeks_label)
    
    return df

df = create_weeks_columns(future_df)
df_columns = ['restaurant','weeks_ahead','weeks','capacity','max_guests TW']
groupby_columns = df_columns[:-2]

dff = df[df_columns].groupby(groupby_columns).sum().reset_index()
dff['full'] = dff['max_guests TW']/dff['capacity']

def reduce_minus(value):
    return 0 if value < 0 else value

dff['empty'] = (dff['capacity']-dff['max_guests TW']).apply(reduce_minus)
future_breakdown_df = dff


# Getting last year reviews

def create_weeks_columns(df):
    
    today = datetime.today()
    
    def weeks_ago(date):
        return -floor(((today - date).days)/7)-1
    
    def weeks_label(weeks_ago):
        return 'Last Week' if weeks_ago == -1 else str(-weeks_ago) + ' Weeks Ago'

    df['weeks_ago'] = df['date'].apply(weeks_ago)
    df['weeks'] = df['weeks_ago'].apply(weeks_label)
    
    return df

def convert_to_bookings_restaurants(df):

    def map_restaurant(restaurant):

        restaurant_map = {
            '100 Wardour Street':'100 Wardour St',
            'Cantina':'Cantina del Ponte',
            'South Place Chophouse':'South Place Chop House'        
        }

        try:
            return restaurant_map[restaurant]
        except KeyError:
            return restaurant
    
    df.restaurant = df.restaurant.apply(map_restaurant)
    
    return df

def remove_null_scores(df):
    
    def remove_0(score):
        return None if score==0 else score

    for col in ['food','service','ambience','value']:
        df[col]=df[col].apply(remove_0)
        
    return df

def rename_score_column(df):
    
     return df.rename(columns={'score':'overall'})

reviews_dff = rename_score_column(
    remove_null_scores(
        convert_to_bookings_restaurants(
            create_weeks_columns(
                reviews_df
            )
        )
    )
)