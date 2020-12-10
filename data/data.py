import pandas as pd
from datetime import date, datetime, timedelta
from authentication.authentication import auth
from authentication.users import *

rev_df = pd.read_csv("data/App Revenue.csv")
rev_df['Date'] = pd.to_datetime(rev_df['Date']).dt.date
cov_df = pd.read_csv("data/App Covers.csv")
cov_df['Date'] = pd.to_datetime(cov_df['Date']).dt.date

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


# Specifying today's date as March 13th
# mar_13 = '06/03/20'
# today = datetime.strptime(mar_13, '%d/%m/%y').date()

today = date.today()
yesterday = onedayago(today)

daily_upper = daily_lower = yesterday
daily_upper_lw = daily_lower_lw = oneweekago(daily_upper)
daily_upper_ly = daily_lower_ly = oneyearago(daily_upper)

wtd_upper  = yesterday
wtd_lower = first_day_of_week(yesterday)
wtd_upper_lw = oneweekago(wtd_upper)
wtd_lower_lw = oneweekago(wtd_lower)
wtd_upper_ly = oneyearago(wtd_upper)
wtd_lower_ly = oneyearago(wtd_lower)

mtd_upper  = yesterday
mtd_lower = first_day_of_month(yesterday)
mtd_upper_lw = fourweeksago(mtd_upper)
mtd_lower_lw = fourweeksago(mtd_lower)
mtd_upper_ly = oneyearago(mtd_upper)
mtd_lower_ly = oneyearago(mtd_lower)

weekly_upper  = first_day_of_week(today) - timedelta(1)
weekly_lower = oneweekago(first_day_of_week(today))
weekly_upper_lw = oneweekago(weekly_upper)
weekly_lower_lw = oneweekago(weekly_lower)
weekly_upper_ly = oneyearago(weekly_upper)
weekly_lower_ly = oneyearago(weekly_lower)

monthly_upper  = first_day_of_month(today) - timedelta(1)
monthly_lower = first_day_of_month(monthly_upper)
monthly_upper_lw = monthly_lower-timedelta(1)
monthly_lower_lw = first_day_of_month(monthly_upper_lw)
monthly_upper_ly = twelvemonthsago(monthly_upper)
monthly_lower_ly = twelvemonthsago(monthly_lower)

def date_filtering(df, bounds):
    
    mask1 = df['Date'] <= bounds[0]
    mask2 = df['Date'] >= bounds[1]
    mask3 = df['Date'] <= bounds[2]
    mask4 = df['Date'] >= bounds[3]
    mask5 = df['Date'] <= bounds[4]
    mask6 = df['Date'] >= bounds[5]
    return df[(mask1&mask2) | (mask3&mask4) | (mask5&mask6)]

daily_bounds = [daily_upper,daily_lower,daily_upper_lw,daily_lower_lw,daily_upper_ly,daily_lower_ly]
wtd_bounds = [wtd_upper,wtd_lower,wtd_upper_lw,wtd_lower_lw,wtd_upper_ly,wtd_lower_ly]
mtd_bounds = [mtd_upper,mtd_lower,mtd_upper_lw,mtd_lower_lw,mtd_upper_ly,mtd_lower_ly]
weekly_bounds = [weekly_upper,weekly_lower,weekly_upper_lw,weekly_lower_lw,weekly_upper_ly,weekly_lower_ly]
monthly_bounds = [monthly_upper,monthly_lower,monthly_upper_lw,monthly_lower_lw,monthly_upper_ly,monthly_lower_ly]
all_bounds = [daily_bounds, wtd_bounds, mtd_bounds, weekly_bounds, monthly_bounds]

daily_rev_df,daily_cov_df = date_filtering(rev_df,daily_bounds),date_filtering(cov_df,daily_bounds)
wtd_rev_df,wtd_cov_df = date_filtering(rev_df,wtd_bounds),date_filtering(cov_df,wtd_bounds)
mtd_rev_df,mtd_cov_df = date_filtering(rev_df,mtd_bounds),date_filtering(cov_df,mtd_bounds)
weekly_rev_df,weekly_cov_df = date_filtering(rev_df,weekly_bounds),date_filtering(cov_df,weekly_bounds)
monthly_rev_df,monthly_cov_df = date_filtering(rev_df,monthly_bounds),date_filtering(cov_df,monthly_bounds)

