from data.data import *
from plots.figures import *
from display.styling import *

change_metrics = [
    'vs. LW', 
    'vs. LM', 
    'vs. LY'
]

def sales_breakdown_graph(
    shift,
    area,
    measure,
    metric,
    rev_df,
    cov_df, 
    bounds,
    current_col,
    last_col,
    vs_col
):

    change_col, base_col = (vs_col, last_col) if metric in [vs_col, last_col] else ('vs. LY', 'Last Year')
    on_column = 'SiteName'
    
    if measure == 'Revenue':
        rev_dff = user_site_filter(shift_filter(area_filter(rev_df, area),shift))
        dff = Breakdown_Revenue(rev_dff,bounds,current_col,last_col,vs_col,on_column).sort_values(by=on_column, ascending=False)
    
    elif measure == 'Covers':
        cov_dff = user_site_filter(shift_filter(area_filter(cov_df, area),shift))
        dff = Breakdown_Covers(cov_dff,bounds,current_col,last_col,vs_col,on_column).sort_values(by=on_column, ascending=False)
    
    if measure == "Spend":
        rev_dff = user_site_filter(shift_filter(area_filter(rev_df, area),shift))
        cov_dff = user_site_filter(shift_filter(area_filter(cov_df, area),shift))
        dff = Breakdown_Spend(rev_dff,cov_dff,bounds,current_col,last_col,vs_col,on_column).sort_values(by=on_column, ascending=False)
        
    total_template = templates['Sales Breakdown'][measure]['Total']
    change_template = templates['Sales Breakdown'][measure]['Change']
    
    color_current = total_colors[measure]['Current']
    color_last = total_colors[measure]['Last']
    
    title = area + ' ' + measure + ' ' + metric
    
    if metric in change_metrics:
        return sales_breakdown_change_figure(dff, title, change_template, current_col, change_col, base_col) 
    else:
        return sales_breakdown_totals_figure(dff, title, total_template, color_last, color_current, current_col, change_col, base_col)
    
def sales_group_revenue_graph(
    shift,
    metric,
    df,
    bounds,
    current_col,
    last_col,
    vs_col
):

    change_col, base_col = (vs_col, last_col) if metric in [vs_col, last_col] else ('vs. LY', 'Last Year')
    on_column = 'GenericLocation'
    measure = 'Revenue'
    
    rev_dff = user_site_filter(shift_filter(df, shift))
    dff = Group_Revenue(rev_dff,bounds,current_col,last_col,vs_col,on_column)
    
    total_template = templates['Sales'][measure]['Total']
    change_template = templates['Sales'][measure]['Change']
    
    color_current = total_colors[measure]['Current']
    color_last = total_colors[measure]['Last']
    
    title = 'Group Revenue ' + metric
    
    if metric in change_metrics:
        return sales_change_figure(dff,on_column,change_template,title,measure,current_col,change_col,base_col)
    else:
        return sales_totals_figure(dff,on_column,color_current,color_last,total_template,title,measure,current_col,change_col,base_col)

def sales_group_covers_graph(
    shift,
    metric,
    df,
    bounds,
    current_col,
    last_col,
    vs_col
):
    change_col, base_col = (vs_col, last_col) if metric in [vs_col, last_col] else ('vs. LY', 'Last Year')
    on_column = 'GenericLocation'
    measure = 'Covers'
    
    cov_dff = user_site_filter(shift_filter(df, shift))
    dff = Group_Covers(cov_dff,bounds,current_col,last_col,vs_col,on_column)
    
    total_template = templates['Sales'][measure]['Total']
    change_template = templates['Sales'][measure]['Change']
    
    color_current = total_colors[measure]['Current']
    color_last = total_colors[measure]['Last']
    
    title = 'Group Covers ' + metric
    
    if metric in change_metrics:
        return sales_change_figure(dff,on_column,change_template,title,measure,current_col,change_col,base_col)
    else:
        return sales_totals_figure(dff,on_column,color_current,color_last,total_template,title,measure,current_col,change_col,base_col)

