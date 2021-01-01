from display.layouts import *
from display.variables import *
from plots.graphs import *
from data.data import *
from data.date_bounds import *
from app import app

# Daily Sales Callbacks

@app.callback(dash.dependencies.Output('daily site dropdown', 'options'),
              [dash.dependencies.Input('daily shift dropdown', 'options')])
def update_daily_site_dropdown(shift):
    return [{'label':i,'value':i} for i in user_restaurants[auth._username]]

@app.callback(dash.dependencies.Output('daily site dropdown', 'value'),
              [dash.dependencies.Input('daily site dropdown', 'options')])
def set_daily_site_dropdown_value(available_options):
    return available_options[0]['value']

@app.callback(dash.dependencies.Output('daily sales total', 'figure'), daily_dropdown_dependencies)
def update_daily_sales_total(shift,area,measure,metric,site):
    return sales_breakdown_graph(shift,area,measure,metric,daily_rev_df,daily_cov_df,daily_bounds,daily_current_col,daily_last_col,daily_vs_col)
    
@app.callback(dash.dependencies.Output('daily group revenue', 'figure'),daily_dropdown_dependencies)
def update_daily_group_revenue(shift,area,measure,metric,site):
    return sales_group_revenue_graph(shift,metric,daily_rev_df,daily_bounds,daily_current_col,daily_last_col,daily_vs_col)
    
@app.callback(dash.dependencies.Output('daily group covers', 'figure'),daily_dropdown_dependencies)
def update_daily_group_covers(shift,area,measure,metric,site):
    return sales_group_covers_graph(shift,metric,daily_cov_df,daily_bounds,daily_current_col,daily_last_col,daily_vs_col)

@app.callback(dash.dependencies.Output('daily group spend', 'figure'),daily_dropdown_dependencies)
def update_daily_group_spend(shift,area,measure,metric,site):
    return sales_group_spend_graph(shift,metric,daily_rev_df,daily_cov_df,daily_bounds,daily_current_col,daily_last_col,daily_vs_col)

@app.callback(dash.dependencies.Output('daily site revenue', 'figure'),daily_dropdown_dependencies)
def update_daily_site_revenue(shift,area,measure,metric,site):
    return sales_site_revenue_graph(shift,metric,site,daily_rev_df,daily_bounds,daily_current_col,daily_last_col,daily_vs_col)

@app.callback(dash.dependencies.Output('daily site covers', 'figure'),daily_dropdown_dependencies)
def update_daily_site_covers(shift,area,measure,metric,site):
    return sales_site_covers_graph(shift,metric,site,daily_cov_df,daily_bounds,daily_current_col,daily_last_col,daily_vs_col)
    
@app.callback(dash.dependencies.Output('daily site spend', 'figure'),daily_dropdown_dependencies)
def update_daily_site_spend(shift,area,measure,metric,site):
    return sales_site_spend_graph(shift,metric,site,daily_rev_df,daily_cov_df,daily_bounds,daily_current_col,daily_last_col,daily_vs_col)
    
    
# WTD

@app.callback(dash.dependencies.Output('wtd site dropdown', 'options'),
              [dash.dependencies.Input('wtd shift dropdown', 'options')])
def update_wtd_site_dropdown(shift):
    return [{'label':i,'value':i} for i in user_restaurants[auth._username]]

@app.callback(dash.dependencies.Output('wtd site dropdown', 'value'),
              [dash.dependencies.Input('wtd site dropdown', 'options')])
def set_wtd_site_dropdown_value(available_options):
    return available_options[0]['value']

@app.callback(dash.dependencies.Output('wtd site week dropdown', 'options'),
              [dash.dependencies.Input('wtd shift dropdown', 'options')])
def update_wtd_site_week_dropdown(shift):
    return [{'label':i,'value':i} for i in ['Group'] + user_restaurants[auth._username]]

@app.callback(dash.dependencies.Output('wtd sales total', 'figure'), wtd_dropdown_dependencies)
def update_wtd_sales_total(shift,area,measure,metric,site):
    return sales_breakdown_graph(shift,area,measure,metric,wtd_rev_df,wtd_cov_df,wtd_bounds,wtd_current_col,wtd_last_col,wtd_vs_col)
    
