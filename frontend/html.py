import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from datetime import date, datetime, timedelta

from authentication.users import sales_restaurants, user_restaurants
from authentication.authentication import auth

from frontend.plots.figures import trends_group_pickup_figure, trends_group_future_figure
from data.data import trends_df

def div_style_simple(width):
    
    return {
        'textAlign':'center',
        'display': 'inline-block',
        'width':width,
        'align-items':'center',
        'justify-content':'center',
    }


# Titles

def render_h1(text):
        
    style={
        'textAlign':"center",
        'background-color': 'snow',
    }
    
    if text== 'Next 4 Weeks':
        return html.H1(
            [text],
            id = 'homepage title',
            style = style
        )
        
    else:
        return html.H1(
            [text],
            style = style
        )
    
def title_div(text):
    
    h1 = render_h1(text)
    
    return html.Div([h1], style={'padding':'5px'})
    
    
def sales_title_div(report):
    
    if report in ['wtd', 'mtd']:
        title_string = report.upper()
    else:
        title_string = report.capitalize()
    
    return title_div(title_string)
    

def homepage_title_div(text):
    
    h1 = render_h1(text)
    style = {'width':'50%','display':'inline-block'}
    
    return html.Div([h1], style = style)
            

# Dropdowns

metrics = ['vs. LW','vs. LY', 'Totals Last Week', 'Totals Last Year']
default_metric_index = 1

dropdown_values = {
    'restaurants':sales_restaurants,
    'restaurants_week': ['Group'] + sales_restaurants,
    'shifts':['All Shifts', 'Lunch', 'Dinner'],
    'measures':['Revenue', 'Covers', 'Spend'],
    'areas':["Full Site", "Restaurant", "Bar", "PDR", "Events & Ex Hires", "Retail & Other"],
    'types':["Total", "Food",  "Beverage", "Wine", "Non-Wine"]
}

def render_dropdown(dropdown_id, values, initial_value, style):
    
    return dcc.Dropdown(
        id = dropdown_id,
        options = [{'label':i, 'value':i} for i in values],
        value = initial_value,
        style = style
    )

def render_bare_dropdown_div(dropdown, style):
    
    return html.Div(
        [dropdown],
        style = style
    )

def render_dropdown_div(p_string, dropdowns, style):
    
    return html.Div(
        [html.P([p_string])] + dropdowns,
        style = style
    )

def render_dropdown_row(dropdowns):
    
    style={
        'border-radius': '15px',
        'box-shadow': '8px 8px 8px grey',
        'background-color': '#f9f9f9',
        'padding': '10px 5px',
    }
    
    return html.Div(
        dropdowns,
        style = style
    )

def render_flex_dropdown_row(dropdowns):
    
    style = {
        'width': '100%', 
        'display': 'flex', 
        'align-items': 'center', 
        'justify-content': 'center',
        'border-radius': '15px',
        'box-shadow': '8px 8px 8px grey',
        'background-color': '#f9f9f9',
        'padding': '10px 5px',
    }
    
    return html.Div(
        dropdowns,
        style = style
    )

def homepage_sales_dropdown():    
    
    dropdown_width = '90%'
    dropdown_height = '20px'
    div_width = '25%'
    margin = '0px 0px 0px 20px'
    font_size = '20px'
    
    dropdown_style = {
        'width':dropdown_width,
        'height':dropdown_height,
#         'line-height':line_height,
        'margin':margin,
        'font-size':font_size,
    }
    div_style = div_style_simple(div_width)
    
    metrics = ['Daily Sales','WTD Sales','MTD Sales', '4Wks Sales']
    
#     Dropdown
    
    def homepage_sales_dropdown():
        
        dropdown_id = 'homepage sales dropdown'
        values = metrics
        initial_value = 'Daily Sales'
        style = dropdown_style
        
        return render_dropdown(dropdown_id, values, initial_value, style)
    
