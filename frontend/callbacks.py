from dash.dependencies import Input, Output

from app import app
from authentication.users import bookings_to_sales_restaurants_dict
from frontend.layouts import *
from frontend.plots.graphs import *
from data.data import tracker_df, pickup_df, trends_df, future_df

# Dropdown Inputs

def dropdown_inputs(report):
    
    def dropdown_ids(report):
        dropdowns = ['shift','area','measure','metric','site']
        return [report + ' ' + dropdown + ' dropdown' for dropdown in dropdowns]
    
    dropdown_ids = dropdown_ids(report)
    return [Input(x, 'value') for x in dropdown_ids]

def week_dropdown_inputs(report):
    
    def week_dropdown_ids(report):
        dropdowns = ['site','area','category','measure']
        return [report + ' ' + dropdown + ' week dropdown' for dropdown in dropdowns] + [report + ' metric dropdown'] + [report + ' metric week dropdown']

    dropdown_ids = week_dropdown_ids(report)
    return [Input(x, 'value') for x in dropdown_ids]

daily_dropdown_inputs = dropdown_inputs('daily')
wtd_dropdown_inputs = dropdown_inputs('wtd')
mtd_dropdown_inputs = dropdown_inputs('mtd')
weekly_dropdown_inputs = dropdown_inputs('weekly')
monthly_dropdown_inputs = dropdown_inputs('monthly')

wtd_week_dropdown_inputs = week_dropdown_inputs('wtd')
mtd_week_dropdown_inputs = week_dropdown_inputs('mtd')
weekly_week_dropdown_inputs = week_dropdown_inputs('weekly')
monthly_week_dropdown_inputs = week_dropdown_inputs('monthly')

tracker_dropdown_ids = ['tracker_week_dropdown','tracker_metric_dropdown','tracker_site_dropdown']
tracker_dropdown_inputs = [Input(x, 'value') for x in tracker_dropdown_ids]

pickup_dropdown_ids = ['pickup_week_dropdown','pickup_metric_dropdown','pickup_site_dropdown']
pickup_dropdown_inputs = [Input(x, 'value') for x in pickup_dropdown_ids]

# Callbacks

# Home Page

@app.callback(
    Output('homepage daily sales','figure'),
    [Input('homepage metric dropdown','value'),
     Input('homepage measure dropdown', 'value'),])
def update_homepage_daily_sales(metric,measure):
    
    if measure == 'Revenue':
        func = sales_group_revenue_graph
    elif measure == 'Covers':
        func = sales_group_covers_graph
    elif measure == 'Spend':
        func = sales_group_spend_graph
        
    return func('All Shifts',metric,'daily')

@app.callback(
    Output('homepage wtd sales','figure'),
    [Input('homepage metric dropdown','value'),
     Input('homepage measure dropdown', 'value'),])
def update_homepage_wtd_sales(metric,measure):
    
    if measure == 'Revenue':
        func = sales_group_revenue_graph
    elif measure == 'Covers':
        func = sales_group_covers_graph
    elif measure == 'Spend':
        func = sales_group_spend_graph
        
    return func('All Shifts',metric,'wtd')

@app.callback(
    Output('homepage mtd sales','figure'),
    [Input('homepage metric dropdown','value'),
     Input('homepage measure dropdown', 'value'),])
def update_homepage_mtd_sales(metric,measure):
    
    if measure == 'Revenue':
        func = sales_group_revenue_graph
    elif measure == 'Covers':
        func = sales_group_covers_graph
    elif measure == 'Spend':
        func = sales_group_spend_graph
        
    if metric == 'vs. LW':
        metric = 'vs. LM'
    elif metric == 'Totals Last Week':
        metric = 'Totals Last Month'
        
    return func('All Shifts',metric,'mtd')

@app.callback(Output('homepage tracker','figure'),
             [Input('homepage metric dropdown','value')])
def update_homepage_tracker(metric):
    return tracker_group_8_weeks_graph('This Week',metric,'100 Wardour St', tracker_df, 'Booked Covers')