@app.callback(dash.dependencies.Output('wtd group revenue', 'figure'),wtd_dropdown_dependencies)
def update_wtd_group_revenue(shift,area,measure,metric,site):
    return sales_group_revenue_graph(shift,metric,wtd_rev_df,wtd_bounds,wtd_current_col,wtd_last_col,wtd_vs_col)
    
@app.callback(dash.dependencies.Output('wtd group covers', 'figure'),wtd_dropdown_dependencies)
def update_wtd_group_covers(shift,area,measure,metric,site):
    return sales_group_covers_graph(shift,metric,wtd_cov_df,wtd_bounds,wtd_current_col,wtd_last_col,wtd_vs_col)

@app.callback(dash.dependencies.Output('wtd group spend', 'figure'),wtd_dropdown_dependencies)
def update_wtd_group_spend(shift,area,measure,metric,site):
    return sales_group_spend_graph(shift,metric,wtd_rev_df,wtd_cov_df,wtd_bounds,wtd_current_col,wtd_last_col,wtd_vs_col)

@app.callback(dash.dependencies.Output('wtd site revenue', 'figure'),wtd_dropdown_dependencies)
def update_wtd_site_revenue(shift,area,measure,metric,site):
    return sales_site_revenue_graph(shift,metric,site,wtd_rev_df,wtd_bounds,wtd_current_col,wtd_last_col,wtd_vs_col)

@app.callback(dash.dependencies.Output('wtd site covers', 'figure'),wtd_dropdown_dependencies)
def update_wtd_site_covers(shift,area,measure,metric,site):
    return sales_site_covers_graph(shift,metric,site,wtd_cov_df,wtd_bounds,wtd_current_col,wtd_last_col,wtd_vs_col)
    
@app.callback(dash.dependencies.Output('wtd site spend', 'figure'),wtd_dropdown_dependencies)
def update_wtd_site_spend(shift,area,measure,metric,site):
    return sales_site_spend_graph(shift,metric,site,wtd_rev_df,wtd_cov_df,wtd_bounds,wtd_current_col,wtd_last_col,wtd_vs_col)

@app.callback(dash.dependencies.Output('wtd week view', 'figure'),wtd_week_dropdown_dependencies)
def update_wtd_week_view(site,area,category,measure,metric,weekmetric):
    return sales_week_view_graph(site, area, category, measure, metric, weekmetric, wtd_rev_df,wtd_cov_df,wtd_bounds,wtd_days,wtd_current_col,wtd_last_col,wtd_vs_col)

@app.callback(dash.dependencies.Output('wtd week covers', 'figure'),wtd_week_dropdown_dependencies)
def update_wtd_week_covers(site,area,category,measure,metric,weekmetric):
    return sales_week_covers_graph(site, area, measure, metric, weekmetric, wtd_cov_df,wtd_bounds,wtd_days,wtd_current_col,wtd_last_col,wtd_vs_col)


# MTD Sales

@app.callback(dash.dependencies.Output('mtd site dropdown', 'options'),
              [dash.dependencies.Input('mtd shift dropdown', 'options')])
def update_mtd_site_dropdown(shift):
    return [{'label':i,'value':i} for i in user_restaurants[auth._username]]

@app.callback(dash.dependencies.Output('mtd site dropdown', 'value'),
              [dash.dependencies.Input('mtd site dropdown', 'options')])
def set_mtd_site_dropdown_value(available_options):
    return available_options[0]['value']

@app.callback(dash.dependencies.Output('mtd site week dropdown', 'options'),
              [dash.dependencies.Input('mtd shift dropdown', 'options')])
def update_mtd_site_week_dropdown(shift):
    return [{'label':i,'value':i} for i in ['Group'] + user_restaurants[auth._username]]

@app.callback(dash.dependencies.Output('mtd sales total', 'figure'), mtd_dropdown_dependencies)
def update_mtd_sales_total(shift,area,measure,metric,site):
    return sales_breakdown_graph(shift,area,measure,metric,mtd_rev_df,mtd_cov_df,mtd_bounds,mtd_current_col,mtd_last_col,mtd_vs_col)
    
