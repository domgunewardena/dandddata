# Process for creating dataframes that denote how many days of each weekday have occurred for each timeframe within each sales report - these will be merged with revenue/covers/spend dataframes to allow averages to be calculated for each day within the app

import pandas as pd

from data.date_bounds import daily_bounds, wtd_bounds, mtd_bounds, weekly_bounds, monthly_bounds

def create_day_counts_df(bounds, current_col, last_col):
    
    def day_count_df(lower, upper):
        df = pd.DataFrame(
            data=pd.date_range(
                start=lower,
                end=upper
            ),
            columns = ['Date']
        )
        df['Day'], df['Count'] = df['Date'].dt.day_name,1
        return df[['Day','Count']].groupby('Day').sum().reset_index()

    def merge_day_df(left,right):
        return pd.merge(
            left=left,
            right=right,
            on='Day'
        )

    df_tm = day_count_df(bounds[1],bounds[0])    
    df_lm = day_count_df(bounds[3],bounds[2])    
    df_ly = day_count_df(bounds[5],bounds[4])

    df = merge_day_df(merge_day_df(df_tm,df_lm),df_ly)
    df.columns = ['Day',current_col,last_col,'Last Year']
    return df

week_current_col = 'This Week'
month_current_col = 'This Month'

weekly_last_col = 'Last Week'
monthly_last_col = 'Last Month'

wtd_days = create_day_counts_df(wtd_bounds, week_current_col, weekly_last_col)
weekly_days = create_day_counts_df(weekly_bounds, week_current_col, weekly_last_col)

mtd_days = create_day_counts_df(mtd_bounds, month_current_col, monthly_last_col)
monthly_days = create_day_counts_df(monthly_bounds, month_current_col, monthly_last_col)

day_counts = {
    'wtd':wtd_days,
    'weekly':weekly_days,
    'mtd':mtd_days,
    'monthly':monthly_days
}
