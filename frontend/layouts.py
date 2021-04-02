import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from datetime import date, datetime, timedelta

from frontend.html import *
# from frontend.styling import *
# from authentication.users import user_restaurants
# from authentication.authentication import auth

# from frontend.plots.figures import trends_group_pickup_figure, trends_group_future_figure
# from data.data import trends_df

def homepage():
    
    homepage_titles = html.Div(
        [
            homepage_title_div('Next 4 Weeks'),
            homepage_title_div('Last 4 Weeks'),
        ]
    )

    homepage_summary_graphs = html.Div(
        [
            homepage_div('homepage future summary'),
            homepage_div('homepage tracker summary'),
            homepage_div('homepage revenue summary'),
            homepage_div('homepage score summary'),
        ]
    )
    
    homepage_worst_graphs = html.Div(
        [
            homepage_div('homepage future worst'),
            homepage_div('homepage tracker worst'),
            homepage_div('homepage revenue worst'),
            homepage_div('homepage score worst'),
        ]
    )
    
    return html.Div(
        children=[
            homepage_titles,
            homepage_summary_graphs,
            homepage_worst_graphs
        ]
    )

def group():
        
    group_dropdowns = core_dropdowns('group')
    
    group_future_graph = group_future_div('group future')
    
    group_sales_graphs = html.Div(
        [
            group_sales_div('group daily sales'),
            group_sales_div('group wtd sales'),
            group_sales_div('group mtd sales'),
        ]
    )
    
    group_spend_graphs = html.Div(
        [
            group_sales_div('group daily spend'),
            group_sales_div('group wtd spend'),
            group_sales_div('group mtd spend'),
        ]
    )
    
    group_tracker_graphs = html.Div(
        [
            group_tracker_div('group tracker'),
            group_tracker_div('group pickup'),
        ]
    )
    
    group_review_graphs = html.Div(
        [
            group_review_div('group overall'),
            group_review_div('group food'),
            group_review_div('group service'),
            group_review_div('group ambience'),
            group_review_div('group value'),
        ]
    )
    
    return html.Div(
        children=[
            group_dropdowns, 
            group_future_graph, 
            group_tracker_graphs, 
            group_sales_graphs,
            group_spend_graphs,
            group_review_graphs
        ]
    )


def breakdown():
    
    breakdown_dropdowns =  core_dropdowns('breakdown')
    
    breakdown_sales_graphs = html.Div(
        [
            breakdown_sales_div('breakdown daily sales'),
            breakdown_sales_div('breakdown wtd sales'),
            breakdown_sales_div('breakdown mtd sales'),
        ]
    )
    
    breakdown_tracker_graphs = html.Div(
        [
            breakdown_tracker_div('breakdown this week tracker'),
            breakdown_tracker_div('breakdown next week tracker'),
            breakdown_tracker_div('breakdown two weeks tracker'),
        ]
    )
    
    breakdown_future_graphs = html.Div(
        [
            breakdown_future_div('breakdown this week future'),
            breakdown_future_div('breakdown next week future'),
            breakdown_future_div('breakdown two weeks future'),
        ]
    )
    
    
    
    return html.Div(
        children=[
            breakdown_dropdowns,
            breakdown_future_graphs,
            breakdown_tracker_graphs, 
            breakdown_sales_graphs, 
            breakdown_review_div('breakdown overall'),
            breakdown_review_div('breakdown food'),
            breakdown_review_div('breakdown service'),
            breakdown_review_div('breakdown ambience'),
            breakdown_review_div('breakdown value')
        ]
    )
       
def restaurant():
    
    restaurant_dropdowns =  core_dropdowns('restaurant')
    
    restaurant_future_graph = group_future_div('restaurant future')
    
    restaurant_tracker_graphs = html.Div(
        [
            group_tracker_div('restaurant tracker'),
            group_tracker_div('restaurant pickup'),
        ]
    )
    
    restaurant_revenue_graphs = html.Div(
        [
            group_sales_div('restaurant daily sales'),
            group_sales_div('restaurant wtd sales'),
            group_sales_div('restaurant mtd sales'),
        ]
    )
    
    restaurant_spend_graphs = html.Div(
        [
            group_sales_div('restaurant daily spend'),
            group_sales_div('restaurant wtd spend'),
            group_sales_div('restaurant mtd spend'),
        ]
    )
    
    restaurant_review_graphs = html.Div(
        [
            group_review_div('restaurant overall'),
            group_review_div('restaurant food'),
            group_review_div('restaurant service'),
            group_review_div('restaurant ambience'),
            group_review_div('restaurant value'),
        ]
    )
    
    return html.Div(
        children=[
            restaurant_dropdowns, 
            restaurant_future_graph, 
            restaurant_tracker_graphs, 
            restaurant_revenue_graphs, 
            restaurant_spend_graphs,
            restaurant_review_graphs
        ]
    )

def sales_layout_template(report):
    
    title = sales_title_div(report)
    
    overview_dropdowns =  sales_overview_dropdowns(report)
    
    overview_graphs = html.Div(
        [
            sales_measures_div(report, 'group'),
            sales_breakdown_div(report),
            sales_measures_div(report, 'site'),
        ]
    )
    
    week_dropdowns = sales_week_dropdowns(report)
    
    week_graphs = html.Div(
        [
            sales_week_div(report + ' week view'),
            sales_week_div(report + ' week covers'),
        ]
    )
    
    if report == 'daily':
        layout = html.Div(children = [title, overview_dropdowns, overview_graphs])
    else:
        layout = html.Div(children = [title, overview_dropdowns, overview_graphs, week_dropdowns, week_graphs])
    
    return layout                             
    
def tracker_layout_template(report):
    
    if report == 'tracker':
        title_string = 'Cover Tracker'
    else:
        title_string = 'Daily Pickup'
        
    title = title_div(title_string)
    
    dropdowns = tracker_dropdowns(report)
    
    graphs = html.Div(
        [
            tracker_site_div(report, 'group'),
            tracker_breakdown_div(report),
            tracker_site_div(report, 'site')
        ]
    )
    
    return html.Div(children = [title, dropdowns, graphs])

def future():
    
    title = title_div('Future Bookings')
    
    dropdowns = future_dropdowns()
    
    graphs = future_div()
    
    return html.Div(
        children=[
            title,
            dropdowns,
            graphs
        ]
    )

def trends():
    
    title = title_div('Booking Trends')
    
    dropdowns = trends_dropdowns()
    
    pickup_row = trends_row('pickup')
    future_row = trends_row('future')
    
    return html.Div(
        children=[
            title,
            dropdowns,
            pickup_row,
            future_row
        ]
    )

homepage_layout = homepage()
group_layout = group()
breakdown_layout = breakdown()
restaurant_layout = restaurant()
daily_layout = sales_layout_template('daily')
wtd_layout = sales_layout_template('wtd')
mtd_layout = sales_layout_template('mtd')
weekly_layout = sales_layout_template('weekly')
monthly_layout = sales_layout_template('monthly')
tracker_layout = tracker_layout_template('tracker')
pickup_layout = tracker_layout_template('pickup')
future_layout = future()
trends_layout = trends()