def day_count_df(lower, upper):
    df = pd.DataFrame(
        data=pd.date_range(
            start=lower,
            end=upper
        ),
        columns = ['Date']
    )
    df['Day'], df['Count'] = df['Date'].dt.weekday_name,1
    return df[['Day','Count']].groupby('Day').sum().reset_index()
    
def merge_day_df(left,right):
    return pd.merge(
        left=left,
        right=right,
        on='Day'
    )
    
def day_df(bounds, current_col, last_col):

    df_tm = day_count_df(bounds[1],bounds[0])    
    df_lm = day_count_df(bounds[3],bounds[2])    
    df_ly = day_count_df(bounds[5],bounds[4])

    df = merge_day_df(merge_day_df(df_tm,df_lm),df_ly)
    df.columns = ['Day',current_col,last_col,'Last Year']
    return df


week_current_col, weekly_last_col = 'This Week', 'Last Week'
month_current_col, monthly_last_col = 'This Month', 'Last Month'

wtd_days = day_df(wtd_bounds, week_current_col, weekly_last_col)
weekly_days = day_df(weekly_bounds, week_current_col, weekly_last_col)

mtd_days = day_df(mtd_bounds, month_current_col, monthly_last_col)
monthly_days = day_df(monthly_bounds, month_current_col, monthly_last_col)

def infinite(x): 
    if x == float('inf'): 
        return 0 
    elif x == float('-inf'): 
        return 0 
    else: 
        return x
    
def Comp_DF(df_tw, df_lw, df_ly, on_column, current_column, last_col, vs_col):
    
    df_ty = pd.merge(
        left=df_tw,
        right=df_lw,
        on=on_column,
        how='outer'
    ).fillna(0)

    df = pd.merge(
        left=df_ty,
        right=df_ly,
        on=on_column,
        how='outer'
    ).fillna(0)

    df.columns = [on_column,current_column,last_col, 'Last Year']
    df = df.append(df.sum(numeric_only=True),ignore_index=True).fillna('Total')
    df[vs_col] = df[current_column] - df[last_col]
    df['vs. LY'] = df[current_column] - df['Last Year']
    df[vs_col + ' %'] = (df[vs_col].replace(0,1) / df[last_col].replace(0,1))
    df['vs. LY %'] = (df['vs. LY'].replace(0,1) / df['Last Year'].replace(0,1))
    return df

def Date_Splitter(df,bounds,current_column,last_col,vs_col,on_column,func):

    mask1 = df['Date'] <= bounds[0]
    mask2 = df['Date'] >= bounds[1]
    mask3 = df['Date'] <= bounds[2]
    mask4 = df['Date'] >= bounds[3]
    mask5 = df['Date'] <= bounds[4]
    mask6 = df['Date'] >= bounds[5]

    df_tw = func(df[mask1 & mask2])
    df_lw = func(df[mask3 & mask4])
    df_ly = func(df[mask5 & mask6])

    return Comp_DF(df_tw, df_lw, df_ly, on_column, current_column, last_col, vs_col)

def Spend_DF(rev_df,cov_df,on_column,current_column,last_col,vs_col):
    
    df = pd.merge(
        left=rev_df,
        right=cov_df,
        on=on_column,
        how='outer'
    )
    
    for column in [current_column, last_col, 'Last Year']:
        df[column] = df[column+'_x'] / df[column+'_y']
        
    df[vs_col] = df[current_column] - df[last_col]
    df['vs. LY'] = df[current_column] - df['Last Year']
    df[vs_col + ' %'] = (df[vs_col].replace(0,1) / df[last_col].replace(0,1))
    df['vs. LY %'] = (df['vs. LY'].replace(0,1) / df['Last Year'].replace(0,1))
    
    return df[[on_column,current_column,last_col,'Last Year',vs_col,vs_col + ' %','vs. LY','vs. LY %']]

def Area_Revenue(df):
    df_cols = ['GenericLocation', 'Revenue']
    groupby_cols = df_cols[:-1]
    return df[df_cols].groupby(groupby_cols).sum().reset_index()

def Location_Revenue(df):
    df_cols = ['LocationName', 'Revenue']
    groupby_cols = df_cols[:-1]
    return df[df_cols].groupby(groupby_cols).sum().reset_index()

def Type_Revenue(df):
    df_cols = ['RevenueType', 'Revenue']
    groupby_cols = df_cols[:-1]
    return df[df_cols].groupby(groupby_cols).sum().reset_index()