#     Div
    
    def homepage_sales_dropdown_div():
        
        dropdown = homepage_sales_dropdown()
        style = div_style
        
        return render_bare_dropdown_div(dropdown, style)
        
    return homepage_sales_dropdown_div()
    
    

def core_dropdowns(report):    
    
    dropdown_width = '99%'
    div_width = '50%'
    
    dropdown_style = {'width':dropdown_width}
    div_style = div_style_simple(div_width)
    
    metrics = ['vs. LW','vs. LY', 'Totals Last Week', 'Totals Last Year']
    
#     Dropdowns
    
    def metric_dropdown(report):
        
        dropdown_id = report + ' metric dropdown'
        values = metrics
        initial_value = metrics[default_metric_index]
        style = dropdown_style
        
        return render_dropdown(dropdown_id, values, initial_value, style)
    
    def measure_dropdown(report):
        
        dropdown_id = report + ' measure dropdown'
        values = ['Revenue', 'Covers']
        initial_value = 'Revenue'
        style = dropdown_style
        
        return render_dropdown(dropdown_id, values, initial_value, style)
    
    def site_dropdown(report):
        
        dropdown_id = report + ' site dropdown'
        values = dropdown_values['restaurants']
        initial_value = dropdown_values['restaurants'][0]
        style = dropdown_style
        
        return render_dropdown(dropdown_id, values, initial_value, style)
    
#     Divs
    
    def metric_dropdown_div(report):
        
        p_string = 'Choose the metric of the report:'
        dropdowns = [metric_dropdown(report)]
        style = div_style
        
        return render_dropdown_div(p_string, dropdowns, style)
    
    
    def measure_dropdown_div(report):
        
        p_string = 'Choose the measure of the sales graphs:'
        dropdowns = [measure_dropdown(report)]
        style = div_style
        
        return render_dropdown_div(p_string, dropdowns, style)
    
    def site_dropdown_div(report):
        
        p_string = 'Choose the restaurant of the report:'
        dropdowns = [site_dropdown(report)]
        style = div_style
        
        return render_dropdown_div(p_string, dropdowns, style)
    
    if report == 'group' or report == 'breakdown':
        dropdowns = [metric_dropdown_div(report), measure_dropdown_div(report)]
    elif report == 'restaurant':
        dropdowns = [metric_dropdown_div(report), site_dropdown_div(report)]
        
    return render_dropdown_row(dropdowns)
    
def sales_overview_dropdowns(report):
    
    dropdown_width = '99%'
    div_width = '33%'
    bottom_padding = '2px 0px'
    
    dropdown_style = {'width':dropdown_width}
    bottom_dropdown_style = {'width':dropdown_width, 'padding':bottom_padding}
    div_style = div_style_simple(div_width)
    
    week_metrics = ['vs. LW','vs. LY', 'Totals Last Week', 'Totals Last Year']
    month_metrics = ['vs. LM','vs. LY', 'Totals Last Month', 'Totals Last Year']
    
    week_reports = ['daily','wtd','weekly']
    month_reports = ['mtd','monthly']

    if report in week_reports:
        metrics = week_metrics
    elif report in month_reports:
        metrics = month_metrics
    
#     Dropdowns
    
    def metric_dropdown(report):
        
        dropdown_id = report + ' metric dropdown'
        values = metrics
        initial_value = metrics[default_metric_index]
        style = dropdown_style
        
        return render_dropdown(dropdown_id, values, initial_value, style)
    
    def shift_dropdown(report):
        
        dropdown_id = report + ' shift dropdown'
        values = dropdown_values['shifts']
        initial_value = 'All Shifts'
        style = bottom_dropdown_style
        
        return render_dropdown(dropdown_id, values, initial_value, style)
    
    def area_dropdown(report):
        
        dropdown_id = report + ' area dropdown'
        values = dropdown_values['areas']
        initial_value = 'Full Site'
        style = dropdown_style
        
        return render_dropdown(dropdown_id, values, initial_value, style)
    
    def measure_dropdown(report):
        
        dropdown_id = report + ' measure dropdown'
        values = dropdown_values['measures']
        initial_value = 'Revenue'
        style = bottom_dropdown_style
        
        return render_dropdown(dropdown_id, values, initial_value, style)
    
    def site_dropdown(report):
        
        dropdown_id = report + ' site dropdown'
        values = dropdown_values['restaurants']
        initial_value = dropdown_values['restaurants'][0]
        style = dropdown_style
        
        return render_dropdown(dropdown_id, values, initial_value, style)
    
