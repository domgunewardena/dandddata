# Data processing functions that are called within graph functions - generating dataframes that are fed into figures in the front end
  
import pandas as pd
import numpy as np
from datetime import date, datetime, timedelta

from authentication.authentication import auth
from authentication.users import user_restaurants

# Returns final dataframe that gets fed into figure functions - generating columns for each time period (current, last, last year) & comparison columns    
def final_dataframe(dfs, on_column, current_column, last_col, vs_col):
    
    df_ty = pd.merge(
        left=dfs[0],
        right=dfs[1],
        on=on_column,
        how='outer'
    ).fillna(0)

    df = pd.merge(
        left=df_ty,
        right=dfs[2],
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

def date_filtering(df,bounds,current_column,last_col,vs_col,on_column,func):

    mask1 = df['Date'] <= bounds[0]
    mask2 = df['Date'] >= bounds[1]
    mask3 = df['Date'] <= bounds[2]
    mask4 = df['Date'] >= bounds[3]
    mask5 = df['Date'] <= bounds[4]
    mask6 = df['Date'] >= bounds[5]

    df1 = func(df[mask1 & mask2])
    df2 = func(df[mask3 & mask4])
    df3 = func(df[mask5 & mask6])
    
    dfs = [df1,df2,df3]
    
    def fill_empty_dataframe_with_zero_values(dfs):
        
        def get_populated_df(dfs):
            
            return [df for df in dfs if df.empty==False][0].copy()
        
        def get_empty_df(populated_df):
            
            df = populated_df.copy()
            
            for col in df.columns:
                if np.issubdtype(df[col].dtype, np.number):
                    df[col].values[:] = 0
                    
            return df
        
        empty_df = get_empty_df(get_populated_df(dfs))
        
        return [empty_df if df.empty else df for df in dfs]
    
    dfs = fill_empty_dataframe_with_zero_values(dfs)

    return final_dataframe(dfs, on_column, current_column, last_col, vs_col)

def spend_df(rev_df,cov_df,on_column,current_column,last_col,vs_col):
    
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


def group_revenue_by_area(df):
    df_cols = ['GenericLocation', 'Revenue']
    groupby_cols = df_cols[:-1]
    return df[df_cols].groupby(groupby_cols).sum().reset_index()

def group_revenue_by_location(df):
    df_cols = ['LocationName', 'Revenue']
    groupby_cols = df_cols[:-1]
    return df[df_cols].groupby(groupby_cols).sum().reset_index()

def group_revenue_by_type(df):
    df_cols = ['RevenueType', 'Revenue']
    groupby_cols = df_cols[:-1]
    return df[df_cols].groupby(groupby_cols).sum().reset_index()

def group_revenue_by_wine(df):
    df_cols = ['Wine', 'Revenue']
    groupby_cols = df_cols[:-1]
    return df[df_cols].groupby(groupby_cols).sum().reset_index()

def group_revenue_by_site(df):
    df_cols = ['SiteName', 'Revenue']
    groupby_cols = df_cols[:-1]
    return df[df_cols].groupby(groupby_cols).sum().reset_index()

def group_covers_by_area(df):
    df_cols = ['GenericLocation', 'Covers']
    groupby_cols = df_cols[:-1]
    return df[df_cols].groupby(groupby_cols).sum().reset_index()

def group_covers_by_location(df):
    df_cols = ['LocationName', 'Covers']
    groupby_cols = df_cols[:-1]
    return df[df_cols].groupby(groupby_cols).sum().reset_index()

def group_covers_by_site(df):
    df_cols = ['SiteName', 'Covers']
    groupby_cols = df_cols[:-1]
    return df[df_cols].groupby(groupby_cols).sum().reset_index()


def group_general_df(df,bounds,current_column,last_col,vs_col,oncolumn,func):
    
    df = date_filtering(df,bounds,current_column,last_col,vs_col,oncolumn,func)
    sorter = ['Total',"Restaurant", "Bar", "PDR", "Events & Ex Hires", "Retail & Other"]
    df[oncolumn] = df[oncolumn].astype("category")
    df[oncolumn].cat.set_categories(sorter, inplace=True)
    return df.sort_values([oncolumn])

def group_revenue_df(df,bounds,current_column,last_col,vs_col,oncolumn):
    return group_general_df(df,bounds,current_column,last_col,vs_col,oncolumn,group_revenue_by_area)

def group_covers_df(df,bounds,current_column,last_col,vs_col,oncolumn):
    return group_general_df(df,bounds,current_column,last_col,vs_col,oncolumn,group_covers_by_area)

def group_simple_spend_df(rev_df,cov_df,bounds,current_column,last_col,vs_col,oncolumn):
    
    return spend_df(
        group_revenue_df(rev_df,bounds,current_column,last_col,vs_col,oncolumn),
        group_covers_df(cov_df,bounds,current_column,last_col,vs_col,oncolumn),
        oncolumn,
        current_column,
        last_col,
        vs_col
    )

def group_spend_df(rev_df, cov_df, bounds, current_column,last_col,vs_col,oncolumn):
    
    df = rev_df
    bevmask = df['RevenueType'] == 'Beverage'
    foodmask = df['RevenueType'] == 'Food'   
    restaurantmask = df[oncolumn] == 'Restaurant'
    df = df[(bevmask | foodmask) & restaurantmask]
    type_df = date_filtering(df,bounds,current_column,last_col,vs_col,'RevenueType',group_revenue_by_type)
    
    df = rev_df
    bevmask = df['RevenueType'] == 'Beverage'
    foodmask = df['RevenueType'] == 'Food'
    restaurantmask = df[oncolumn] == 'Restaurant'
    df = df[bevmask & restaurantmask]
    wine_df = date_filtering(df,bounds,current_column,last_col,vs_col,'Wine',group_revenue_by_wine)
    wine_df = wine_df.drop(index=len(wine_df)-1)
    wine_df.columns = ['RevenueType',current_column,last_col,'Last Year',vs_col, vs_col + ' %', 'vs. LY', 'vs. LY %']
    
    revenue = pd.concat([type_df, wine_df],ignore_index=True, sort=False).iloc[:,:4]
    cov_df = cov_df[cov_df['GenericLocation'] == 'Restaurant']
    covers = group_covers_df(cov_df,bounds,current_column,last_col,vs_col,oncolumn).iloc[:,:4]
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

def site_general_df(site,df,bounds,current_column,last_col,vs_col,oncolumn,func):
    df = date_filtering(df[df['SiteName'] == site],bounds,current_column,last_col,vs_col,oncolumn,func)
    sorter = ['Total'] + df[oncolumn].drop(index=len(df)-1).to_list()
    df[oncolumn] = df[oncolumn].astype("category")
    df[oncolumn].cat.set_categories(sorter, inplace=True)
    return df.sort_values([oncolumn])

def site_revenue_df(site,df,bounds,current_column,last_col,vs_col,oncolumn):
    return site_general_df(site,df,bounds,current_column,last_col,vs_col,oncolumn,group_revenue_by_location)

def site_covers_df(site,df,bounds,current_column,last_col,vs_col,oncolumn):
    return site_general_df(site,df,bounds,current_column,last_col,vs_col,oncolumn,group_covers_by_location)

def site_simple_spend_df(site,rev_df,cov_df,bounds,current_column,last_col,vs_col,oncolumn):
    
    return spend_df(
        site_revenue_df(site,rev_df,bounds,current_column,last_col,vs_col,oncolumn),
        site_covers_df(site,cov_df,bounds,current_column,last_col,vs_col,oncolumn),
        oncolumn,
        current_column,
        last_col,
        vs_col,
    )

def site_spend_df(site,rev_df,cov_df,bounds,current_column,last_col,vs_col,oncolumn):
    
    df = rev_df[rev_df['SiteName'] == site]
    bevmask = df['RevenueType'] == 'Beverage'
    foodmask = df['RevenueType'] == 'Food'   
    restaurantmask = df['GenericLocation'] == 'Restaurant'
    df = df[(bevmask | foodmask) & restaurantmask]
    type_df = date_filtering(df,bounds,current_column,last_col,vs_col,'RevenueType',group_revenue_by_type)
    
    df = rev_df[rev_df['SiteName'] == site]
    bevmask = df['RevenueType'] == 'Beverage'
    restaurantmask = df['GenericLocation'] == 'Restaurant'
    df = df[bevmask & restaurantmask]
    wine_df = date_filtering(df,bounds,current_column,last_col,vs_col,'Wine',group_revenue_by_wine)
    wine_df = wine_df.drop(index=len(wine_df)-1)
    wine_df.columns = ['RevenueType',current_column,last_col,'Last Year',vs_col, vs_col + ' %', 'vs. LY', 'vs. LY %']

    revenue = pd.concat([type_df, wine_df],ignore_index=True, sort=False).iloc[:,:4]
    cov_df = cov_df[cov_df['GenericLocation'] == 'Restaurant']
    cov_df = cov_df[cov_df['SiteName'] == site]
    covers = group_covers_df(cov_df,bounds,current_column,last_col,vs_col,'GenericLocation').iloc[:,:4]
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


def breakdown_general_df(df,bounds,current_column,last_col,vs_col,oncolumn,func):
    df = date_filtering(df,bounds,current_column,last_col,vs_col,oncolumn,func)
    return df.drop(index=len(df)-1)
    
def breakdown_revenue_df(df,bounds,current_column,last_col,vs_col,oncolumn):
    return breakdown_general_df(df,bounds,current_column,last_col,vs_col,oncolumn,group_revenue_by_site)

def breakdown_covers_df(df,bounds,current_column,last_col,vs_col,oncolumn):
    return breakdown_general_df(df,bounds,current_column,last_col,vs_col,oncolumn,group_covers_by_site)

def breakdown_spend_df(rev_df,cov_df,bounds,current_column,last_col,vs_col,oncolumn):
    
    return spend_df(
        breakdown_revenue_df(rev_df,bounds,current_column,last_col,vs_col,oncolumn),
        breakdown_covers_df(cov_df,bounds,current_column,last_col,vs_col,oncolumn),
        oncolumn,
        current_column,
        last_col,
        vs_col
    )

def final_dataframe_week(df_tw, df_lw, df_ly, on_columns, current_column, last_col, vs_col):
    
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
    df['vs. LY %'] = (df['vs. LY'].replace(0,1) / df['Last Year'].replace(0,1))
    return df

def date_filtering_week(df,bounds,current_column,last_col,vs_col,on_columns,func):

    mask1 = df['Date'] <= bounds[0]
    mask2 = df['Date'] >= bounds[1]
    mask3 = df['Date'] <= bounds[2]
    mask4 = df['Date'] >= bounds[3]
    mask5 = df['Date'] <= bounds[4]
    mask6 = df['Date'] >= bounds[5]

    df_tw = func(df[mask1 & mask2])
    df_lw = func(df[mask3 & mask4])
    df_ly = func(df[mask5 & mask6])

    return final_dataframe_week(df_tw, df_lw, df_ly, on_columns, current_column, last_col, vs_col)

def spend_df_week(rev_df,cov_df,on_columns,current_column,last_col,vs_col):
    
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
    df['vs. LY %'] = (df['vs. LY'].replace(0,1) / df['Last Year'].replace(0,1))
    
    return df[on_columns + [current_column,last_col,'Last Year',vs_col,vs_col + ' %','vs. LY','vs. LY %']]

def group_by_session_day(df,measure):
    df_cols = ['Session','Day', measure]
    groupby_cols = df_cols[:-1]
    return df[df_cols].groupby(groupby_cols).sum().reset_index()
    
def group_revenue_by_session_day(df):
    return group_by_session_day(df, 'Revenue')

def group_covers_by_session_day(df):
    return group_by_session_day(df, 'Covers')

def sort_by_session_day(df):
    
    df = df[df['Session'].isin(['Lunch','Dinner'])].copy()
    session_sorter = ['Lunch','Dinner']
    day_sorter = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    df['Session'] = df['Session'].astype("category")
    df['Session'].cat.set_categories(session_sorter, inplace=True)
    df['Day'] = df['Day'].astype("category")
    df['Day'].cat.set_categories(day_sorter, inplace=True)
    return df[df['Session'].isin(['Lunch','Dinner'])].sort_values(by=['Session','Day'])

def week_general_df(site,df,bounds,current_column,last_col,vs_col,on_columns,func):
    if site=='Group':
        df = df
    else:
        df = df[df['SiteName'] == site]
    return sort_by_session_day(date_filtering_week(df,bounds,current_column,last_col,vs_col,on_columns,func))
                
def week_revenue_df(site,category,df,bounds,day_df,current_column,last_col,vs_col,on_columns):
    if category == 'Beverage' or category == 'Food':
        df = df[df['RevenueType']==category]
    elif category == 'Wine' or category == 'Non-Wine':
        mask1 = df['RevenueType']=='Beverage'
        mask2 = df['Wine'] == category
        df = df[mask1 & mask2]
    return pd.merge(
        week_general_df(site,df,bounds,current_column,last_col,vs_col,on_columns,group_revenue_by_session_day), 
        day_df,
        how='left',
        on='Day',
        suffixes = ('',' Count')
    )

def week_covers_df(site,df,bounds,day_df,current_column,last_col,vs_col,on_columns):
    return pd.merge(
        week_general_df(site,df,bounds,current_column,last_col,vs_col,on_columns,group_covers_by_session_day), 
        day_df,
        how='left',
        on='Day',
        suffixes = ('',' Count')
    )

def week_spend_df(site,category,rev_df,cov_df,bounds,day_df,current_column,last_col,vs_col,on_columns):
    
    return spend_df_week(
        week_revenue_df(site,category,rev_df,bounds,day_df,current_column,last_col,vs_col,on_columns),
        week_covers_df(site,cov_df,bounds,day_df,current_column,last_col,vs_col,on_columns),
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
    return df[df['SiteName'].isin(user_restaurants[auth._username][‘sales’)]


# Tracker Functions

def tracker_group_df(df):

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
        df['vs. LW %'] = (df['vs. LW'].replace(0,1) / abs(df['Last Week'].replace(0,1)))
        df['vs. LY'] = df['This Week'] - df['Last Year']
        df['vs. LY %'] = (df['vs. LY'].replace(0,1)  / abs(df['Last Year'].replace(0,1)))

        return df   
        
    df=df[df['Restaurant']!='Modern Pantry']
    df_columns = list(df.columns)[1:]
    groupby_columns = df_columns[:2]
    return add_comparison_columns(group_sort_columns(df[df_columns].groupby(groupby_columns).sum().reset_index()))

def tracker_user_site_filter(df):
    return df[df['Restaurant'].isin(user_restaurants[auth._username][‘bookings’])]

def tracker_site_filter(df, site):
    return df[df['Restaurant']==site]

def tracker_week_filter(df, week):
    return df[df['Week']==week]

def tracker_day_filter(df, graph_type):
    return df[df['Day'] == 'Full Week'] if graph_type == '8 Week' else df[df['Day'] != 'Full Week'] 
    
    
# Booking Trends Functions

def trends_table_filter(df, table):
    return df[df['Table']==table]

def trends_site_filter(df, site):
    return df[df['Restaurant'] == 'Group'] if site=='Group' else df[df['Restaurant']!='Group']
