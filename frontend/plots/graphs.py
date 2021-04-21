from data.data import sales_dataframes, tracker_df, reviews_dff, future_breakdown_df
from data.functions import *
from data.date_bounds import date_bounds, date_columns
from data.day_counts import day_counts
from frontend.plots.figures import *
from frontend.styling import *
import numpy as np

def sales_breakdown_graph(
    shift,
    area,
    measure,
    metric,
    report
):
    
    rev_df = sales_dataframes[report]['revenue']
    cov_df = sales_dataframes[report]['covers']
    
    bounds = date_bounds[report]
    current_col = date_columns['current'][report]
    last_col = date_columns['last'][report]
    vs_col = date_columns['vs'][report]
    
    change_col, base_col = (vs_col, last_col) if metric in [vs_col, 'Totals ' + last_col] else ('vs. LY', 'Last Year')
    on_column = 'SiteName'
    
    if measure == 'Revenue':
        rev_dff = user_site_filter(shift_filter(area_filter(rev_df, area),shift))
        dff = breakdown_revenue_df(rev_dff,bounds,current_col,last_col,vs_col,on_column).sort_values(by=on_column, ascending=False)
    
    elif measure == 'Covers':
        cov_dff = user_site_filter(shift_filter(area_filter(cov_df, area),shift))
        dff = breakdown_covers_df(cov_dff,bounds,current_col,last_col,vs_col,on_column).sort_values(by=on_column, ascending=False)
    
    if measure == "Spend":
        rev_dff = user_site_filter(shift_filter(area_filter(rev_df, area),shift))
        cov_dff = user_site_filter(shift_filter(area_filter(cov_df, area),shift))
        dff = breakdown_spend_df(rev_dff,cov_dff,bounds,current_col,last_col,vs_col,on_column).sort_values(by=on_column, ascending=False)
        
    total_template = templates['Sales Breakdown'][measure]['Total']
    change_template = templates['Sales Breakdown'][measure]['Change']
    
    color_current = total_colors[measure]['Current']
    color_last = total_colors[measure]['Last']
    
    
    title_string = capitalize_report_title(report)
    if area == 'Full Site':
        title = title_string + ' ' + measure + ' ' + metric
    else:
        title = title_string + ' ' + area + ' ' + measure + ' ' + metric
    
    if 'vs.' in metric:
        return sales_breakdown_change_figure(dff, title, change_template, current_col, change_col, base_col) 
    else:
        return sales_breakdown_totals_figure(dff, title, total_template, color_last, color_current, current_col, change_col, base_col)
    
def sales_group_revenue_graph(
    shift,
    metric,
    report
):
    
#     Logic to convert summary page week metrics from metric input to month metrics
    if report == 'mtd':
        if metric == 'vs. LW':
            metric = 'vs. LM'
        elif metric == 'Last Week':
            metric = 'Last Month'
    
    df = sales_dataframes[report]['revenue']

    bounds = date_bounds[report]
    current_col = date_columns['current'][report]
    last_col = date_columns['last'][report]
    vs_col = date_columns['vs'][report]
    
    change_col, base_col = ('vs. LY', 'Last Year') if metric in ['vs. LY', 'Totals Last Year'] else (vs_col, last_col)
    on_column = 'GenericLocation'
    measure = 'Revenue'
    
    rev_dff = user_site_filter(shift_filter(df, shift))
    dff = group_revenue_df(rev_dff,bounds,current_col,last_col,vs_col,on_column)
    
    total_template = templates['Sales'][measure]['Total']
    change_template = templates['Sales'][measure]['Change']
    
    color_current = total_colors[measure]['Current']
    color_last = total_colors[measure]['Last']
    
    title_string = capitalize_report_title(report)
    title = title_string + ' Group Revenue ' + metric
    
    if 'vs.' in metric:
        return sales_change_figure(dff,on_column,change_template,title,measure,current_col,change_col,base_col)
    else:
        return sales_totals_figure(dff,on_column,color_current,color_last,total_template,title,measure,current_col,change_col,base_col)

