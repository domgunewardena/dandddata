import pandas as pd
import numpy as np
from datetime import date, datetime, timedelta

from authentication.authentication import auth
from authentication.users import user_restaurants, bookings_user_restaurants

from data.date_bounds import bound_filtering, daily_bounds, wtd_bounds, mtd_bounds, weekly_bounds, monthly_bounds
from data.skeleton import generate_skeleton_df

from data.database.postgresql_tables import revenue, covers, tracker, pickup, future, trends

# rev_df = pd.read_csv("data/App Revenue.csv")
# cov_df = pd.read_csv("data/App Covers.csv")

# tracker_df = pd.read_csv('data/Tracker.csv').iloc[:,1:]
# pickup_df = pd.read_csv('data/Pickup.csv').iloc[:,1:]

# future_df = pd.read_csv("data/Future Bookings.csv")
# future_df['weekday'] = pd.to_datetime(future_df['visit_day']).dt.weekday_name

# trends_df = pd.read_csv('data/Booking Trends.csv')

tracker_df = tracker.dataframe
pickup_df = pickup.dataframe
trends_df = trends.dataframe
future_df = future.dataframe
future_df['weekday'] = pd.to_datetime(future_df['visit_day']).dt.weekday_name
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