@app.callback(Output('homepage pickup','figure'),
             [Input('homepage metric dropdown','value')])
def update_homepage_pickup(metric):
    return tracker_group_8_weeks_graph('This Week',metric,'100 Wardour St', pickup_df, 'Pickup')


# Breakdown 

@app.callback(
    Output('breakdown daily sales','figure'),
    [Input('breakdown metric dropdown','value'),
     Input('breakdown measure dropdown', 'value'),])
def update_breakdown_daily_sales(metric,measure):
    return sales_breakdown_graph(
        'All Shifts',
        'Full Site',
        measure,
        metric,
        'daily'
    ) 

@app.callback(
    Output('breakdown wtd sales','figure'),
    [Input('breakdown metric dropdown','value'),
     Input('breakdown measure dropdown', 'value'),])
def update_breakdown_daily_sales(metric,measure):
    return sales_breakdown_graph(
        'All Shifts',
        'Full Site',
        measure,
        metric,
        'wtd'
    ) 

@app.callback(
    Output('breakdown mtd sales','figure'),
    [Input('breakdown metric dropdown','value'),
     Input('breakdown measure dropdown', 'value'),])
def update_breakdown_daily_sales(metric,measure):
        
    if metric == 'vs. LW':
        metric = 'vs. LM'
    elif metric == 'Totals Last Week':
        metric = 'Totals Last Month'
        
    return sales_breakdown_graph(
        'All Shifts',
        'Full Site',
        measure,
        metric,
        'mtd'
    )

@app.callback(Output('breakdown this week tracker','figure'),
             [Input('breakdown metric dropdown','value')])
def update_breakdown_this_week_tracker(metric):
    return tracker_breakdown_graph('This Week', metric, 'Group', tracker_df, 'Booked Covers')

@app.callback(Output('breakdown next week tracker','figure'),
             [Input('breakdown metric dropdown','value')])
def update_breakdown_next_week_tracker(metric):
    return tracker_breakdown_graph('Next Week', metric, 'Group', tracker_df, 'Booked Covers')

@app.callback(Output('breakdown two weeks tracker','figure'),
             [Input('breakdown metric dropdown','value')])
def update_breakdown_two_weeks_tracker(metric):
    return tracker_breakdown_graph('Two Weeks', metric, 'Group', tracker_df, 'Booked Covers')


# Restaurant

@app.callback(Output('restaurant site dropdown', 'options'),
              [Input('restaurant metric dropdown', 'options')])
def update_daily_site_dropdown(shift):
    return [{'label':i,'value':i} for i in user_restaurants[auth._username]['bookings']]

@app.callback(Output('restaurant site dropdown', 'value'),
              [Input('restaurant site dropdown', 'options')])
def set_daily_site_dropdown_value(available_options):
    return available_options[0]['value']

@app.callback(
    Output('restaurant daily sales','figure'),
    [Input('restaurant metric dropdown','value'),
     Input('restaurant site dropdown', 'value'),])
def update_restaurant_daily_sales(metric,site):
    site = bookings_to_sales_restaurants_dict[site]
    return sales_site_revenue_graph('All Shifts', metric, site, 'daily')

@app.callback(
    Output('restaurant wtd sales','figure'),
    [Input('restaurant metric dropdown','value'),
     Input('restaurant site dropdown', 'value'),])
def update_restaurant_wtd_sales(metric,site):
    site = bookings_to_sales_restaurants_dict[site]
    return sales_site_revenue_graph('All Shifts', metric, site, 'wtd')

@app.callback(
    Output('restaurant mtd sales','figure'),
    [Input('restaurant metric dropdown','value'),
     Input('restaurant site dropdown', 'value'),])
def update_restaurant_mtd_sales(metric,site):
    site = bookings_to_sales_restaurants_dict[site]
    return sales_site_revenue_graph('All Shifts', metric, site, 'mtd')


@app.callback(
    Output('restaurant daily spend','figure'),
    [Input('restaurant metric dropdown','value'),
     Input('restaurant site dropdown', 'value'),])
