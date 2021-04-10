from datetime import date, datetime, timedelta

# Date Functions 
def get_week(date):
    return date.isocalendar()[1]

def get_weekdaynum(date):
    return date.isocalendar()[2]

def get_year(date):
    return date.isocalendar()[0]

def days_ago(date, days):
    return date - timedelta(days)

def onedayago(date):
    return days_ago(date, 1)

def weeks_ago(date, weeks):
    return date - timedelta(7*weeks)

def oneweekago(date):
    return weeks_ago(date, 1)

def fourweeksago(date):
    return weeks_ago(date, 4)

def years_ago(date, years):
    return date - timedelta(364*years)

def oneyearago(date):
#     return years_ago(date, 1)
    return years_ago(date, 2)

def twelvemonthsago(date):
    if date.month==2 and date.day==29:
#         return (date-timedelta(1)).replace(year=date.year-1)
        return (date-timedelta(1)).replace(year=date.year-2)
        
    else:
#         return date.replace(year=date.year-1) 
        return date.replace(year=date.year-2) 

def first_day_of_week(date):
    return date - timedelta(get_weekdaynum(date)-1)

def first_day_of_month(date):
    return date.replace(day=1)

today = date.today()
yesterday = onedayago(today)

# Defining date bounds of the different sales reports for subsequent filtering into the sales report dataframes

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

four_weeks_upper = yesterday
four_weeks_lower = fourweeksago(yesterday)
four_weeks_upper_lw = oneweekago(four_weeks_upper)
four_weeks_lower_lw = oneweekago(four_weeks_lower)
four_weeks_upper_ly = oneyearago(four_weeks_upper)
four_weeks_lower_ly = oneyearago(four_weeks_lower)

def bound_filtering(df, bounds):
    
    mask1 = df['Date'] <= bounds[0]
    mask2 = df['Date'] >= bounds[1]
    mask3 = df['Date'] <= bounds[2]
    mask4 = df['Date'] >= bounds[3]
    mask5 = df['Date'] <= bounds[4]
    mask6 = df['Date'] >= bounds[5]
    return df[(mask1 & mask2) | (mask3 & mask4) | (mask5 & mask6)]

daily_bounds = [
    daily_upper,
    daily_lower,
    daily_upper_lw,
    daily_lower_lw,
    daily_upper_ly,
    daily_lower_ly,
]

wtd_bounds = [
    wtd_upper,
    wtd_lower,
    wtd_upper_lw,
    wtd_lower_lw,
    wtd_upper_ly,
    wtd_lower_ly,
]

mtd_bounds = [
    mtd_upper,
    mtd_lower,
    mtd_upper_lw,
    mtd_lower_lw,
    mtd_upper_ly,
    mtd_lower_ly,
]

weekly_bounds = [
    weekly_upper,
    weekly_lower,
    weekly_upper_lw,
    weekly_lower_lw,
    weekly_upper_ly,
    weekly_lower_ly,
]

monthly_bounds = [
    monthly_upper,
    monthly_lower,
    monthly_upper_lw,
    monthly_lower_lw,
    monthly_upper_ly,
    monthly_lower_ly,
]

four_weeks_bounds = [
    four_weeks_upper,
    four_weeks_lower,
    four_weeks_upper_lw,
    four_weeks_lower_lw,
    four_weeks_upper_ly,
    four_weeks_lower_ly,
]

all_bounds = [
    daily_bounds, 
    wtd_bounds, 
    mtd_bounds, 
    weekly_bounds, 
    monthly_bounds,
    four_weeks_bounds,
]

date_bounds = {
    'daily':daily_bounds,
    'wtd':wtd_bounds,
    'mtd':mtd_bounds,
    'weekly':weekly_bounds,
    'monthly':monthly_bounds,
    'four_weeks':four_weeks_bounds,
}

date_columns = {
    'current':{
        'daily':'Today',
        'wtd':'This Week',
        'weekly':'This Week',
        'mtd':'This Month',
        'monthly':'This Month',
        'four_weeks':'This Month',
    },
    'last':{
        'daily':'Last Week',
        'wtd':'Last Week',
        'weekly':'Last Week',
        'mtd':'Last Month',
        'monthly':'Last Month',
        'four_weeks':'Last Month',
    },    
    'vs':{
        'daily':'vs. LW',
        'wtd':'vs. LW',
        'weekly':'vs. LW',
        'mtd':'vs. LM',
        'monthly':'vs. LM',
        'four_weeks':'vs. LM',
    },   
    'curr_abbr':{
        'daily':'TW',
        'wtd':'TW',
        'weekly':'TW',
        'mtd':'TM',
        'monthly':'TM',
        'four_weeks':'TM',
    },      
    'last_abbr':{
        'daily':'LW',
        'wtd':'LW',
        'weekly':'LW',
        'mtd':'LM',
        'monthly':'LM',
        'four_weeks':'LM',
    },         
    'p_abbr':{
        'daily':'LW%',
        'wtd':'LW%',
        'weekly':'LW%',
        'mtd':'LM%',
        'monthly':'LM%',
        'four_weeks':'LM%',
    },
    'color_scale':{
        'daily':[[0,'DarkSlateBlue'],[.5,'Linen'],[1,'GhostWhite']],
        'wtd':[[0,'DarkViolet'],[.5,'Linen'],[1,'GhostWhite']],
        'weekly':[[0,'MediumOrchid'],[.5,'Linen'],[1,'GhostWhite']],
        'mtd':[[0,'Orange'],[.5,'Linen'],[1,'GhostWhite']],
        'monthly':[[0,'DarkOrange'],[.5,'Linen'],[1,'GhostWhite']],
        'four_weeks':[[0,'DarkRed'],[.5,'Linen'],[1,'GhostWhite']],
    },
}