def sales_group_covers_graph(
    shift,
    metric,
    report
):
    
    df = sales_dataframes[report]['covers']

    bounds = date_bounds[report]
    current_col = date_columns['current'][report]
    last_col = date_columns['last'][report]
    vs_col = date_columns['vs'][report]
    
    change_col, base_col = (vs_col, last_col) if metric in [vs_col, 'Totals ' + last_col] else ('vs. LY', 'Last Year')
    on_column = 'GenericLocation'
    measure = 'Covers'
    
    cov_dff = user_site_filter(shift_filter(df, shift))
    dff = group_covers_df(cov_dff,bounds,current_col,last_col,vs_col,on_column)
    
    total_template = templates['Sales'][measure]['Total']
    change_template = templates['Sales'][measure]['Change']
    
    color_current = total_colors[measure]['Current']
    color_last = total_colors[measure]['Last']
    
    title_string = capitalize_report_title(report)
    title = title_string + ' Group Covers ' + metric
    
    if 'vs.' in metric:
        return sales_change_figure(dff,on_column,change_template,title,measure,current_col,change_col,base_col)
    else:
        return sales_totals_figure(dff,on_column,color_current,color_last,total_template,title,measure,current_col,change_col,base_col)

def sales_group_spend_graph(
    shift,
    metric,
    report
):
    
    rev_df = sales_dataframes[report]['revenue']
    cov_df = sales_dataframes[report]['covers']

    bounds = date_bounds[report]
    current_col = date_columns['current'][report]
    last_col = date_columns['last'][report]
    vs_col = date_columns['vs'][report]
    
    change_col, base_col = (vs_col, last_col) if metric in [vs_col, 'Totals ' + last_col] else ('vs. LY', 'Last Year')
    on_column = 'GenericLocation'
    measure = 'Spend'
    
    rev_dff = user_site_filter(shift_filter(rev_df,shift))
    cov_dff = user_site_filter(shift_filter(cov_df,shift))
    dff = group_spend_df(rev_dff,cov_dff,bounds,current_col,last_col,vs_col,on_column)
        
    total_template = templates['Sales'][measure]['Total']
    change_template = templates['Sales'][measure]['Change']
    
    color_current = total_colors[measure]['Current']
    color_last = total_colors[measure]['Last']
    
    title_string = capitalize_report_title(report)
    title = title_string + ' Group Restaurant Spend ' + metric
    
    if 'vs.' in metric:
        return sales_change_figure(dff,'RevenueType',change_template,title, measure,current_col,change_col,base_col)
    else:
        return sales_totals_figure(dff,'RevenueType',color_current,color_last,total_template,title,measure,current_col,change_col,base_col)
      
def sales_site_revenue_graph(
    shift,
    metric,
    site,
    report
):
    
    df = sales_dataframes[report]['revenue']

    bounds = date_bounds[report]
    current_col = date_columns['current'][report]
    last_col = date_columns['last'][report]
    vs_col = date_columns['vs'][report]
    
    change_col, base_col = (vs_col, last_col) if metric in [vs_col, 'Totals ' + last_col] else ('vs. LY', 'Last Year')
    on_column = 'LocationName'
    measure = 'Revenue'
    
    rev_dff = shift_filter(df, shift)
    dff = site_revenue_df(site,rev_dff,bounds,current_col,last_col,vs_col,on_column)
    
    total_template = templates['Sales'][measure]['Total']
    change_template = templates['Sales'][measure]['Change']
    
    color_current = total_colors[measure]['Current']
    color_last = total_colors[measure]['Last']
    
    title_string = capitalize_report_title(report)    
    title = title_string + ' Revenue ' + metric
    
    if 'vs.' in metric:
        return sales_change_figure(dff,on_column,change_template,title,measure,current_col,change_col,base_col)
    else:
        return sales_totals_figure(dff,on_column,color_current,color_last,total_template,title,measure,current_col,change_col,base_col)

def sales_site_covers_graph(
    shift,
    metric,
    site,
    report
):
    
    df = sales_dataframes[report]['covers']

    bounds = date_bounds[report]
    current_col = date_columns['current'][report]
    last_col = date_columns['last'][report]
    vs_col = date_columns['vs'][report]
    
    change_col, base_col = (vs_col, last_col) if metric in [vs_col, 'Totals ' + last_col] else ('vs. LY', 'Last Year')
    on_column = 'LocationName'
    measure = 'Covers'
    
    cov_dff = shift_filter(df, shift)
    dff = site_covers_df(site,cov_dff,bounds,current_col,last_col,vs_col,on_column)
    
    total_template = templates['Sales'][measure]['Total']
    change_template = templates['Sales'][measure]['Change']
    
    color_current = total_colors[measure]['Current']
    color_last = total_colors[measure]['Last']
    
    title_string = capitalize_report_title(report)    
    title = title_string + ' Covers ' + metric
    
    if 'vs.' in metric:
        return sales_change_figure(dff,on_column,change_template,title,measure,current_col,change_col,base_col)
    else:
        return sales_totals_figure(dff,on_column,color_current,color_last,total_template,title,measure,current_col,change_col,base_col)
    