def Wine_Revenue(df):
    df_cols = ['Wine', 'Revenue']
    groupby_cols = df_cols[:-1]
    return df[df_cols].groupby(groupby_cols).sum().reset_index()

def Site_Breakdown_Revenue(df):
    df_cols = ['SiteName', 'Revenue']
    groupby_cols = df_cols[:-1]
    return df[df_cols].groupby(groupby_cols).sum().reset_index()

def Area_Covers(df):
    df_cols = ['GenericLocation', 'Covers']
    groupby_cols = df_cols[:-1]
    return df[df_cols].groupby(groupby_cols).sum().reset_index()

def Location_Covers(df):
    df_cols = ['LocationName', 'Covers']
    groupby_cols = df_cols[:-1]
    return df[df_cols].groupby(groupby_cols).sum().reset_index()

def Site_Breakdown_Covers(df):
    df_cols = ['SiteName', 'Covers']
    groupby_cols = df_cols[:-1]
    return df[df_cols].groupby(groupby_cols).sum().reset_index()


def Group_DF(df,bounds,current_column,last_col,vs_col,oncolumn,func):
    
    df = Date_Splitter(df,bounds,current_column,last_col,vs_col,oncolumn,func)
    sorter = ['Total',"Restaurant", "Bar", "PDR", "Events & Ex Hires", "Retail & Other"]
    df[oncolumn] = df[oncolumn].astype("category")
    df[oncolumn].cat.set_categories(sorter, inplace=True)
    return df.sort_values([oncolumn])

def Group_Revenue(df,bounds,current_column,last_col,vs_col,oncolumn):
    return Group_DF(df,bounds,current_column,last_col,vs_col,oncolumn,Area_Revenue)

def Group_Covers(df,bounds,current_column,last_col,vs_col,oncolumn):
    return Group_DF(df,bounds,current_column,last_col,vs_col,oncolumn,Area_Covers)

def Group_Simple_Spend(rev_df,cov_df,bounds,current_column,last_col,vs_col,oncolumn):
    
    return Spend_DF(
        Group_Revenue(rev_df,bounds,current_column,last_col,vs_col,oncolumn),
        Group_Covers(cov_df,bounds,current_column,last_col,vs_col,oncolumn),
        oncolumn,
        current_column,
        last_col,
        vs_col
    )

def Group_Spend(rev_df, cov_df, bounds, current_column,last_col,vs_col,oncolumn):
    
    df = rev_df
    bevmask = df['RevenueType'] == 'Beverage'
    foodmask = df['RevenueType'] == 'Food'   
    restaurantmask = df[oncolumn] == 'Restaurant'
    df = df[(bevmask | foodmask) & restaurantmask]
    type_df = Date_Splitter(df,bounds,current_column,last_col,vs_col,'RevenueType',Type_Revenue)
    
    df = rev_df
    bevmask = df['RevenueType'] == 'Beverage'
    foodmask = df['RevenueType'] == 'Food'
    restaurantmask = df[oncolumn] == 'Restaurant'
    df = df[bevmask & restaurantmask]
    wine_df = Date_Splitter(df,bounds,current_column,last_col,vs_col,'Wine',Wine_Revenue)
    wine_df = wine_df.drop(index=len(wine_df)-1)
    wine_df.columns = ['RevenueType',current_column,last_col,'Last Year',vs_col, vs_col + ' %', 'vs. LY', 'vs. LY %']
    
    revenue = pd.concat([type_df, wine_df],ignore_index=True, sort=False).iloc[:,:4]
    cov_df = cov_df[cov_df['GenericLocation'] == 'Restaurant']
    covers = Group_Covers(cov_df,bounds,current_column,last_col,vs_col,oncolumn).iloc[:,:4]
    covers['Join Column'] = revenue['Join Column'] = 1
    covers.columns = [oncolumn, current_column+' x', last_col + ' x', 'Last Year x', 'Join Column']
    df = pd.merge(revenue, covers, how='outer')
    for column in [current_column, last_col, 'Last Year']:
        df[column] = df[column]/df[column + ' x']
    df = df.iloc[:,:4]

    oncolumn = 'RevenueType'
    df[vs_col] = df[current_column] - df[last_col]
    df['vs. LY'] = df[current_column] - df['Last Year']
    df[vs_col + ' %'] = (df[vs_col].replace(0,1) / df[last_col].replace(0,1))
    df['vs. LY %'] = (df['vs. LY'].replace(0,1) / df['Last Year'].replace(0,1))
    sorter = ['Total','Food','Beverage','Wine','Non-Wine']
    df[oncolumn] = df[oncolumn].astype("category")
    df[oncolumn].cat.set_categories(sorter, inplace=True)
    
    return df.drop_duplicates().sort_values(by=oncolumn)