@app.callback(dash.dependencies.Output('mtd group revenue', 'figure'),mtd_dropdown_dependencies)
def update_mtd_group_revenue(shift,area,measure,metric,site):
    return sales_group_revenue_graph(shift,metric,mtd_rev_df,mtd_bounds,mtd_current_col,mtd_last_col,mtd_vs_col)
    
@app.callback(dash.dependencies.Output('mtd group covers', 'figure'),mtd_dropdown_dependencies)
def update_mtd_group_covers(shift,area,measure,metric,site):
    return sales_group_covers_graph(shift,metric,mtd_cov_df,mtd_bounds,mtd_current_col,mtd_last_col,mtd_vs_col)

@app.callback(dash.dependencies.Output('mtd group spend', 'figure'),mtd_dropdown_dependencies)
def update_mtd_group_spend(shift,area,measure,metric,site):
    return sales_group_spend_graph(shift,metric,mtd_rev_df,mtd_cov_df,mtd_bounds,mtd_current_col,mtd_last_col,mtd_vs_col)

@app.callback(dash.dependencies.Output('mtd site revenue', 'figure'),mtd_dropdown_dependencies)
def update_mtd_site_revenue(shift,area,measure,metric,site):
    return sales_site_revenue_graph(shift,metric,site,mtd_rev_df,mtd_bounds,mtd_current_col,mtd_last_col,mtd_vs_col)

@app.callback(dash.dependencies.Output('mtd site covers', 'figure'),mtd_dropdown_dependencies)
def update_mtd_site_covers(shift,area,measure,metric,site):
    return sales_site_covers_graph(shift,metric,site,mtd_cov_df,mtd_bounds,mtd_current_col,mtd_last_col,mtd_vs_col)
    
@app.callback(dash.dependencies.Output('mtd site spend', 'figure'),mtd_dropdown_dependencies)
def update_mtd_site_spend(shift,area,measure,metric,site):
    return sales_site_spend_graph(shift,metric,site,mtd_rev_df,mtd_cov_df,mtd_bounds,mtd_current_col,mtd_last_col,mtd_vs_col)

@app.callback(dash.dependencies.Output('mtd week view', 'figure'),mtd_week_dropdown_dependencies)
def update_mtd_week_view(site,area,category,measure,metric,weekmetric):
    return sales_week_view_graph(site, area, category, measure, metric, weekmetric, mtd_rev_df,mtd_cov_df,mtd_bounds,mtd_days,mtd_current_col,mtd_last_col,mtd_vs_col)

@app.callback(dash.dependencies.Output('mtd week covers', 'figure'),mtd_week_dropdown_dependencies)
def update_mtd_week_covers(site,area,category,measure,metric,weekmetric):
    return sales_week_covers_graph(site, area, measure, metric, weekmetric, mtd_cov_df,mtd_bounds,mtd_days,mtd_current_col,mtd_last_col,mtd_vs_col)

# Weekly

@app.callback(dash.dependencies.Output('weekly site dropdown', 'options'),
              [dash.dependencies.Input('weekly shift dropdown', 'options')])
def update_weekly_site_dropdown(shift):
    return [{'label':i,'value':i} for i in user_restaurants[auth._username]]

@app.callback(dash.dependencies.Output('weekly site dropdown', 'value'),
              [dash.dependencies.Input('weekly site dropdown', 'options')])
def set_weekly_site_dropdown_value(available_options):
    return available_options[0]['value']

@app.callback(dash.dependencies.Output('weekly site week dropdown', 'options'),
              [dash.dependencies.Input('weekly shift dropdown', 'options')])
def update_weekly_site_week_dropdown(shift):
    return [{'label':i,'value':i} for i in ['Group'] + user_restaurants[auth._username]]

@app.callback(dash.dependencies.Output('weekly sales total', 'figure'), weekly_dropdown_dependencies)
def update_weekly_sales_total(shift,area,measure,metric,site):
    return sales_breakdown_graph(shift,area,measure,metric,weekly_rev_df,weekly_cov_df,weekly_bounds,weekly_current_col,weekly_last_col,weekly_vs_col)
    