def sales_site_spend_graph(
    shift,
    metric,
    site,
    report
):
    
    rev_df = sales_dataframes[report]['revenue']
    cov_df = sales_dataframes[report]['covers']

    bounds = date_bounds[report]
    current_col = date_columns['current'][report]
    last_col = date_columns['last'][report]
    vs_col = date_columns['vs'][report]
    
    change_col, base_col = (vs_col, last_col) if metric in [vs_col, 'Totals ' + last_col] else ('vs. LY', 'Last Year')
    on_column = 'LocationName'
    measure = 'Spend'
    
    rev_dff = shift_filter(rev_df,shift)
    cov_dff = shift_filter(cov_df,shift)
    dff = site_spend_df(site,rev_dff,cov_dff,bounds,current_col,last_col,vs_col,on_column)
    
    total_template = templates['Sales'][measure]['Total']
    change_template = templates['Sales'][measure]['Change']
    
    color_current = total_colors[measure]['Current']
    color_last = total_colors[measure]['Last']
    
    title_string = capitalize_report_title(report)    
    title = title_string + ' Restaurant Spend ' + metric
    
    if 'vs.' in metric:
        return sales_change_figure(dff,'RevenueType',change_template,title,measure,current_col,change_col,base_col)
    else:
        return sales_totals_figure(dff,'RevenueType',color_current,color_last,total_template,title,measure,current_col,change_col,base_col)
       
def sales_week_view_graph(
    site,
    area,
    category,
    measure,
    metric,
    weekmetric,
    report
):
    
    rev_df = sales_dataframes[report]['revenue']
    cov_df = sales_dataframes[report]['covers']

    bounds = date_bounds[report]
    current_col = date_columns['current'][report]
    last_col = date_columns['last'][report]
    vs_col = date_columns['vs'][report]
    day_df = day_counts[report]
    
    change_col, base_col = (vs_col, last_col) if metric in [vs_col, 'Totals ' + last_col] else ('vs. LY', 'Last Year')
    on_columns = ['Session','Day']
    
    if measure == 'Revenue':
        
        rev_dff = area_filter(site_filter(rev_df, site),area)
        dff = week_revenue_df(site,category,rev_dff,bounds,day_df,current_col,last_col,vs_col,on_columns)
        
        if weekmetric == 'Averages':
            y_last = dff[base_col]/(dff[base_col + ' Count'])
            y_current = dff[current_col]/(dff[current_col + ' Count'])
            y = dff[change_col]/(dff[base_col + ' Count'])
        else:
            y_last = dff[base_col]
            y_current = dff[current_col]
            y = dff[change_col]            

    if measure == 'Spend':
        
        rev_dff = area_filter(site_filter(rev_df, site),area)
        cov_dff = area_filter(site_filter(cov_df, site),area)
        dff = week_spend_df(site,category,rev_dff,cov_dff,bounds,day_df,current_col,last_col,vs_col,on_columns)
        
        y_last = dff[base_col]
        y_current = dff[current_col]
        y = dff[change_col]
    
    total_template = templates['Sales'][measure]['Total']
    change_template = templates['Sales'][measure]['Change']
    
    color_current = dff['Session'].apply(lambda x:week_colors_totals(measure, x,'Current'))
    color_last = dff['Session'].apply(lambda x:week_colors_totals(measure, x,'Last'))
        
    title = site + "  " + area + "  " + category + " " + measure + "  " + metric
    customdata = dff[change_col + ' %']
        
    if 'vs.' in metric:
        return sales_week_change_figure(dff, y, change_template, title, measure, change_col)
    else:
        return sales_week_totals_figure(dff, y_last, y_current, color_last, color_current, total_template, title, measure, current_col, base_col)