def Site_DF(site,df,bounds,current_column,last_col,vs_col,oncolumn,func):
    df = Date_Splitter(df[df['SiteName'] == site],bounds,current_column,last_col,vs_col,oncolumn,func)
    sorter = ['Total'] + df[oncolumn].drop(index=len(df)-1).to_list()
    df[oncolumn] = df[oncolumn].astype("category")
    df[oncolumn].cat.set_categories(sorter, inplace=True)
    return df.sort_values([oncolumn])

def Site_Revenue(site,df,bounds,current_column,last_col,vs_col,oncolumn):
    return Site_DF(site,df,bounds,current_column,last_col,vs_col,oncolumn,Location_Revenue)

def Site_Covers(site,df,bounds,current_column,last_col,vs_col,oncolumn):
    return Site_DF(site,df,bounds,current_column,last_col,vs_col,oncolumn,Location_Covers)

def Site_Simple_Spend(site,rev_df,cov_df,bounds,current_column,last_col,vs_col,oncolumn):
    
    return Spend_DF(
        Site_Revenue(site,rev_df,bounds,current_column,last_col,vs_col,oncolumn),
        Site_Covers(site,cov_df,bounds,current_column,last_col,vs_col,oncolumn),
        oncolumn,
        current_column,
        last_col,
        vs_col
    )

def Site_Spend(site,rev_df,cov_df,bounds,current_column,last_col,vs_col,oncolumn):
    
    df = rev_df[rev_df['SiteName'] == site]
    bevmask = df['RevenueType'] == 'Beverage'
    foodmask = df['RevenueType'] == 'Food'   
    restaurantmask = df['GenericLocation'] == 'Restaurant'
    df = df[(bevmask | foodmask) & restaurantmask]
    type_df = Date_Splitter(df,bounds,current_column,last_col,vs_col,'RevenueType',Type_Revenue)
    
    df = rev_df[rev_df['SiteName'] == site]
    bevmask = df['RevenueType'] == 'Beverage'
    restaurantmask = df['GenericLocation'] == 'Restaurant'
    df = df[bevmask & restaurantmask]
    wine_df = Date_Splitter(df,bounds,current_column,last_col,vs_col,'Wine',Wine_Revenue)
    wine_df = wine_df.drop(index=len(wine_df)-1)
    wine_df.columns = ['RevenueType',current_column,last_col,'Last Year',vs_col, vs_col + ' %', 'vs. LY', 'vs. LY %']

    revenue = pd.concat([type_df, wine_df],ignore_index=True, sort=False).iloc[:,:4]
    cov_df = cov_df[cov_df['GenericLocation'] == 'Restaurant']
    cov_df = cov_df[cov_df['SiteName'] == site]
    covers = Group_Covers(cov_df,bounds,current_column,last_col,vs_col,'GenericLocation').iloc[:,:4]
    covers['Join Column'] = revenue['Join Column'] = 1
    covers.columns = [oncolumn, current_column+' x', last_col + ' x', 'Last Year x', 'Join Column']
    df = pd.merge(revenue, covers, how='outer')
    for column in [current_column, last_col, 'Last Year']:
        df[column] = df[column]/df[column + ' x']
    df = df.iloc[:,:4]

    oncolumn = 'RevenueType'
    df[vs_col] = df[current_column] - df[last_col]
    df['vs. LY'] = df[current_column] - df['Last Year']
    df[vs_col + ' %'] = (df[vs_col].replace(0,1) / df[last_col].replace(0,1))
    df['vs. LY %'] = (df['vs. LY'].replace(0,1) / df['Last Year'].replace(0,1))
    sorter = ['Total','Food','Beverage','Wine','Non-Wine']
    df[oncolumn] = df[oncolumn].astype("category")
    df[oncolumn].cat.set_categories(sorter, inplace=True)
    
    return df.drop_duplicates().sort_values(by=oncolumn)


def Breakdown_DF(df,bounds,current_column,last_col,vs_col,oncolumn,func):
    df = Date_Splitter(df,bounds,current_column,last_col,vs_col,oncolumn,func)
    return df.drop(index=len(df)-1)
    