#     Divs

    def metric_and_shift_dropdown_div(report):
        
        p_string = 'Choose the metric and shift of the report:'
        dropdowns = [metric_dropdown(report), shift_dropdown(report)]
        style = div_style
        
        return render_dropdown_div(p_string, dropdowns, style)

    def area_and_measure_dropdown_div(report):
        
        p_string = 'Choose the area and measure of the group_summary:'
        dropdowns = [area_dropdown(report), measure_dropdown(report)]
        style = div_style
        
        return render_dropdown_div(p_string, dropdowns, style)
    
    def site_dropdown_div(report):
        
        p_string = 'Choose the restaurant of the site analysis:'
        dropdowns = [site_dropdown(report)]
        style = div_style
        
        return render_dropdown_div(p_string, dropdowns, style)
    
    dropdowns = [
        metric_and_shift_dropdown_div(report), 
        area_and_measure_dropdown_div(report), 
        site_dropdown_div(report)
    ]
    
    return render_dropdown_row(dropdowns)
    
def sales_week_dropdowns(report):
    
    dropdown_width = '99%'
    div_width = '20%'
    
    dropdown_style = {'width':dropdown_width}
    div_style = {
        'textAlign':'center',
        'display': 'inline-block',
        'width':div_width
    }
    
    week_metrics = ['vs. LW','vs. LY', 'Totals Last Week', 'Totals Last Year']
    month_metrics = ['vs. LM','vs. LY', 'Totals Last Month', 'Totals Last Year']
    
    week_reports = ['daily','wtd','weekly']
    month_reports = ['mtd','monthly']

    if report in week_reports:
        metrics = week_metrics
    elif report in month_reports:
        metrics = month_metrics
    
#     Dropdowns
    
    def site_dropdown(report):
        
        dropdown_id = report + ' site week dropdown'
        values = dropdown_values['restaurants_week']
        initial_value = 'Group'
        style = dropdown_style
        
        return render_dropdown(dropdown_id, values, initial_value, style)
    
    def area_dropdown(report):
        
        dropdown_id = report + ' area week dropdown'
        values = dropdown_values['areas']
        initial_value = 'Full Site'
        style = dropdown_style
        
        return render_dropdown(dropdown_id, values, initial_value, style)
    
    def category_dropdown(report):
        
        dropdown_id = report + ' category week dropdown'
        values = dropdown_values['types']
        initial_value = 'Total'
        style = dropdown_style
        
        return render_dropdown(dropdown_id, values, initial_value, style)
    
    def measure_dropdown(report):
        
        dropdown_id = report + ' measure week dropdown'
        values = ['Revenue','Spend']
        initial_value = 'Revenue'
        style = dropdown_style
        
        return render_dropdown(dropdown_id, values, initial_value, style)
    
    def metric_dropdown(report):
        
        dropdown_id = report + ' metric week dropdown'
        values = ['Actuals','Averages']
        initial_value = 'Actuals'
        style = dropdown_style
        
        return render_dropdown(dropdown_id, values, initial_value, style)
    