def sales_week_covers_graph(
    site,
    area,
    measure,
    metric,
    weekmetric,
    report
):
    
    cov_df = sales_dataframes[report]['covers']

    bounds = date_bounds[report]
    current_col = date_columns['current'][report]
    last_col = date_columns['last'][report]
    vs_col = date_columns['vs'][report]
    day_df = day_counts[report]
    
    change_col, base_col = (vs_col, last_col) if metric in [vs_col, 'Totals ' + last_col] else ('vs. LY', 'Last Year')
    on_columns = ['Session','Day']
    measure = 'Covers'
    
    cov_dff = area_filter(site_filter(cov_df, site),area)
    dff = week_covers_df(site,cov_dff,bounds,day_df,current_col,last_col,vs_col,on_columns)
    
    title = site + "  " + area + "  " + measure + "  " + metric
    customdata = dff[change_col + ' %']
    
    total_template = templates['Sales'][measure]['Total']
    change_template = templates['Sales'][measure]['Change']
    
    color_current = dff['Session'].apply(lambda x:week_colors_totals(measure, x,'Current'))
    color_last = dff['Session'].apply(lambda x:week_colors_totals(measure, x,'Last'))
    
    if weekmetric == 'Averages':
        y_last = dff[base_col]/(dff[base_col + ' Count'])
        y_current = dff[current_col]/(dff[current_col + ' Count'])
        y = dff[change_col]/(dff[base_col + ' Count'])
    else:
        y_last = dff[base_col]
        y_current = dff[current_col]
        y = dff[change_col] 
        
    if 'vs.' in metric:
        return sales_week_change_figure(dff, y, change_template, title, measure, change_col)
    else:
        return sales_week_totals_figure(dff, y_last, y_current, color_last, color_current, total_template, title, measure, current_col, base_col)
    
    
# Tracker Graphs

def tracker_group_8_weeks_graph(week, metric ,site, df, measure):
    
    dff = tracker_day_filter(
        tracker_group_df(
            tracker_user_site_filter(
                df
            )
        ), '8 Week'
    )
    
    x = dff['Week']
    graph = 'Next 16 Weeks - Group ' + measure
    
    if 'vs.' in metric:
        return tracker_change_figure(dff, x, metric, graph, measure)
    else:
        metric = metric.replace('Totals ', '')
        return tracker_totals_figure(dff, x, metric, graph, measure)
    
def tracker_group_week_graph(week, metric, site, df, measure):

    dff = tracker_week_filter(
        tracker_day_filter(
            tracker_group_df(
                tracker_user_site_filter(
                    df
                )
            ), 'Weekly'
        ), week
    )
    
    x = dff['Day']
    graph = week + ' - Group ' + measure
    
    if 'vs.' in metric:
        return tracker_change_figure(dff, x, metric, graph, measure)
    else:
        metric = metric.replace('Totals ', '')
        return tracker_totals_figure(dff, x, metric, graph, measure)
    
def tracker_site_8_weeks_graph(week, metric, site, df, measure):
    
    dff = tracker_day_filter(
        tracker_site_filter(
            df, site
        ), '8 Week'
    )
    
    x = dff['Week']
    graph = 'Next 16 Weeks - ' + measure
    
    if 'vs.' in metric:
        return tracker_change_figure(dff, x, metric, graph, measure)
    else:
        metric = metric.replace('Totals ', '')
        return tracker_totals_figure(dff, x, metric, graph, measure)
    
def tracker_site_week_graph(week, metric, site, df, measure):
    
    dff = tracker_week_filter(
        tracker_day_filter(
            tracker_site_filter(
                df, site
            ), 'Weekly'
        ),week
    )

    x = dff['Day']
    graph = week + ' - ' + measure
    
    if 'vs.' in metric:
        return tracker_change_figure(dff, x, metric, graph, measure)
    else:
        metric = metric.replace('Totals ', '')
        return tracker_totals_figure(dff, x, metric, graph, measure)
    
def tracker_breakdown_graph(week, metric, site, df, measure):
    
    dff = tracker_week_filter(
        tracker_day_filter(
            tracker_user_site_filter(
                df
            ), '8 Week'
        ),week
    ).sort_values(by='Restaurant',ascending=False)
    
    graph = week + ' ' + measure
            
    if 'vs.' in metric:
        return tracker_breakdown_change_figure(dff, metric, graph, measure)
    else:
        metric = metric.replace('Totals ', '')
        return tracker_breakdown_totals_figure(dff, metric, graph, measure)