def sales_group_spend_graph(
    shift,
    metric,
    rev_df,
    cov_df,
    bounds,
    current_col,
    last_col,
    vs_col
):
    change_col, base_col = (vs_col, last_col) if metric in [vs_col, last_col] else ('vs. LY', 'Last Year')
    on_column = 'GenericLocation'
    measure = 'Spend'
    
    rev_dff = user_site_filter(shift_filter(rev_df,shift))
    cov_dff = user_site_filter(shift_filter(cov_df,shift))
    dff = Group_Spend(rev_dff,cov_dff,bounds,current_col,last_col,vs_col,on_column)
        
    total_template = templates['Sales'][measure]['Total']
    change_template = templates['Sales'][measure]['Change']
    
    color_current = total_colors[measure]['Current']
    color_last = total_colors[measure]['Last']
    
    title = 'Group Restaurant Spend ' + metric
    
    if metric in change_metrics:
        return sales_change_figure(dff,'RevenueType',change_template,title, measure,current_col,change_col,base_col)
    else:
        return sales_totals_figure(dff,'RevenueType',color_current,color_last,total_template,title,measure,current_col,change_col,base_col)
      
def sales_site_revenue_graph(
    shift,
    metric,
    site,
    df,
    bounds,
    current_col,
    last_col,
    vs_col
):
    
    change_col, base_col = (vs_col, last_col) if metric in [vs_col, last_col] else ('vs. LY', 'Last Year')
    on_column = 'LocationName'
    measure = 'Revenue'
    
    rev_dff = shift_filter(df, shift)
    dff = Site_Revenue(site,rev_dff,bounds,current_col,last_col,vs_col,on_column)
    
    total_template = templates['Sales'][measure]['Total']
    change_template = templates['Sales'][measure]['Change']
    
    color_current = total_colors[measure]['Current']
    color_last = total_colors[measure]['Last']
    
    title = site + ' Revenue ' + metric
    
    if metric in change_metrics:
        return sales_change_figure(dff,on_column,change_template,title,measure,current_col,change_col,base_col)
    else:
        return sales_totals_figure(dff,on_column,color_current,color_last,total_template,title,measure,current_col,change_col,base_col)

def sales_site_covers_graph(
    shift,
    metric,
    site,
    df,
    bounds,
    current_col,
    last_col,
    vs_col
):
    
    change_col, base_col = (vs_col, last_col) if metric in [vs_col, last_col] else ('vs. LY', 'Last Year')
    on_column = 'LocationName'
    measure = 'Covers'
    
    cov_dff = shift_filter(df, shift)
    dff = Site_Covers(site,cov_dff,bounds,current_col,last_col,vs_col,on_column)
    
    total_template = templates['Sales'][measure]['Total']
    change_template = templates['Sales'][measure]['Change']
    
    color_current = total_colors[measure]['Current']
    color_last = total_colors[measure]['Last']
    
    title = site + ' Covers ' + metric
    
    if metric in change_metrics:
        return sales_change_figure(dff,on_column,change_template,title,measure,current_col,change_col,base_col)
    else:
        return sales_totals_figure(dff,on_column,color_current,color_last,total_template,title,measure,current_col,change_col,base_col)
    