@app.callback(dash.dependencies.Output('weekly group revenue', 'figure'),weekly_dropdown_dependencies)
def update_weekly_group_revenue(shift,area,measure,metric,site):
    return sales_group_revenue_graph(shift,metric,weekly_rev_df,weekly_bounds,weekly_current_col,weekly_last_col,weekly_vs_col)
    
@app.callback(dash.dependencies.Output('weekly group covers', 'figure'),weekly_dropdown_dependencies)
def update_weekly_group_covers(shift,area,measure,metric,site):
    return sales_group_covers_graph(shift,metric,weekly_cov_df,weekly_bounds,weekly_current_col,weekly_last_col,weekly_vs_col)

@app.callback(dash.dependencies.Output('weekly group spend', 'figure'),weekly_dropdown_dependencies)
def update_weekly_group_spend(shift,area,measure,metric,site):
    return sales_group_spend_graph(shift,metric,weekly_rev_df,weekly_cov_df,weekly_bounds,weekly_current_col,weekly_last_col,weekly_vs_col)

@app.callback(dash.dependencies.Output('weekly site revenue', 'figure'),weekly_dropdown_dependencies)
def update_weekly_site_revenue(shift,area,measure,metric,site):
    return sales_site_revenue_graph(shift,metric,site,weekly_rev_df,weekly_bounds,weekly_current_col,weekly_last_col,weekly_vs_col)

@app.callback(dash.dependencies.Output('weekly site covers', 'figure'),weekly_dropdown_dependencies)
def update_weekly_site_covers(shift,area,measure,metric,site):
    return sales_site_covers_graph(shift,metric,site,weekly_cov_df,weekly_bounds,weekly_current_col,weekly_last_col,weekly_vs_col)
    
@app.callback(dash.dependencies.Output('weekly site spend', 'figure'),weekly_dropdown_dependencies)
def update_weekly_site_spend(shift,area,measure,metric,site):
    return sales_site_spend_graph(shift,metric,site,weekly_rev_df,weekly_cov_df,weekly_bounds,weekly_current_col,weekly_last_col,weekly_vs_col)

@app.callback(dash.dependencies.Output('weekly week view', 'figure'),weekly_week_dropdown_dependencies)
def update_weekly_week_view(site,area,category,measure,metric,weekmetric):
    return sales_week_view_graph(site, area, category, measure, metric, weekmetric, weekly_rev_df,weekly_cov_df,weekly_bounds,weekly_days,weekly_current_col,weekly_last_col,weekly_vs_col)

@app.callback(dash.dependencies.Output('weekly week covers', 'figure'),weekly_week_dropdown_dependencies)
def update_weekly_week_covers(site,area,category,measure,metric,weekmetric):
    return sales_week_covers_graph(site, area, measure, metric, weekmetric, weekly_cov_df,weekly_bounds,weekly_days,weekly_current_col,weekly_last_col,weekly_vs_col)

# Monthly

@app.callback(dash.dependencies.Output('monthly site dropdown', 'options'),
              [dash.dependencies.Input('monthly shift dropdown', 'options')])
def update_monthly_site_dropdown(shift):
    return [{'label':i,'value':i} for i in user_restaurants[auth._username]]

@app.callback(dash.dependencies.Output('monthly site dropdown', 'value'),
              [dash.dependencies.Input('monthly site dropdown', 'options')])
def set_monthly_site_dropdown_value(available_options):
    return available_options[0]['value']

@app.callback(dash.dependencies.Output('monthly site week dropdown', 'options'),
              [dash.dependencies.Input('monthly shift dropdown', 'options')])
def update_monthly_site_week_dropdown(shift):
    return [{'label':i,'value':i} for i in ['Group'] + user_restaurants[auth._username]]

@app.callback(dash.dependencies.Output('monthly sales total', 'figure'), monthly_dropdown_dependencies)
def update_monthly_sales_total(shift,area,measure,metric,site):
    return sales_breakdown_graph(shift,area,measure,metric,monthly_rev_df,monthly_cov_df,monthly_bounds,monthly_current_col,monthly_last_col,monthly_vs_col)
    