def score_graph(site, category):
    
    df = reviews_dff
    
    weeks_ago = 8
    df = df[df.weeks_ago >= -weeks_ago]
    
    if site == 'Group':
        dff = bookings_user_site_filter(df)
    else:
        dff = bookings_site_filter(df, site)
        
    df_columns = ['weeks_ago','weeks','overall','food','service','ambience','value']
    groupby_columns = ['weeks_ago','weeks']
    
    counts = dff[df_columns].groupby(groupby_columns).count().reset_index()
    scores = dff[df_columns].groupby(groupby_columns).mean().reset_index()

    dff = pd.merge(scores, counts, on=['weeks_ago','weeks'], suffixes=('','_count'))
    
    weeks_ago_list = [x for x in range(-weeks_ago,0)]
    week_labels_list = [str(-x) + ' Weeks Ago' for x in range(-weeks_ago,-1)] + ['Last Week']

    data_dict = {
        'weeks_ago':weeks_ago_list,
        'weeks':week_labels_list
    }

    skeleton_df = pd.DataFrame(data=data_dict)

    final_df = pd.merge(skeleton_df, dff, how='left')
    
    return score_figure(final_df, category)

def score_breakdown_graph(category):
    
    review_restaurants = bookings_breakdown_user_site_filter([
        '100 Wardour St',
        '14 Hills',
        '20 Stories',
        'Angelica',
        'Angler',
        'Aster',
        'Avenue',
        'Bluebird Chelsea',
        'Bluebird London NYC',
        'Bluebird White City',
        'Blueprint Café',
        'Butlers Wharf Chophouse',
        'Cantina del Ponte',
        "Coq d'Argent",
        'Crafthouse',
        'D & D London Ltd',
        'East 59th',
        'Fish Market',
        'Fiume',
        'German Gymnasium',
        'Issho',
        'Klosterhaus',
        'Launceston Place',
        'Le Pont de la Tour',
        'Madison',
        'New Street Grill',
        'Old Bengal Bar',
        'Orrery',
        'Paternoster Chophouse',
        'Plateau',
        "Quaglino's",
        'Radici',
        'Royal Exchange Grand Café',
        'Sartoria',
        'Skylon',
        'South Place Chop House',
        'The Den',
        'The Modern Pantry',
        'queensyard'
    ])
    
    df = reviews_dff
    
    weeks_ago = 4
    dff = bookings_user_site_filter(df[df.weeks_ago >= -weeks_ago]) 
        
    df_columns = ['restaurant','overall','food','service','ambience','value']
    groupby_columns = ['restaurant']
    
    counts = dff[df_columns].groupby(groupby_columns).count().reset_index()
    scores = dff[df_columns].groupby(groupby_columns).mean().reset_index()

    dff = pd.merge(scores, counts, on='restaurant', suffixes=('','_count'))

    skeleton_df = pd.DataFrame(data={'restaurant':review_restaurants})
    final_df = pd.merge(skeleton_df, dff, how='left')
    
    return score_breakdown_figure(final_df, category)

def future_breakdown_graph(week):
    
    df = future_breakdown_df
    dff = bookings_user_site_filter(df[df['weeks']==week]).sort_values(by='restaurant',ascending=False)
    
    return future_breakdown_figure(dff, week)

# Homepage

def homepage_future_graph(graph, site):
    
    df = future_breakdown_df
    weeks_ahead = 4
    dff = df[df.weeks_ahead < weeks_ahead]
    
    groupby_columns = ['weeks_ahead','weeks']
    
    if site == 'Group':
        dff = bookings_user_site_filter(dff)
    else:
        dff = bookings_site_filter(dff, site)
    
    df_columns = groupby_columns + ['capacity','max_guests TW', 'empty']
    df = dff[df_columns].groupby(groupby_columns).sum().reset_index()
    
    df['full'] = (df['max_guests TW']/df.capacity).replace(np.inf, np.nan).fillna(0)
    
    if graph == 'summary':
    
        sums = df[['capacity','max_guests TW','empty']].sum()
        capacity = sums[0]
        covers = sums[1]
        empty = capacity-covers
        full = covers/capacity

        return homepage_future_summary_figure(covers, empty, full, site)
    
    elif graph == 'worst':
        
        if site == 'Group':
            
            dff = df.sort_values('full', ascending=False).tail(5)
            
        else:
            
            week_nums = [0,1,2,3]
            week_labels = ['This Week','Next Week','2 Weeks Ahead', '3 Weeks Ahead']

            skeleton_df = pd.DataFrame(data = {'weeks_ahead':week_nums,'weeks':week_labels})

            dff = pd.merge(skeleton_df, df, how = 'left')
            dff = dff.sort_values('weeks_ahead', ascending=False)
        
        return homepage_future_worst_figure(dff, site)
    
    elif graph == 'breakdown':
        
        week_nums = [0,1,2,3]
        week_labels = ['This Week','Next Week','2 Weeks Ahead', '3 Weeks Ahead']

        skeleton_df = pd.DataFrame(data = {'weeks_ahead':week_nums,'weeks':week_labels})

        dff = pd.merge(skeleton_df, df, how = 'left')
        dff['full'] = (dff['max_guests TW']/dff.capacity).replace(np.inf, np.nan).fillna(0)
        
        return homepage_future_weeks_figure(dff, site)