def update_restaurant_daily_spend(metric,site):
    site = bookings_to_sales_restaurants_dict[site]
    return sales_site_spend_graph('All Shifts', metric, site, 'daily')

@app.callback(
    Output('restaurant wtd spend','figure'),
    [Input('restaurant metric dropdown','value'),
     Input('restaurant site dropdown', 'value'),])
def update_restaurant_wtd_spend(metric,site):
    site = bookings_to_sales_restaurants_dict[site]
    return sales_site_spend_graph('All Shifts', metric, site, 'wtd')

@app.callback(
    Output('restaurant mtd spend','figure'),
    [Input('restaurant metric dropdown','value'),
     Input('restaurant site dropdown', 'value'),])
def update_restaurant_mtd_spend(metric,site):
    site = bookings_to_sales_restaurants_dict[site]
    return sales_site_spend_graph('All Shifts', metric, site, 'mtd')


@app.callback(
    Output('restaurant future', 'figure'),
    [Input('restaurant metric dropdown', 'value'),
     Input('restaurant site dropdown', 'value'),])
def update_restaurant_future(metric,site):
    return future_totals_figure([site],future_df)


@app.callback(
    Output('restaurant tracker','figure'),
    [Input('restaurant metric dropdown','value'),
     Input('restaurant site dropdown', 'value'),])
def update_restaurant_tracker(metric,site):
    return tracker_site_8_weeks_graph('This Week', metric, site, tracker_df, 'Booked Covers')

@app.callback(
    Output('restaurant pickup','figure'),
    [Input('restaurant metric dropdown','value'),
     Input('restaurant site dropdown', 'value'),])
def update_restaurant_pickup(metric,site):
    return tracker_site_8_weeks_graph('This Week', metric, site, pickup_df, 'Pickup')



# Daily Sales

@app.callback(Output('daily site dropdown', 'options'),
              [Input('daily shift dropdown', 'options')])
def update_daily_site_dropdown(shift):
    return [{'label':i,'value':i} for i in user_restaurants[auth._username]['sales']]

@app.callback(Output('daily site dropdown', 'value'),
              [Input('daily site dropdown', 'options')])
def set_daily_site_dropdown_value(available_options):
    return available_options[0]['value']

@app.callback(Output('daily sales total', 'figure'), daily_dropdown_inputs)
def update_daily_sales_total(shift,area,measure,metric,site):
    return sales_breakdown_graph(shift,area,measure,metric,'daily')
    
@app.callback(Output('daily group revenue', 'figure'),daily_dropdown_inputs)
def update_daily_group_revenue(shift,area,measure,metric,site):
    return sales_group_revenue_graph(shift,metric,'daily')
    
@app.callback(Output('daily group covers', 'figure'),daily_dropdown_inputs)
def update_daily_group_covers(shift,area,measure,metric,site):
    return sales_group_covers_graph(shift,metric,'daily')

@app.callback(Output('daily group spend', 'figure'),daily_dropdown_inputs)
def update_daily_group_spend(shift,area,measure,metric,site):
    return sales_group_spend_graph(shift,metric,'daily')

@app.callback(Output('daily site revenue', 'figure'),daily_dropdown_inputs)
def update_daily_site_revenue(shift,area,measure,metric,site):
    return sales_site_revenue_graph(shift,metric,site,'daily')

@app.callback(Output('daily site covers', 'figure'),daily_dropdown_inputs)
def update_daily_site_covers(shift,area,measure,metric,site):
    return sales_site_covers_graph(shift,metric,site,'daily')
    
@app.callback(Output('daily site spend', 'figure'),daily_dropdown_inputs)
def update_daily_site_spend(shift,area,measure,metric,site):
    return sales_site_spend_graph(shift,metric,site,'daily')
    
# WTD Sales

@app.callback(Output('wtd site dropdown', 'options'),
              [Input('wtd shift dropdown', 'options')])