@app.callback(dash.dependencies.Output('monthly group revenue', 'figure'),monthly_dropdown_dependencies)
def update_monthly_group_revenue(shift,area,measure,metric,site):
    return sales_group_revenue_graph(shift,metric,monthly_rev_df,monthly_bounds,monthly_current_col,monthly_last_col,monthly_vs_col)
    
@app.callback(dash.dependencies.Output('monthly group covers', 'figure'),monthly_dropdown_dependencies)
def update_monthly_group_covers(shift,area,measure,metric,site):
    return sales_group_covers_graph(shift,metric,monthly_cov_df,monthly_bounds,monthly_current_col,monthly_last_col,monthly_vs_col)

@app.callback(dash.dependencies.Output('monthly group spend', 'figure'),monthly_dropdown_dependencies)
def update_monthly_group_spend(shift,area,measure,metric,site):
    return sales_group_spend_graph(shift,metric,monthly_rev_df,monthly_cov_df,monthly_bounds,monthly_current_col,monthly_last_col,monthly_vs_col)

@app.callback(dash.dependencies.Output('monthly site revenue', 'figure'),monthly_dropdown_dependencies)
def update_monthly_site_revenue(shift,area,measure,metric,site):
    return sales_site_revenue_graph(shift,metric,site,monthly_rev_df,monthly_bounds,monthly_current_col,monthly_last_col,monthly_vs_col)

@app.callback(dash.dependencies.Output('monthly site covers', 'figure'),monthly_dropdown_dependencies)
def update_monthly_site_covers(shift,area,measure,metric,site):
    return sales_site_covers_graph(shift,metric,site,monthly_cov_df,monthly_bounds,monthly_current_col,monthly_last_col,monthly_vs_col)
    
@app.callback(dash.dependencies.Output('monthly site spend', 'figure'),monthly_dropdown_dependencies)
def update_monthly_site_spend(shift,area,measure,metric,site):
    return sales_site_spend_graph(shift,metric,site,monthly_rev_df,monthly_cov_df,monthly_bounds,monthly_current_col,monthly_last_col,monthly_vs_col)

@app.callback(dash.dependencies.Output('monthly week view', 'figure'),monthly_week_dropdown_dependencies)
def update_monthly_week_view(site,area,category,measure,metric,weekmetric):
    return sales_week_view_graph(site, area, category, measure, metric, weekmetric, monthly_rev_df,monthly_cov_df,monthly_bounds,monthly_days,monthly_current_col,monthly_last_col,monthly_vs_col)

@app.callback(dash.dependencies.Output('monthly week covers', 'figure'),monthly_week_dropdown_dependencies)
def update_monthly_week_covers(site,area,category,measure,metric,weekmetric):
    return sales_week_covers_graph(site, area, measure, metric, weekmetric, monthly_cov_df,monthly_bounds,monthly_days,monthly_current_col,monthly_last_col,monthly_vs_col)

# Tracker

@app.callback(dash.dependencies.Output('tracker_site_dropdown', 'options'),
              [dash.dependencies.Input('tracker_week_dropdown', 'options')])
def update_tracker_site_dropdown(week):
    return [{'label':i,'value':i} for i in bookings_user_restaurants[auth._username]]

@app.callback(dash.dependencies.Output('tracker_site_dropdown', 'value'),
              [dash.dependencies.Input('tracker_site_dropdown', 'options')])
def set_tracker_site_dropdown_value(available_options):
    return available_options[0]['value']

@app.callback(dash.dependencies.Output('tracker_group_8_weeks', 'figure'),tracker_dropdown_dependencies)
def update_tracker_group_8_weeks(week,metric,site):
    return tracker_group_8_weeks_graph(week,metric,site, tracker_df, 'Booked Covers')
    
@app.callback(dash.dependencies.Output('tracker_group_week', 'figure'),tracker_dropdown_dependencies)
def update_tracker_group_week(week,metric,site):
    return tracker_group_week_graph(week, metric, site, tracker_df, 'Booked Covers')