def homepage_tracker_graph(graph, site):
    
    df = tracker_df
    mask1 = df['Week'].isin(['This Week','Next Week','Two Weeks','Three Weeks'])
    mask2 = df['Day'] == 'Full Week'
    dff = df[mask1 & mask2]
    
    if site == 'Group':
        dff = map_bookings_to_sales_restaurants(tracker_user_site_filter(dff))
    else:
        dff = map_bookings_to_sales_restaurants(tracker_site_filter(dff, site))
        
    if graph == 'sites':
        groupby_columns = ['Restaurant']
    else:
        groupby_columns = ['Week']

    df_columns = groupby_columns + ['This Week','Last Week','Last Year']
    df = dff[df_columns].groupby(groupby_columns).sum().reset_index()
   
    df['vs. LY'] = df['This Week'] - df['Last Year']
    df['vs. LY %'] = (df['vs. LY'] / df['Last Year']).replace(np.inf, np.nan).fillna(0)
    
    if graph == 'summary':
        
        sums = df[['This Week','Last Week','Last Year']].sum()
        thisyear = sums[0]
        lastyear = sums[2]
        pchange = ((thisyear - lastyear) / lastyear)*100
        
        return homepage_summary_figure(thisyear, lastyear, pchange, 'Covers', site)
    
    elif graph == 'worst':
        
        if site == 'Group':
            
            dff = df.sort_values('vs. LY %', ascending=False).tail(5)
            
        else:
            
            week_labels = ['This Week','Next Week','Two Weeks', 'Three Weeks'][::-1]

            skeleton_df = pd.DataFrame(data = {'Week':week_labels})

            dff = pd.merge(skeleton_df, df, how = 'left')
        
        return homepage_worst_figure(dff, 'Covers', site)
    
    elif graph == 'sites':
        
        dff = remove_false_ly_values(df.sort_values('Restaurant', ascending = False), 'Restaurant')
        
        return homepage_sites_figure(dff, 'Covers', site)
    
    elif graph == 'breakdown':
            
        week_labels = ['This Week','Next Week','Two Weeks', 'Three Weeks']
        skeleton_df = pd.DataFrame(data = {'Week':week_labels})
        dff = pd.merge(skeleton_df, df, how = 'left')
        
        return homepage_tracker_weeks_figure(dff, site)
        
        
    
def homepage_revenue_graph(graph, site):
    
    shift = 'All Shifts'
    area = 'All Locations'
    measure = 'Revenue'
    metric = 'vs. LY'
    report = 'four_weeks'

    bounds = date_bounds[report]
    current_col = date_columns['current'][report]
    last_col = date_columns['last'][report]
    vs_col = date_columns['vs'][report]
    change_col, base_col = (vs_col, last_col) if metric in [vs_col, 'Totals ' + last_col] else ('vs. LY', 'Last Year')
    
    if site == 'Group':
        
        on_column = 'SiteName'
        rev_df = user_site_filter(sales_dataframes[report]['revenue'])
        df = breakdown_revenue_df(rev_df,bounds,current_col,last_col,vs_col,on_column).sort_values(by=on_column, ascending=False)
        
    else:
        
        on_column = 'LocationName'
        rev_df = site_filter(sales_dataframes[report]['revenue'], site)
        df = site_revenue_df(site,rev_df,bounds,current_col,last_col,vs_col,on_column)

    
    if graph == 'summary':
        
        sums = df[['This Month','Last Month','Last Year']].sum()
        thisyear = sums[0]
        lastyear = sums[2]
        pchange = ((thisyear - lastyear) / lastyear)*100
        
        return homepage_summary_figure(thisyear, lastyear, pchange, 'Revenue', site)
    
    elif graph == 'worst':
        
        if site == 'Group':
            dff = df.sort_values('vs. LY %', ascending=False).tail(5)
        else:
            dff = df[df[on_column] != 'Total'].sort_values('vs. LY', ascending=False)
        
        return homepage_worst_figure(dff, 'Revenue', site)
    
    elif graph == 'sites':
        
        return homepage_sites_figure(df, 'Revenue', site)
    
    
    
    
