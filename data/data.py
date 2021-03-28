import pandas as pd
import numpy as np
from datetime import date, datetime, timedelta
from math import floor

from data.date_bounds import bound_filtering, daily_bounds, wtd_bounds, mtd_bounds, weekly_bounds, monthly_bounds
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
}

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

def get_last_year_reviews(df):
    
    return df[df.weeks_ago > -9]

last_year_reviews = get_last_year_reviews(
    remove_null_scores(
        convert_to_bookings_restaurants(
            create_weeks_columns(
                reviews_df
            )
        )
    )
)