#     Divs
    
    def site_dropdown_div(report):
        
        p_string = 'Choose the restaurant of the week view:'
        dropdowns = [site_dropdown(report)]
        style = div_style
        
        return render_dropdown_div(p_string, dropdowns, style)
    
    def area_dropdown_div(report):
        
        p_string = 'Choose the area of the week view:'
        dropdowns = [area_dropdown(report)]
        style = div_style
        
        return render_dropdown_div(p_string, dropdowns, style)
    
    def category_dropdown_div(report):
        
        p_string = 'Choose the revenue category of the week view:'
        dropdowns = [category_dropdown(report)]
        style = div_style
        
        return render_dropdown_div(p_string, dropdowns, style)
    
    def measure_dropdown_div(report):
        
        p_string = 'Choose the measure of the week view:'
        dropdowns = [measure_dropdown(report)]
        style = div_style
        
        return render_dropdown_div(p_string, dropdowns, style)
    
    def metric_dropdown_div(report):
        
        p_string = 'Choose the metric of the week view:'
        dropdowns = [metric_dropdown(report)]
        style = div_style
        
        return render_dropdown_div(p_string, dropdowns, style)
    
    dropdowns = [
        site_dropdown_div(report), 
        area_dropdown_div(report), 
        category_dropdown_div(report),
        measure_dropdown_div(report),
        metric_dropdown_div(report),
    ]
    
    return render_dropdown_row(dropdowns)