@app.callback(dash.dependencies.Output('tracker_site_8_weeks', 'figure'),tracker_dropdown_dependencies)
def update_tracker_site_8_weeks(week,metric,site):
    return tracker_site_8_weeks_graph(week, metric, site, tracker_df, 'Booked Covers')
    
@app.callback(dash.dependencies.Output('tracker_site_week', 'figure'),tracker_dropdown_dependencies)
def update_tracker_site_week(week,metric,site):
    return tracker_site_week_graph(week, metric, site, tracker_df, 'Booked Covers')
    
@app.callback(dash.dependencies.Output('tracker_breakdown', 'figure'),tracker_dropdown_dependencies)
def update_tracker_breakdown(week,metric,site):
    return tracker_breakdown_graph(week, metric, site, tracker_df, 'Booked Covers')

# Pickup

@app.callback(dash.dependencies.Output('pickup_site_dropdown', 'options'),
              [dash.dependencies.Input('pickup_week_dropdown', 'options')])
def update_pickup_site_dropdown(week):
    return [{'label':i,'value':i} for i in bookings_user_restaurants[auth._username]]

@app.callback(dash.dependencies.Output('pickup_site_dropdown', 'value'),
              [dash.dependencies.Input('pickup_site_dropdown', 'options')])
def set_pickup_site_dropdown_value(available_options):
    return available_options[0]['value']

@app.callback(dash.dependencies.Output('pickup_group_8_weeks', 'figure'),pickup_dropdown_dependencies)
def update_pickup_group_8_weeks(week,metric,site):
    return tracker_group_8_weeks_graph(week,metric,site, pickup_df, 'Pickup')
    
@app.callback(dash.dependencies.Output('pickup_group_week', 'figure'),pickup_dropdown_dependencies)
def update_pickup_group_week(week,metric,site):
    return tracker_group_week_graph(week, metric, site, pickup_df, 'Pickup')

@app.callback(dash.dependencies.Output('pickup_site_8_weeks', 'figure'),pickup_dropdown_dependencies)
def update_pickup_site_8_weeks(week,metric,site):
    return tracker_site_8_weeks_graph(week, metric, site, pickup_df, 'Pickup')
    
@app.callback(dash.dependencies.Output('pickup_site_week', 'figure'),pickup_dropdown_dependencies)
def update_pickup_site_week(week,metric,site):
    return tracker_site_week_graph(week, metric, site, pickup_df, 'Pickup')
    
@app.callback(dash.dependencies.Output('pickup_breakdown', 'figure'),pickup_dropdown_dependencies)
def update_pickup_breakdown(week,metric,site):
    return tracker_breakdown_graph(week, metric, site, pickup_df, 'Pickup')


# Future Bookings

@app.callback(dash.dependencies.Output('future graph', 'figure'),
              [dash.dependencies.Input('future dropdown', 'value')])
def update_daily_site_dropdown(metric):
    if metric == 'Total Bookings':
        return future_totals_figure(bookings_user_restaurants[auth._username],future_df)
    else:
        return future_changes_figure(bookings_user_restaurants[auth._username],future_df)
    
    
# Booking Trends
    
@app.callback(dash.dependencies.Output('trends site dropdown', 'options'),
              [dash.dependencies.Input('textarea-example', 'value')])
def update_daily_site_dropdown(shift):
    return [{'label':i,'value':i} for i in bookings_user_restaurants[auth._username]]

@app.callback(dash.dependencies.Output('trends site dropdown', 'value'),
              [dash.dependencies.Input('trends site dropdown', 'options')])
def set_daily_site_dropdown_value(available_options):
    return available_options[0]['value']

@app.callback(dash.dependencies.Output('trends site pickup', 'figure'),
             [dash.dependencies.Input('trends site dropdown', 'value')])
def update_site_pickup(site):
    return trends_site_pickup_figure(trends_df,site,today_week,today_weekday_num)

@app.callback(dash.dependencies.Output('trends site future', 'figure'),
             [dash.dependencies.Input('trends site dropdown', 'value')])
def update_site_future(site):
    return trends_site_future_figure(trends_df,site,today_week,today_weekday_num)