def update_wtd_site_dropdown(shift):
    return [{'label':i,'value':i} for i in user_restaurants[auth._username]['sales']]

@app.callback(Output('wtd site dropdown', 'value'),
              [Input('wtd site dropdown', 'options')])
def set_wtd_site_dropdown_value(available_options):
    return available_options[0]['value']

@app.callback(Output('wtd site week dropdown', 'options'),
              [Input('wtd shift dropdown', 'options')])
def update_wtd_site_week_dropdown(shift):
    return [{'label':i,'value':i} for i in ['Group'] + user_restaurants[auth._username]['sales']]

@app.callback(Output('wtd sales total', 'figure'), wtd_dropdown_inputs)
def update_wtd_sales_total(shift,area,measure,metric,site):
    return sales_breakdown_graph(shift,area,measure,metric,'wtd')
    
@app.callback(Output('wtd group revenue', 'figure'),wtd_dropdown_inputs)
def update_wtd_group_revenue(shift,area,measure,metric,site):
    return sales_group_revenue_graph(shift,metric,'wtd')
    
@app.callback(Output('wtd group covers', 'figure'),wtd_dropdown_inputs)
def update_wtd_group_covers(shift,area,measure,metric,site):
    return sales_group_covers_graph(shift,metric,'wtd')

@app.callback(Output('wtd group spend', 'figure'),wtd_dropdown_inputs)
def update_wtd_group_spend(shift,area,measure,metric,site):
    return sales_group_spend_graph(shift,metric,'wtd')

@app.callback(Output('wtd site revenue', 'figure'),wtd_dropdown_inputs)
def update_wtd_site_revenue(shift,area,measure,metric,site):
    return sales_site_revenue_graph(shift,metric,site,'wtd')

@app.callback(Output('wtd site covers', 'figure'),wtd_dropdown_inputs)
def update_wtd_site_covers(shift,area,measure,metric,site):
    return sales_site_covers_graph(shift,metric,site,'wtd')
    
@app.callback(Output('wtd site spend', 'figure'),wtd_dropdown_inputs)
def update_wtd_site_spend(shift,area,measure,metric,site):
    return sales_site_spend_graph(shift,metric,site,'wtd')

@app.callback(Output('wtd week view', 'figure'),wtd_week_dropdown_inputs)
def update_wtd_week_view(site,area,category,measure,metric,weekmetric):
    return sales_week_view_graph(site, area, category, measure, metric, weekmetric, 'wtd')

@app.callback(Output('wtd week covers', 'figure'),wtd_week_dropdown_inputs)
def update_wtd_week_covers(site,area,category,measure,metric,weekmetric):
    return sales_week_covers_graph(site, area, measure, metric, weekmetric, 'wtd')


# MTD Sales

@app.callback(Output('mtd site dropdown', 'options'),
              [Input('mtd shift dropdown', 'options')])
def update_mtd_site_dropdown(shift):
    return [{'label':i,'value':i} for i in user_restaurants[auth._username]['sales']]

@app.callback(Output('mtd site dropdown', 'value'),
              [Input('mtd site dropdown', 'options')])
def set_mtd_site_dropdown_value(available_options):
    return available_options[0]['value']

@app.callback(Output('mtd site week dropdown', 'options'),
              [Input('mtd shift dropdown', 'options')])
def update_mtd_site_week_dropdown(shift):
    return [{'label':i,'value':i} for i in ['Group'] + user_restaurants[auth._username]['sales']]

@app.callback(Output('mtd sales total', 'figure'), mtd_dropdown_inputs)
def update_mtd_sales_total(shift,area,measure,metric,site):
    return sales_breakdown_graph(shift,area,measure,metric,'mtd')
    
@app.callback(Output('mtd group revenue', 'figure'),mtd_dropdown_inputs)
def update_mtd_group_revenue(shift,area,measure,metric,site):
    return sales_group_revenue_graph(shift,metric,'mtd')
    
