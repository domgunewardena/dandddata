import pandas as pd
import numpy as np
from datetime import date, datetime, timedelta

from authentication.authentication import auth
from authentication.users import user_restaurants, bookings_user_restaurants

from data.date_bounds import bound_filtering, daily_bounds, wtd_bounds, mtd_bounds, weekly_bounds, monthly_bounds

# from data.database.postgresql_tables import revenue, covers, tracker, pickup, future, trends
from data.database.postgresql_tables import revenue, covers

# rev_df = pd.read_csv("data/App Revenue.csv")
# cov_df = pd.read_csv("data/App Covers.csv")

def generate_skeleton_df(df,measure):
    
    date_columns = ['Date','Day','OrdDay']
    
    rev_df_columns = ['SiteName', 'LocationName', 'GenericLocation', 'Session', 'OrdSession', 'RevenueType', 'Wine', 'Date', 'Day', 'OrdDay', 'Revenue']
    cov_df_columns = ['SiteName', 'LocationName', 'GenericLocation', 'Session', 'Date', 'Day', 'OrdDay', 'Covers']    
    df_columns = rev_df_columns if measure=='Revenue' else cov_df_columns

    skeleton_df_columns = df_columns.copy()
    for col in [measure] + date_columns:
        skeleton_df_columns.remove(col)

    skeleton_df = df[skeleton_df_columns].groupby(skeleton_df_columns).sum().reset_index()

    if measure == 'Revenue':

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
    skeleton.columns = df_columns.copy()[:-1]

    return pd.merge(skeleton,df,how='outer').fillna(0)

rev_df = generate_skeleton_df(revenue.dataframe, 'Revenue')
cov_df = generate_skeleton_df(covers.dataframe, 'Covers')

# Add Date Columns
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

# Function to ensure any infinite values are converted to 0 to allow calculation

# def infinite(x): 
#     if x == float('inf'): 
#         return 0 
#     elif x == float('-inf'): 
#         return 0 
#     else: 
#         return x
    
tracker_df = pd.read_csv('data/Tracker.csv').iloc[:,1:]
pickup_df = pd.read_csv('data/Pickup.csv').iloc[:,1:]

future_df = pd.read_csv("data/Future Bookings.csv")
future_df['weekday'] = pd.to_datetime(future_df['visit_day']).dt.weekday_name

trends_df = pd.read_csv('data/Booking Trends.csv')