def Breakdown_Revenue(df,bounds,current_column,last_col,vs_col,oncolumn):
    return Breakdown_DF(df,bounds,current_column,last_col,vs_col,oncolumn,Site_Breakdown_Revenue)

def Breakdown_Covers(df,bounds,current_column,last_col,vs_col,oncolumn):
    return Breakdown_DF(df,bounds,current_column,last_col,vs_col,oncolumn,Site_Breakdown_Covers)

def Breakdown_Spend(rev_df,cov_df,bounds,current_column,last_col,vs_col,oncolumn):
    
    return Spend_DF(
        Breakdown_Revenue(rev_df,bounds,current_column,last_col,vs_col,oncolumn),
        Breakdown_Covers(cov_df,bounds,current_column,last_col,vs_col,oncolumn),
        oncolumn,
        current_column,
        last_col,
        vs_col
    )

def Comp_DF_Week(df_tw, df_lw, df_ly, on_columns, current_column, last_col, vs_col):
    
    df_ty = pd.merge(
        left=df_tw,
        right=df_lw,
        on=on_columns,
        how='outer'
    ).fillna(0)

    df = pd.merge(
        left=df_ty,
        right=df_ly,
        on=on_columns,
        how='outer'
    ).fillna(0)

    df.columns = on_columns + [current_column,last_col, 'Last Year']    
    df[vs_col] = df[current_column] - df[last_col]
    df['vs. LY'] = df[current_column] - df['Last Year']
    df[vs_col + ' %'] = (df[vs_col].replace(0,1) / df[last_col].replace(0,1))
    df['vs. LY %'] = (df[vs_col].replace(0,1) / df[last_col].replace(0,1))
    return df

def Date_Splitter_Week(df,bounds,current_column,last_col,vs_col,on_columns,func):

    mask1 = df['Date'] <= bounds[0]
    mask2 = df['Date'] >= bounds[1]
    mask3 = df['Date'] <= bounds[2]
    mask4 = df['Date'] >= bounds[3]
    mask5 = df['Date'] <= bounds[4]
    mask6 = df['Date'] >= bounds[5]

    df_tw = func(df[mask1 & mask2])
    df_lw = func(df[mask3 & mask4])
    df_ly = func(df[mask5 & mask6])

    return Comp_DF_Week(df_tw, df_lw, df_ly, on_columns, current_column, last_col, vs_col)

def Spend_DF_Week(rev_df,cov_df,on_columns,current_column,last_col,vs_col):
    
    df = pd.merge(
        left=rev_df,
        right=cov_df,
        on=on_columns,
        how='outer'
    )
    
    for column in [current_column, last_col, 'Last Year']:
        df[column] = df[column+'_x'] / df[column+'_y']
        
    df[vs_col] = df[current_column] - df[last_col]
    df['vs. LY'] = df[current_column] - df['Last Year']
    df[vs_col + ' %'] = (df[vs_col].replace(0,1) / df[last_col].replace(0,1))
    df['vs. LY %'] = (df[vs_col].replace(0,1) / df[last_col].replace(0,1))
    
    return df[on_columns + [current_column,last_col,'Last Year',vs_col,vs_col + ' %','vs. LY','vs. LY %']]

def Day_Shift_DF(df,measure):
    df_cols = ['Session','Day', measure]
    groupby_cols = df_cols[:-1]
    return df[df_cols].groupby(groupby_cols).sum().reset_index()
    
def Day_Shift_Revenue(df):
    return Day_Shift_DF(df, 'Revenue')

def Day_Shift_Covers(df):
    return Day_Shift_DF(df, 'Covers')

def Session_Day_Sorting(df):
    
    df = df[df['Session'].isin(['Lunch','Dinner'])].copy()
    session_sorter = ['Lunch','Dinner']
    day_sorter = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    df['Session'] = df['Session'].astype("category")
    df['Session'].cat.set_categories(session_sorter, inplace=True)
    df['Day'] = df['Day'].astype("category")
    df['Day'].cat.set_categories(day_sorter, inplace=True)
    return df[df['Session'].isin(['Lunch','Dinner'])].sort_values(by=['Session','Day'])