@app.callback(Output('mtd group covers', 'figure'),mtd_dropdown_inputs)
def update_mtd_group_covers(shift,area,measure,metric,site):
    return sales_group_covers_graph(shift,metric,'mtd')

@app.callback(Output('mtd group spend', 'figure'),mtd_dropdown_inputs)
def update_mtd_group_spend(shift,area,measure,metric,site):
    return sales_group_spend_graph(shift,metric,'mtd')

@app.callback(Output('mtd site revenue', 'figure'),mtd_dropdown_inputs)
def update_mtd_site_revenue(shift,area,measure,metric,site):
    return sales_site_revenue_graph(shift,metric,site,'mtd')

@app.callback(Output('mtd site covers', 'figure'),mtd_dropdown_inputs)
def update_mtd_site_covers(shift,area,measure,metric,site):
    return sales_site_covers_graph(shift,metric,site,'mtd')
    
@app.callback(Output('mtd site spend', 'figure'),mtd_dropdown_inputs)
def update_mtd_site_spend(shift,area,measure,metric,site):
    return sales_site_spend_graph(shift,metric,site,'mtd')

@app.callback(Output('mtd week view', 'figure'),mtd_week_dropdown_inputs)
def update_mtd_week_view(site,area,category,measure,metric,weekmetric):
    return sales_week_view_graph(site, area, category, measure, metric, weekmetric, 'mtd')

@app.callback(Output('mtd week covers', 'figure'),mtd_week_dropdown_inputs)
def update_mtd_week_covers(site,area,category,measure,metric,weekmetric):
    return sales_week_covers_graph(site, area, measure, metric, weekmetric, 'mtd')

# Weekly Sales

@app.callback(Output('weekly site dropdown', 'options'),
              [Input('weekly shift dropdown', 'options')])
def update_weekly_site_dropdown(shift):
    return [{'label':i,'value':i} for i in user_restaurants[auth._username]['sales']]

@app.callback(Output('weekly site dropdown', 'value'),
              [Input('weekly site dropdown', 'options')])
def set_weekly_site_dropdown_value(available_options):
    return available_options[0]['value']

@app.callback(Output('weekly site week dropdown', 'options'),
              [Input('weekly shift dropdown', 'options')])
def update_weekly_site_week_dropdown(shift):
    return [{'label':i,'value':i} for i in ['Group'] + user_restaurants[auth._username]['sales']]

@app.callback(Output('weekly sales total', 'figure'), weekly_dropdown_inputs)
def update_weekly_sales_total(shift,area,measure,metric,site):
    return sales_breakdown_graph(shift,area,measure,metric,'weekly')
    
@app.callback(Output('weekly group revenue', 'figure'),weekly_dropdown_inputs)
def update_weekly_group_revenue(shift,area,measure,metric,site):
    return sales_group_revenue_graph(shift,metric,'weekly')
    
@app.callback(Output('weekly group covers', 'figure'),weekly_dropdown_inputs)
def update_weekly_group_covers(shift,area,measure,metric,site):
    return sales_group_covers_graph(shift,metric,'weekly')

@app.callback(Output('weekly group spend', 'figure'),weekly_dropdown_inputs)
def update_weekly_group_spend(shift,area,measure,metric,site):
    return sales_group_spend_graph(shift,metric,'weekly')

@app.callback(Output('weekly site revenue', 'figure'),weekly_dropdown_inputs)
def update_weekly_site_revenue(shift,area,measure,metric,site):
    return sales_site_revenue_graph(shift,metric,site,'weekly')

@app.callback(Output('weekly site covers', 'figure'),weekly_dropdown_inputs)
def update_weekly_site_covers(shift,area,measure,metric,site):
    return sales_site_covers_graph(shift,metric,site,'weekly')
    
@app.callback(Output('weekly site spend', 'figure'),weekly_dropdown_inputs)
def update_weekly_site_spend(shift,area,measure,metric,site):
    return sales_site_spend_graph(shift,metric,site,'weekly')