def homepage_score_graph(graph, site):
    
    df = reviews_dff
    dff = df[df.weeks_ago > -5]
    
    if site == 'Group':
        dff = bookings_user_site_filter(dff)
    else:
        dff = bookings_site_filter(dff, site)
    
    if graph == 'summary':
        
        overall = dff['overall'].mean()
        
        return homepage_score_summary_figure(overall, site)
    
    elif graph == 'worst':
        
        if site == 'Group':
        
            df_columns = ['restaurant','overall']
            groupby_columns = 'restaurant'

            means = dff[df_columns].groupby(groupby_columns).mean().reset_index()
            counts = dff[df_columns].groupby(groupby_columns).count().reset_index()

            restaurants = pd.merge(means,counts,on='restaurant',suffixes=('','_count'), how='outer')
            df = restaurants.sort_values('overall', ascending=False).tail(5)
            
        else:
            
            df_columns = ['overall','food','service','ambience','value']

            means = dff[df_columns].mean().reset_index()
            counts = dff[df_columns].count().reset_index()

            df = pd.merge(means,counts,on='index',suffixes=('_score','_count'), how='outer')

            column_map = {
                'index':'category',
                '0_score':'score',
                '0_count':'count',
            }

            df = df.rename(columns=column_map)
        
        return homepage_score_worst_figure(df, site)
    
    elif graph == 'sites':
        
        df_columns = ['restaurant','overall']
        groupby_columns = 'restaurant'

        means = dff[df_columns].groupby(groupby_columns).mean().reset_index()
        counts = dff[df_columns].groupby(groupby_columns).count().reset_index()

        restaurants = pd.merge(means,counts,on='restaurant',suffixes=('','_count'), how='outer')
        df = restaurants.sort_values('restaurant', ascending=False)
        
    return homepage_score_figure(df, site)

def detail_sales_graph(graph, site):
    
    metric = 'vs. LY'
    report = 'four_weeks'

    bounds = date_bounds[report]
    current_col = date_columns['current'][report]
    last_col = date_columns['last'][report]
    vs_col = date_columns['vs'][report]
    change_col, base_col = (vs_col, last_col) if metric in [vs_col, 'Totals ' + last_col] else ('vs. LY', 'Last Year')
    
    if site == 'Group':
        
        rev_df = user_site_filter(sales_dataframes[report]['revenue'])
        on_column = 'GenericLocation'
        
        if graph == 'revenue':
            
            df = group_revenue_df(rev_df,bounds,current_column,last_col,vs_col,oncolumn)
            df = df[df.on_column != 'Total']
            
            return detail_sales_figure(df, on_column)
            
        elif graph == 'spend':
            
            cov_df = user_site_filter(sales_dataframes[report]['covers'])            
            df = group_spend_df(rev_df, cov_df, bounds, current_column,last_col,vs_col,oncolumn)
            df = df[df.on_column != 'Total'] 
            
            return detail_sales_figure(df, on_column)           
        
    else:
        
        rev_df = site_filter(sales_dataframes[report]['revenue'], site)
        on_column = 'LocationName'
        y_column = 'RevenueType'
        
        if graph == 'revenue':
            
            df = site_revenue_df(site,rev_df,bounds,current_col,last_col,vs_col,on_column)
            df = df[df.y_column != 'Total']
            
            return detail_sales_figure(df, y_column)
            
        elif graph == 'spend':
            
            cov_df = site_filter(sales_dataframes[report]['covers'], site)
            df = site_spend_df(site,rev_df,cov_df,bounds,current_column,last_col,vs_col,oncolumn)
            df = df[df.y_column != 'Total']
            
            return detail_sales_figure(df, y_column)
        