def Week_DF(site,df,bounds,current_column,last_col,vs_col,on_columns,func):
    if site=='Group':
        df = df
    else:
        df = df[df['SiteName'] == site]
    return Session_Day_Sorting(Date_Splitter_Week(df,bounds,current_column,last_col,vs_col,on_columns,func))
                
def Week_Revenue(site,category,df,bounds,day_df,current_column,last_col,vs_col,on_columns):
    if category == 'Beverage' or category == 'Food':
        df = df[df['RevenueType']==category]
    elif category == 'Wine' or category == 'Non-Wine':
        mask1 = df['RevenueType']=='Beverage'
        mask2 = df['Wine'] == category
        df = df[mask1 & mask2]
    return pd.merge(
        Week_DF(site,df,bounds,current_column,last_col,vs_col,on_columns,Day_Shift_Revenue), 
        day_df,
        how='left',
        on='Day',
        suffixes = ('',' Count')
    )

def Week_Covers(site,df,bounds,day_df,current_column,last_col,vs_col,on_columns):
    return pd.merge(
        Week_DF(site,df,bounds,current_column,last_col,vs_col,on_columns,Day_Shift_Covers), 
        day_df,
        how='left',
        on='Day',
        suffixes = ('',' Count')
    )

def Week_Spend(site,category,rev_df,cov_df,bounds,day_df,current_column,last_col,vs_col,on_columns):
    
    return Spend_DF_Week(
        Week_Revenue(site,category,rev_df,bounds,day_df,current_column,last_col,vs_col,on_columns),
        Week_Covers(site,cov_df,bounds,day_df,current_column,last_col,vs_col,on_columns),
        on_columns,
        current_column,
        last_col,
        vs_col
        )


def area_filter(df, area):
    return df[df['GenericLocation']==area] if area!='Full Site' else df

def shift_filter(df, shift):
    return df[df['Session']==shift] if shift!='All Shifts' else df

def site_filter(df, site):
    return df[df['SiteName']==site] if site !='Group' else df

def user_site_filter(df):
    return df[df['SiteName'].isin(user_restaurants[auth._username])]


tracker_df = pd.read_csv('data/Tracker.csv').iloc[:,1:]
pickup_df = pd.read_csv('data/Pickup.csv').iloc[:,1:]

def group_sort_columns(df):
    
    week_sorter = [
        'This Week', 
        'Next Week', 
        'Two Weeks', 
        'Three Weeks',
        'Four Weeks',
        'Five Weeks',
        'Six Weeks',
        'Seven Weeks',
        'Eight Weeks'
    ]

    day_sorter = [
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday',
        'Sunday',
        'Full Week'
    ]

    columns = ['Week','Day']
    sorters = [week_sorter, day_sorter]

    for i in range(2):
        df[columns[i]] = df[columns[i]].astype('category')
        df[columns[i]].cat.set_categories(sorters[i], inplace=True)

    return df.sort_values(['Week','Day'])


def add_comparison_columns(df):
    
    df['vs. LW'] = df['This Week'] - df['Last Week']
    df['vs. LW %'] = (df['vs. LW'].replace(0,1) / df['Last Week'].replace(0,1))
    df['vs. LY'] = df['This Week'] - df['Last Year']
    df['vs. LY %'] = (df['vs. LY'].replace(0,1)  / df['Last Year'].replace(0,1))
    
    return df


def tracker_user_site_filter(df):
    return df[df['Restaurant'].isin(bookings_user_restaurants[auth._username])]

def tracker_group_df(df):
    df=df[df['Restaurant']!='Modern Pantry']
    df_columns = list(df.columns)[1:]
    groupby_columns = df_columns[:2]
    return add_comparison_columns(group_sort_columns(df[df_columns].groupby(groupby_columns).sum().reset_index()))

def tracker_site_filter(df, site):
    return df[df['Restaurant']==site]

def tracker_week_filter(df, week):
    return df[df['Week']==week]

def tracker_day_filter(df, graph_type):
    return df[df['Day'] == 'Full Week'] if graph_type == '8 Week' else df[df['Day'] != 'Full Week'] 


future_df = pd.read_csv("data/Future Bookings.csv")
future_df['weekday'] = pd.to_datetime(future_df['visit_day']).dt.weekday_name

trends_df = pd.read_csv('data/Booking Trends.csv')

def trends_table_filter(df, table):
    return df[df['Table']==table]

def trends_site_filter(df, site):
    return df[df['Restaurant'] == 'Group'] if site=='Group' else df[df['Restaurant']!='Group']