@app.callback(Output('weekly week view', 'figure'),weekly_week_dropdown_inputs)
def update_weekly_week_view(site,area,category,measure,metric,weekmetric):
    return sales_week_view_graph(site, area, category, measure, metric, weekmetric, 'weekly')

@app.callback(Output('weekly week covers', 'figure'),weekly_week_dropdown_inputs)
def update_weekly_week_covers(site,area,category,measure,metric,weekmetric):
    return sales_week_covers_graph(site, area, measure, metric, weekmetric, 'weekly')

# Monthly Sales

@app.callback(Output('monthly site dropdown', 'options'),
              [Input('monthly shift dropdown', 'options')])
def update_monthly_site_dropdown(shift):
    return [{'label':i,'value':i} for i in user_restaurants[auth._username]['sales']]

@app.callback(Output('monthly site dropdown', 'value'),
              [Input('monthly site dropdown', 'options')])
def set_monthly_site_dropdown_value(available_options):
    return available_options[0]['value']

@app.callback(Output('monthly site week dropdown', 'options'),
              [Input('monthly shift dropdown', 'options')])
def update_monthly_site_week_dropdown(shift):
    return [{'label':i,'value':i} for i in ['Group'] + user_restaurants[auth._username]['sales']]

@app.callback(Output('monthly sales total', 'figure'), monthly_dropdown_inputs)
def update_monthly_sales_total(shift,area,measure,metric,site):
    return sales_breakdown_graph(shift,area,measure,metric,'monthly')
    
@app.callback(Output('monthly group revenue', 'figure'),monthly_dropdown_inputs)
def update_monthly_group_revenue(shift,area,measure,metric,site):
    return sales_group_revenue_graph(shift,metric,'monthly')
    
@app.callback(Output('monthly group covers', 'figure'),monthly_dropdown_inputs)
def update_monthly_group_covers(shift,area,measure,metric,site):
    return sales_group_covers_graph(shift,metric,'monthly')

@app.callback(Output('monthly group spend', 'figure'),monthly_dropdown_inputs)
def update_monthly_group_spend(shift,area,measure,metric,site):
    return sales_group_spend_graph(shift,metric,'monthly')

@app.callback(Output('monthly site revenue', 'figure'),monthly_dropdown_inputs)
def update_monthly_site_revenue(shift,area,measure,metric,site):
    return sales_site_revenue_graph(shift,metric,site,'monthly')

@app.callback(Output('monthly site covers', 'figure'),monthly_dropdown_inputs)
def update_monthly_site_covers(shift,area,measure,metric,site):
    return sales_site_covers_graph(shift,metric,site,'monthly')
    
@app.callback(Output('monthly site spend', 'figure'),monthly_dropdown_inputs)
def update_monthly_site_spend(shift,area,measure,metric,site):
    return sales_site_spend_graph(shift,metric,site,'monthly')

@app.callback(Output('monthly week view', 'figure'),monthly_week_dropdown_inputs)
def update_monthly_week_view(site,area,category,measure,metric,weekmetric):
    return sales_week_view_graph(site, area, category, measure, metric, weekmetric,'monthly')

@app.callback(Output('monthly week covers', 'figure'),monthly_week_dropdown_inputs)
def update_monthly_week_covers(site,area,category,measure,metric,weekmetric):
    return sales_week_covers_graph(site, area, measure, metric, weekmetric, 'monthly')

# Tracker

@app.callback(Output('tracker_site_dropdown', 'options'),
              [Input('tracker_week_dropdown', 'options')])
def update_tracker_site_dropdown(week):
    return [{'label':i,'value':i} for i in user_restaurants[auth._username]['bookings']]

@app.callback(Output('tracker_site_dropdown', 'value'),
              [Input('tracker_site_dropdown', 'options')])
def set_tracker_site_dropdown_value(available_options):
    return available_options[0]['value']

@app.callback(Output('tracker_group_8_weeks', 'figure'),tracker_dropdown_inputs)
def update_tracker_group_8_weeks(week,metric,site):
    return tracker_group_8_weeks_graph(week,metric,site, tracker_df, 'Booked Covers')
    