def sales_site_spend_graph(
    shift,
    metric,
    site,
    rev_df,
    cov_df,
    bounds,
    current_col,
    last_col,
    vs_col
):
    
    change_col, base_col = (vs_col, last_col) if metric in [vs_col, last_col] else ('vs. LY', 'Last Year')
    on_column = 'LocationName'
    measure = 'Spend'
    
    rev_dff = shift_filter(rev_df,shift)
    cov_dff = shift_filter(cov_df,shift)
    dff = Site_Spend(site,rev_dff,cov_dff,bounds,current_col,last_col,vs_col,on_column)
    
    total_template = templates['Sales'][measure]['Total']
    change_template = templates['Sales'][measure]['Change']
    
    color_current = total_colors[measure]['Current']
    color_last = total_colors[measure]['Last']
    
    title = site + ' Restaurant Spend ' + metric
    
    if metric in change_metrics:
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
    rev_df,
    cov_df,
    bounds,
    day_df,
    current_col,
    last_col,
    vs_col
):
    
    change_col, base_col = (vs_col, last_col) if metric in [vs_col, last_col] else ('vs. LY', 'Last Year')
    on_columns = ['Session','Day']
    
    if measure == 'Revenue':
        
        rev_dff = area_filter(site_filter(rev_df, site),area)
        dff = Week_Revenue(site,category,rev_dff,bounds,day_df,current_col,last_col,vs_col,on_columns)
        
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
        dff = Week_Spend(site,category,rev_dff,cov_dff,bounds,day_df,current_col,last_col,vs_col,on_columns)
        
        y_last = dff[base_col]
        y_current = dff[current_col]
        y = dff[change_col]
    
    total_template = templates['Sales'][measure]['Total']
    change_template = templates['Sales'][measure]['Change']
    
    color_current = dff['Session'].apply(lambda x:week_colors_totals(measure, x,'Current'))
    color_last = dff['Session'].apply(lambda x:week_colors_totals(measure, x,'Last'))
        
    title = site + "  " + area + "  " + category + " " + measure + "  " + metric
    customdata = dff[change_col + ' %']
        
    if metric in change_metrics:
        return sales_week_change_figure(dff, y, change_template, title, measure, change_col)
    else:
        return sales_week_totals_figure(dff, y_last, y_current, color_last, color_current, total_template, title, measure, current_col, base_col)



def sales_week_covers_graph(
    site,
    area,
    measure,
    metric,
    weekmetric,
    cov_df,
    bounds,
    day_df,
    current_col,
    last_col,
    vs_col
):
    
    change_col, base_col = (vs_col, last_col) if metric in [vs_col, last_col] else ('vs. LY', 'Last Year')
    on_columns = ['Session','Day']
    measure = 'Covers'
    
    cov_dff = area_filter(site_filter(cov_df, site),area)
    dff = Week_Covers(site,cov_dff,bounds,day_df,current_col,last_col,vs_col,on_columns)
    
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
        
    if metric in change_metrics:
        return sales_week_change_figure(dff, y, change_template, title, measure, change_col)
    else:
        return sales_week_totals_figure(dff, y_last, y_current, color_last, color_current, total_template, title, measure, current_col, base_col)
    
    
# Tracker Graphs

def tracker_group_8_weeks_graph(week,metric,site, df, measure):
    
    dff = tracker_day_filter(
        tracker_group_df(
            tracker_user_site_filter(
                df
            )
        ), '8 Week'
    )
    
    x = dff['Week']
    graph = 'Next Eight Weeks - Group ' + measure
    
    if metric in change_metrics:
        return tracker_change_figure(dff, x, metric, graph, measure)
    else:
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
    
    if metric in change_metrics:
        return tracker_change_figure(dff, x, metric, graph, measure)
    else:
        return tracker_totals_figure(dff, x, metric, graph, measure)
    
def tracker_site_8_weeks_graph(week, metric, site, df, measure):
    
    dff = tracker_day_filter(
        tracker_site_filter(
            df, site
        ), '8 Week'
    )
    
    x = dff['Week']
    graph = 'Next Eight Weeks - ' + site + ' ' + measure
    
    if metric in change_metrics:
        return tracker_change_figure(dff, x, metric, graph, measure)
    else:
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
    graph = week + ' - ' + site + ' ' + measure
    
    if metric in change_metrics:
        return tracker_change_figure(dff, x, metric, graph, measure)
    else:
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
            
    if metric in change_metrics:
        return tracker_breakdown_change_figure(dff, metric, graph, measure)
    else:
        return tracker_breakdown_totals_figure(dff, metric, graph, measure)