def detail_tracker_graph(site):
    
    df = tracker_df
    
    if site == 'Group':
        
        dff = tracker_day_filter(
            tracker_group_df(
                tracker_user_site_filter(
                    df)), '8 Week')
        
    else:
        
        dff = tracker_day_filter(
            tracker_site_filter(
                df, site), '8 Week')
        
    weeks_list = [
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

    skeleton = pd.DataFrame({'Week':weeks_list})

    df = pd.merge(skeleton, dff, how='left')
    
    return detail_tracker_figure(df)

def detail_future_graph(site):
    
    df = future_df
    today = datetime.now()
    
    def create_weeks_columns(df):

        def weeks_ahead(date):
            monday = date - timedelta(date.weekday())
            return floor(((monday - today).days)/7)+1

        def weeks_label(weeks_ahead):
            return 'This Week' if weeks_ahead == 0 else 'Next Week' if weeks_ahead == 1 else str(weeks_ahead) + ' Weeks Ahead'

        df['weeks_ahead'] = df['visit_day'].apply(weeks_ahead)
        df['weeks'] = df['weeks_ahead'].apply(weeks_label)

        return df
    
    if site == 'Group':
        df = bookings_user_site_filter(create_weeks_columns(df))
        df_columns = ['visit_day','shift','weeks_ahead','weeks','capacity','max_guests TW']
        
    else:
        df = bookings_site_filter(create_weeks_columns(df), site)
        df_columns = ['restaurant','visit_day','shift','weeks_ahead','weeks','capacity','max_guests TW']

        
    groupby_columns = df_columns[:-2]

    def reduce_minus(value):
        return 0 if value < 0 else value

    dff = df[df_columns].groupby(groupby_columns).sum().reset_index()
    dff['full'] = dff['max_guests TW']/dff['capacity']
    dff['empty'] = (dff['capacity']-dff['max_guests TW']).apply(reduce_minus)
    

def homepage_sales_table(report, measure):

    bounds = date_bounds[report]
    current_column = date_columns['current'][report]
    last_col = date_columns['last'][report]
    vs_col = date_columns['vs'][report]
    on_column = 'SiteName'
    
    rev_df = user_site_filter(sales_dataframes[report]['revenue'])
    cov_df = user_site_filter(sales_dataframes[report]['covers'])
    
    rev = breakdown_revenue_df(rev_df,bounds,current_column,last_col,vs_col,on_column).sort_values('SiteName')
    cov = breakdown_covers_df(cov_df,bounds,current_column,last_col,vs_col,on_column).sort_values('SiteName')
        
    rev_total = get_lfl_total_row(rev, 'SiteName')
    cov_total = get_lfl_total_row(cov, 'SiteName')
    spe_total = rev_total.set_index('SiteName').div(cov_total.set_index('SiteName'),level=[0]).reset_index()
    spe_total.iloc[:,6] = (spe_total.iloc[:,1]-spe_total.iloc[:,2])/spe_total.iloc[:,2]
    spe_total.iloc[:,7] = (spe_total.iloc[:,1]-spe_total.iloc[:,3])/spe_total.iloc[:,3]
    
    rev_total.iloc[:,0] = 'REV'
    cov_total.iloc[:,0] = 'COV'
    spe_total.iloc[:,0] = 'SPE'    
    
    if measure == 'Revenue':
    
        df = breakdown_revenue_df(rev_df,bounds,current_column,last_col,vs_col,on_column).sort_values('SiteName')
        dff = remove_false_ly_values(df, 'SiteName')
        
    elif measure == 'Covers':
        
        df = breakdown_covers_df(cov_df,bounds,current_column,last_col,vs_col,on_column).sort_values('SiteName')
        dff = remove_false_ly_values(df, 'SiteName')
        
    elif measure == 'Spend':
    
        rev_df = spend_type_filter(area_filter(user_site_filter(sales_dataframes[report]['revenue']), 'Restaurant'))
        cov_df = area_filter(user_site_filter(sales_dataframes[report]['covers']), 'Restaurant')
        df = breakdown_spend_df(rev_df,cov_df,bounds,current_column,last_col,vs_col,on_column).sort_values('SiteName')
        dff = remove_false_ly_values(df, 'SiteName')
        
#         rev = breakdown_revenue_df(spend_type_filter(area_filter(rev_df, 'Restaurant')),bounds,current_column,last_col,vs_col,on_column).sort_values('SiteName')
#         cov = breakdown_covers_df(area_filter(cov_df, 'Restaurant'),bounds,current_column,last_col,vs_col,on_column).sort_values('SiteName')
        
#         rev_total = get_lfl_total_row(rev, 'SiteName')
#         cov_total = get_lfl_total_row(cov, 'SiteName')
        
#         spe_total = rev_total.set_index('SiteName').div(cov_total.set_index('SiteName'),level=[0]).reset_index()
        
#         spe_total.iloc[:,6] = (spe_total.iloc[:,1]-spe_total.iloc[:,2])/spe_total.iloc[:,2]
#         spe_total.iloc[:,7] = (spe_total.iloc[:,1]-spe_total.iloc[:,3])/spe_total.iloc[:,3]
                
    dff = rev_total.append([cov_total,spe_total,dff], ignore_index=True)
        
    return sales_heatmap_figure(dff, report, measure)