def tracker_dropdowns(report):    
    
    dropdown_width = '99%'
    div_width = '33%'
    
    dropdown_style = {'width':dropdown_width}
    div_style = div_style_simple(div_width)
    
    weeks = [
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
    
    metrics = [
        'vs. LW',
        'vs. LY',
        'Totals Last Week',
        'Totals Last Year'
    ]
    
#     Dropdowns
    
    def metric_dropdown(report):
        
        dropdown_id = report + '_metric_dropdown'
        values = metrics
        initial_value = metrics[default_metric_index]
        style = dropdown_style
        
        return render_dropdown(dropdown_id, values, initial_value, style)
    
    def week_dropdown(report):
        
        dropdown_id = report + '_week_dropdown'
        values = weeks
        initial_value = 'This Week'
        style = dropdown_style
        
        return render_dropdown(dropdown_id, values, initial_value, style)
    
    def site_dropdown(report):
        
        dropdown_id = report + '_site_dropdown'
        values = dropdown_values['restaurants']
        initial_value = dropdown_values['restaurants'][0]
        style = dropdown_style
        
        return render_dropdown(dropdown_id, values, initial_value, style)
    
#     Divs
    
    def metric_dropdown_div(report):
        
        p_string = 'Choose the metric of the report:'
        dropdowns = [metric_dropdown(report)]
        style = div_style
        
        return render_dropdown_div(p_string, dropdowns, style)
    
    def week_dropdown_div(report):
        
        p_string = 'Choose the week of the report:'
        dropdowns = [week_dropdown(report)]
        style = div_style
        
        return render_dropdown_div(p_string, dropdowns, style)
    
    def site_dropdown_div(report):
        
        p_string = 'Choose the restaurant of the site analysis:'
        dropdowns = [site_dropdown(report)]
        style = div_style
        
        return render_dropdown_div(p_string, dropdowns, style)
    
    dropdowns = [
        metric_dropdown_div(report), 
        week_dropdown_div(report),
        site_dropdown_div(report)
    ]
        
    return render_dropdown_row(dropdowns)

def future_dropdowns():    
    
    dropdown_style = {
        'textAlign':'center',
        'width':'99%'
    }
    div_style = {
        'width': '100%',
    }
    
#     Dropdowns
    
    def metric_dropdown():
        
        dropdown_id = 'future dropdown'
        values = ['Total Bookings', 'vs. LW']
        initial_value = ['Total Bookings']
        style = dropdown_style
        
        return render_dropdown(dropdown_id, values, initial_value, style)
    
#     Divs
    
    def metric_dropdown_div():
        
        p_string = 'Choose the metric of the report:'
        dropdowns = [metric_dropdown()]
        style = div_style
        
        return render_dropdown_div(p_string, dropdowns, style)
    
    dropdowns = [metric_dropdown_div()]
        
    return render_flex_dropdown_row(dropdowns)

def trends_dropdowns():    
    
    dropdown_style = {'textAlign':'center','width':'99%',}
    div_style = {'width': '100%'}
    
#     Dropdowns
    
    def site_dropdown():
        
        dropdown_id = 'trends site dropdown'
        values = user_restaurants['dandd']['bookings']
        initial_value = user_restaurants['dandd']['bookings'][0]
        style = dropdown_style
        
        return render_dropdown(dropdown_id, values, initial_value, style)
    
#     Divs
    
    def site_dropdown_div():
        
        p_string = 'Choose the restaurant of the right-hand graphs:'
        dropdowns = [site_dropdown()]
        style = div_style
        
        return render_dropdown_div(p_string, dropdowns, style)
    
    dropdowns = [site_dropdown_div()]
        
    return render_flex_dropdown_row(dropdowns)


# Graphs

def render_graph(graph_id, height, width):
    
    return dcc.Graph(
        id=graph_id,
        style={
            'height':height,
            'width':width,
            'border-radius': '15px',
            'box-shadow': '8px 8px 8px grey',
            'background-color': '#f9f9f9',
            'padding': '5px',
            'margin': '5px'
        },
        config={'displayModeBar':False}
    )

def render_trends_group_graph(graph_id, func):

    today_weekday_num = date.today().weekday()
    today_week = date.today().isocalendar()[1]
    
    return dcc.Graph(
        id = graph_id,
        figure = func(
            trends_df,
            today_week,
            today_weekday_num
        ),
        config = {'displayModeBar':False}
    )

def render_click_data_graph(graph_id, click_data, height, width):
    
    return dcc.Graph(
        id=graph_id,
        clickData=click_data,
        style={
            'height':height,
            'width':width,
            'border-radius': '15px',
            'box-shadow': '8px 8px 8px grey',
            'background-color': '#f9f9f9',
            'padding': '5px',
            'margin': '5px'
        },
        config={'displayModeBar':False}
    )

def standard_graph(graph_id):
    
    height = '100%'
    width = '100%'
    
    return render_graph(graph_id, height, width)

def small_graph(graph_id):
    
    height = 300
    width = '100%'
    
    return render_graph(graph_id, height, width)

def week_graph(graph_id):
    
    height = 450
    width = '100%'
    
    return render_graph(graph_id, height, width)

def tracker_graph(graph_id):
    
    height = '50%'
    width = '100%'
    
    return render_graph(graph_id, height, width)

def click_data_graph(graph_id, click_data):
    
    height = '100%'
    width = '100%'
    
    return render_click_data_graph(graph_id, click_data, height, width)

def homepage_small_graph(graph_id):
    
    height = '50%'
    width = '100%'
    
    return render_graph(graph_id, height, width)


# Divs

def render_div(graphs_list, height, width):
    
    return html.Div(
        graphs_list,
        style = {
            'display':'inline-block',
            'height':height,
            'width':width,
            'padding':'10px',
        }
    )

def render_flex_div(graphs_list):
    
    return html.Div(
        graphs_list,
        style = {
            'width': '100%', 
            'display': 'flex', 
            'align-items': 'center', 
            'justify-content': 'center'
        }
    )        


# Sales

# Overview

def sales_overview_div(report, graphs_list):
    
    height = 900
    width = '33%'
    
    return render_div(graphs_list, height, width)

def sales_measures_div(report, site_scope):
    
    measures = ['revenue','covers','spend']
    graphs_list = [small_graph(report + ' ' + site_scope + ' ' + measure) for measure in measures]
    
    return sales_overview_div(report, graphs_list)

def sales_breakdown_div(report):
    
    graphs_list = standard_graph(report + ' sales total')
    
    return sales_overview_div(report, graphs_list)

# Week

def sales_week_div(graph_id):
    
    height = 450
    width = '50%'
    graphs_list = [week_graph(graph_id)]
    
    return render_div(graphs_list, height, width)


#  Tracker

def tracker_div(report, graphs_list):
    
    height = 900
    width = '33%'
    
    return render_div(graphs_list, height, width)

def tracker_site_div(report, site_scope):
    
    week_scopes = ['8_weeks','week']
    graphs_list = [tracker_graph(report + '_' + site_scope + '_' + week_scope) for week_scope in week_scopes]
    
    return tracker_div(report, graphs_list)

def tracker_breakdown_div(report):
    
    graphs_list = standard_graph(report + '_breakdown')
    
    return tracker_div(report, graphs_list)


# Future

def future_div():
    
    graph = standard_graph('future graph')
    
    return html.Div(
        [graph],
        style = {
            'width': '100%', 
            'display': 'flex', 
            'align-items': 'center', 
            'justify-content': 'center'
        }
    )


# Trends

def trends_div(graphs_list):
    
    height = 400
    width = '50%'
    
    return render_div(graphs_list, height, width)

def trends_row(report):
    
    if report == 'pickup':
        group_func = trends_group_pickup_figure
    elif report == 'future':
        group_func = trends_group_future_figure
        
    group_graph = render_trends_group_graph('trends group ' + report, group_func)
    site_graph = standard_graph('trends site ' + report)
    
    group_div = trends_div([group_graph])
    site_div = trends_div([site_graph])
    
    return html.Div([group_div, site_div])


# Group

def group_future_div(graph_id):
    
    graph = standard_graph(graph_id)
    
    return render_flex_div([graph])

def group_sales_div(graph_id):
    
    height = 300
    width = '33%'
    graphs_list = [small_graph(graph_id)]
    
    return render_div(graphs_list, height, width)

def group_tracker_div(graph_id):
    
    height = 350
    width = '50%'
    graphs_list = [standard_graph(graph_id)]
    
    return render_div(graphs_list, height, width)

def group_review_div(graph_id):
    
    height = 350
    width = '20%'
    graphs_list = [standard_graph(graph_id)]
    
    return render_div(graphs_list, height, width)


# Breakdown

def breakdown_sales_div(graph_id):
    
    height = 900
    width = '33%'
    graphs_list = [standard_graph(graph_id)]
    
    return render_div(graphs_list, height, width)

def breakdown_tracker_div(graph_id):
    
    height = 1000
    width = '33%'
    graphs_list = [standard_graph(graph_id)]
    
    return render_div(graphs_list, height, width)

def breakdown_review_div(graph_id):
    
    height = 300
    width = '100%'
    graphs_list = [standard_graph(graph_id)]
    
    return render_div(graphs_list, height, width)

def breakdown_future_div(graph_id):
    
    height = 1000
    width = '33%'
    graphs_list = [standard_graph(graph_id)]
    
    return render_div(graphs_list, height, width)


# Homepage


def homepage_div(graph_ids):
    
    height = 400
    width = '25%'
    graphs_list = [standard_graph(graph_id)]
    
    return render_div(graphs_list, height, width)

def homepage_click_div(graph_id):
    
    height = 400
    width = '23%'
    click_data = {'points':[{'y':'Group'}]}
    graphs_list = [click_data_graph(graph_id, click_data)]
    
    return render_div(graphs_list, height, width)

def homepage_split_div(graph_ids):
    
    height = 800
    width = '25%'
    graphs_list = [homepage_small_graph(graph_id) for graph_id in graph_ids]
    
    return render_div(graphs_list, height, width)

def homepage_sites_div(graph_id):
    
    height = 800
    width = '23%'
    graphs_list = [standard_graph(graph_id)]
    
    return render_div(graphs_list, height, width)

def homepage_wide_div(graph_id):
    
    height = 800
    width = '50%'
    graphs_list = [standard_graph(graph_id)]
    
    return render_div(graphs_list, height, width)