@app.callback(Output('tracker_group_week', 'figure'),tracker_dropdown_inputs)
def update_tracker_group_week(week,metric,site):
    return tracker_group_week_graph(week, metric, site, tracker_df, 'Booked Covers')

@app.callback(Output('tracker_site_8_weeks', 'figure'),tracker_dropdown_inputs)
def update_tracker_site_8_weeks(week,metric,site):
    return tracker_site_8_weeks_graph(week, metric, site, tracker_df, 'Booked Covers')
    
@app.callback(Output('tracker_site_week', 'figure'),tracker_dropdown_inputs)
def update_tracker_site_week(week,metric,site):
    return tracker_site_week_graph(week, metric, site, tracker_df, 'Booked Covers')
    
@app.callback(Output('tracker_breakdown', 'figure'),tracker_dropdown_inputs)
def update_tracker_breakdown(week,metric,site):
    return tracker_breakdown_graph(week, metric, site, tracker_df, 'Booked Covers')

# Pickup

@app.callback(Output('pickup_site_dropdown', 'options'),
              [Input('pickup_week_dropdown', 'options')])
def update_pickup_site_dropdown(week):
    return [{'label':i,'value':i} for i in user_restaurants[auth._username]['bookings']]

@app.callback(Output('pickup_site_dropdown', 'value'),
              [Input('pickup_site_dropdown', 'options')])
def set_pickup_site_dropdown_value(available_options):
    return available_options[0]['value']

@app.callback(Output('pickup_group_8_weeks', 'figure'),pickup_dropdown_inputs)
def update_pickup_group_8_weeks(week,metric,site):
    return tracker_group_8_weeks_graph(week,metric,site, pickup_df, 'Pickup')
    
@app.callback(Output('pickup_group_week', 'figure'),pickup_dropdown_inputs)
def update_pickup_group_week(week,metric,site):
    return tracker_group_week_graph(week, metric, site, pickup_df, 'Pickup')

@app.callback(Output('pickup_site_8_weeks', 'figure'),pickup_dropdown_inputs)
def update_pickup_site_8_weeks(week,metric,site):
    return tracker_site_8_weeks_graph(week, metric, site, pickup_df, 'Pickup')
    
@app.callback(Output('pickup_site_week', 'figure'),pickup_dropdown_inputs)
def update_pickup_site_week(week,metric,site):
    return tracker_site_week_graph(week, metric, site, pickup_df, 'Pickup')
    
@app.callback(Output('pickup_breakdown', 'figure'),pickup_dropdown_inputs)
def update_pickup_breakdown(week,metric,site):
    return tracker_breakdown_graph(week, metric, site, pickup_df, 'Pickup')


# Future Bookings

@app.callback(Output('future graph', 'figure'),
              [Input('future dropdown', 'value')])
def update_daily_site_dropdown(metric):
    if metric == 'Total Bookings':
        return future_totals_figure(user_restaurants[auth._username]['bookings'],future_df)
    else:
        return future_changes_figure(user_restaurants[auth._username]['bookings'],future_df)
    
    
# Booking Trends
    
@app.callback(Output('trends site dropdown', 'options'),
              [Input('textarea-example', 'value')])
def update_daily_site_dropdown(shift):
    return [{'label':i,'value':i} for i in user_restaurants[auth._username]['bookings']]

@app.callback(Output('trends site dropdown', 'value'),
              [Input('trends site dropdown', 'options')])
def set_daily_site_dropdown_value(available_options):
    return available_options[0]['value']

@app.callback(Output('trends site pickup', 'figure'),
             [Input('trends site dropdown', 'value')])
def update_site_pickup(site):
    return trends_site_pickup_figure(trends_df,site,today_week,today_weekday_num)

@app.callback(Output('trends site future', 'figure'),
             [Input('trends site dropdown', 'value')])
def update_site_future(site):
    return trends_site_future_figure(trends_df,site,today_week,today_weekday_num)
