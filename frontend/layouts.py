import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from datetime import date, datetime, timedelta

from frontend.styling import *
from authentication.users import user_restaurants
from authentication.authentication import auth

from frontend.plots.figures import trends_group_pickup_figure, trends_group_future_figure
from data.data import trends_df

default_metric = ['vs. LW']

def home_page():
    
    metrics = ['vs. LW','vs. LY', 'Totals Last Week', 'Totals Last Year']
    
    homepage_dropdowns =  html.Div(
        [
            html.Div(
                [
                    html.P(
                        ['Choose the metric of the report:']
                    ),
                    dcc.Dropdown(
                        id = 'homepage metric dropdown',
                        options = [{'label':i, 'value':i} for i in metrics],
                        value = metrics[default_metric_index],
                        style = {'width':dimensions['homepage']['dropdowns']['dropdown_width']}
                    ),
                ],
                style = div_style_simple(dimensions['homepage']['dropdowns']['div_width'])
            ),
            html.Div(
                [
                    html.P(
                        ['Choose the measure of the sales graphs:']
                    ),
                    dcc.Dropdown(
                        id = 'homepage measure dropdown',
                        options = [{'label':i,'value':i} for i in dropdown_values['measures']],
                        value = 'Revenue',
                        style = {
                            'width':dimensions['homepage']['dropdowns']['dropdown_width'],
                        }
                    )
                ],
                style = div_style_simple(dimensions['homepage']['dropdowns']['div_width'])
            ),
        ],
        style = dropdown_row_style
    )
    
    homepage_future_graph = html.Div(
        [
            dcc.Graph(
                id='homepage future',
                config={'displayModeBar':False},
                style={'width':'100%'}
            )
        ],
        style = {
            'width': '100%', 
            'display': 'flex', 
            'align-items': 'center', 
            'justify-content': 'center'
        }
    )
    
    homepage_sales_graphs = html.Div(
        [
            homepage_sales_div('homepage daily sales'),
            homepage_sales_div('homepage wtd sales'),
            homepage_sales_div('homepage mtd sales'),
        ]
    )
    
    homepage_tracker_graphs = html.Div(
        [
            homepage_tracker_div('homepage tracker'),
            homepage_tracker_div('homepage pickup'),
        ]
    )
    
    homepage_review_graphs = html.Div(
        [
            homepage_review_div('homepage overall'),
            homepage_review_div('homepage food'),
            homepage_review_div('homepage service'),
            homepage_review_div('homepage ambience'),
            homepage_review_div('homepage value'),
        ]
    )
    
    return html.Div(
        children=[
            homepage_dropdowns, 
            homepage_future_graph, 
            homepage_tracker_graphs, 
            homepage_sales_graphs,
            homepage_review_graphs
        ]
    )


def breakdown():
    
    metrics = ['vs. LW','vs. LY', 'Totals Last Week', 'Totals Last Year']
    
    breakdown_dropdowns =  html.Div(
        [
            html.Div(
                [
                    html.P(
                        ['Choose the metric of the report:']
                    ),
                    dcc.Dropdown(
                        id = 'breakdown metric dropdown',
                        options = [{'label':i, 'value':i} for i in metrics],
                        value = metrics[default_metric_index],
                        style = {'width':dimensions['homepage']['dropdowns']['dropdown_width']}
                    ),
                ],
                style = div_style_simple(dimensions['homepage']['dropdowns']['div_width'])
            ),
            html.Div(
                [
                    html.P(
                        ['Choose the measure of the sales graphs:']
                    ),
                    dcc.Dropdown(
                        id = 'breakdown measure dropdown',
                        options = [{'label':i,'value':i} for i in dropdown_values['measures']],
                        value = 'Revenue',
                        style = {
                            'width':dimensions['homepage']['dropdowns']['dropdown_width'],
                        }
                    )
                ],
                style = div_style_simple(dimensions['homepage']['dropdowns']['div_width'])
            ),
        ],
        style = dropdown_row_style
    )
    
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
    
    metrics = ['vs. LW','vs. LY', 'Totals Last Week', 'Totals Last Year']
    
    restaurant_dropdowns =  html.Div(
        [
            html.Div(
                [
                    html.P(
                        ['Choose the metric of the report:']
                    ),
                    dcc.Dropdown(
                        id = 'restaurant metric dropdown',
                        options = [{'label':i, 'value':i} for i in metrics],
                        value = metrics[default_metric_index],
                        style = {'width':dimensions['homepage']['dropdowns']['dropdown_width']}
                    ),
                ],
                style = div_style_simple(dimensions['homepage']['dropdowns']['div_width'])
            ),
            html.Div(
                [
                    html.P(
                        ['Choose the restaurant of the report:']
                    ),
                    dcc.Dropdown(
                        id = 'restaurant site dropdown',
                        options = [{'label':i,'value':i} for i in dropdown_values['restaurants']],
                        value = 'Revenue',
                        style = {
                            'width':dimensions['homepage']['dropdowns']['dropdown_width'],
                        }
                    )
                ],
                style = div_style_simple(dimensions['homepage']['dropdowns']['div_width'])
            ),
        ],
        style = dropdown_row_style
    )
    
    restaurant_revenue_graphs = html.Div(
        [
            homepage_sales_div('restaurant daily sales'),
            homepage_sales_div('restaurant wtd sales'),
            homepage_sales_div('restaurant mtd sales'),
        ]
    )
    
    restaurant_spend_graphs = html.Div(
        [
            homepage_sales_div('restaurant daily spend'),
            homepage_sales_div('restaurant wtd spend'),
            homepage_sales_div('restaurant mtd spend'),
        ]
    )
    
    restaurant_tracker_graphs = html.Div(
        [
            homepage_tracker_div('restaurant tracker'),
            homepage_tracker_div('restaurant pickup'),
        ]
    )
    
    restaurant_future_graph = html.Div(
        [
            dcc.Graph(
                id='restaurant future',
                config={'displayModeBar':False},
                style={'width':'100%'}
            )
        ],
        style = {
            'width': '100%', 
            'display': 'flex', 
            'align-items': 'center', 
            'justify-content': 'center'
        }
    )
    
    restaurant_review_graphs = html.Div(
        [
            homepage_review_div('restaurant overall'),
            homepage_review_div('restaurant food'),
            homepage_review_div('restaurant service'),
            homepage_review_div('restaurant ambience'),
            homepage_review_div('restaurant value'),
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
        
    week_metrics = ['vs. LW','vs. LY', 'Totals Last Week', 'Totals Last Year']
    month_metrics = ['vs. LM','vs. LY', 'Totals Last Month', 'Totals Last Year']
    
    week_reports = ['daily','wtd','weekly']
    month_reports = ['mtd','monthly']

    if report in week_reports:
        metrics = week_metrics
    elif report in month_reports:
        metrics = month_metrics
    
    title_string = capitalize_report_title(report)
    
    title = html.Div(
        [
            html.H1(
                children = title_string + ' Sales',
                style = h1_style
            )
        ]
    )
    
    summary_dropdowns =  html.Div(
        [
            html.Div(
                [
                    html.P(
                        ['Choose the metric and shift of the report:']
                    ),
                    dcc.Dropdown(
                        id = report + ' metric dropdown',
                        options = [{'label':i, 'value':i} for i in metrics],
                        value = metrics[default_metric_index],
                        style = {'width':dimensions['div']['dropdown_width']}
                    ),
                    dcc.Dropdown(
                        id = report + ' shift dropdown',
                        options = [{'label':i, 'value':i} for i in dropdown_values['shifts']],
                        value = 'All Shifts',
                        style = {
                            'width':dimensions['div']['dropdown_width'],
                            'padding':'2px 0px'
                        }
                    )
                ],
                style = div_style_simple(dimensions['div']['width'])
            ),
            html.Div(
                [
                    html.P(
                        ['Choose the area and measure of the group summary:']
                    ),
                    dcc.Dropdown(
                        id = report + ' area dropdown',
                        options = [{'label':i, 'value':i} for i in dropdown_values['areas']],
                        value = 'Full Site',
                        style = {'width':dimensions['div']['dropdown_width']}
                    ),
                    dcc.Dropdown(
                        id = report + ' measure dropdown',
                        options = [{'label':i,'value':i} for i in dropdown_values['measures']],
                        value = 'Revenue',
                        style = {
                            'width':dimensions['div']['dropdown_width'],
                            'padding':'2px 0px'
                        }
                    )
                ],
                style = div_style_simple(dimensions['div']['width'])
            ),
            html.Div(
                [
                    html.P(
                        ['Choose the restaurant of the site analysis:']
                    ),
                    dcc.Dropdown(
                        id = report + ' site dropdown',
                        options = [{'label':i, 'value':i} for i in dropdown_values['restaurants']],
                        value = '100 Wardour Street',
                        style = {'width': dimensions['div']['dropdown_width']}
                    )
                ],
                style = div_style_simple(dimensions['div']['width'])
            )
        ],
        style = dropdown_row_style
    )
    
    summary_graphs = html.Div(
        [
            html.Div(
                [
                    small_graph(report + ' group revenue'),
                    small_graph(report + ' group covers'),
                    small_graph(report + ' group spend')
                ],
                style = {
                    'display':'inline-block',
                    'height':dimensions['main']['height'],
                    'width':dimensions['main']['width']
                }
            ),
            html.Div(
                [
                    dcc.Graph(
                        id = report + ' sales total',
                        config = {'displayModeBar':False}
                    )
                ],    
                style = {
                    'display':'inline-block',
                    'height':dimensions['main']['height'],
                    'width':dimensions['main']['width']
                }
            ),
            html.Div(
                [
                    small_graph(report + ' site revenue'),
                    small_graph(report + ' site covers'),
                    small_graph(report + ' site spend')
                ],
                style = {
                    'display': 'inline-block',
                    'height':dimensions['main']['height'],
                    'width':dimensions['main']['width']
                }
            )
        ]
    )
    
    week_dropdowns = html.Div(
        [
            html.Div(
                [
                    html.P(
                        ['Choose the restaurant of the week view:']
                    ),
                    dcc.Dropdown(
                        id = report + ' site week dropdown',
                        options = [{'label':i,'value':i} for i in dropdown_values['restaurants_week']],
                        value = 'Group',
                        style = {'width':dimensions['week_div']['dropdown_width']}
                    )
                ],
                style = week_dropdown_style
            ),
            html.Div(
                [
                    html.P(
                        ['Choose the area of the week view:']
                    ),
                    dcc.Dropdown(
                        id = report + ' area week dropdown',
                        options = [{'label':i,'value':i} for i in dropdown_values['areas']],
                        value = 'Full Site',
                        style = {'width':dimensions['week_div']['dropdown_width']}
                    )
                ],
                style = week_dropdown_style
            ),
            html.Div(
                [
                    html.P(
                        ['Choose the revenue category of the week view:']
                    ),
                    dcc.Dropdown(
                        id = report + ' category week dropdown',
                        options = [{'label':i,'value':i} for i in dropdown_values['types']],
                        value = 'Total',
                        style = {'width':dimensions['week_div']['dropdown_width']}
                    )
                ],
                style = week_dropdown_style
            ),
            html.Div(
                [
                    html.P(
                        ['Choose the measure of the week view:']
                    ),
                    dcc.Dropdown(
                        id = report + ' measure week dropdown',
                        options = [{'label':i, 'value':i} for i in ["Revenue","Spend"]],
                        value = 'Revenue',
                        style = {'width':dimensions['week_div']['dropdown_width']}
                    )
                ],
                style = week_dropdown_style
            ),
            html.Div(
                [
                    html.P(
                        ['Choose the metric of the week view:']
                    ),
                    dcc.Dropdown(
                        id = report + ' metric week dropdown',
                        options = [{'label':i, 'value':i} for i in ["Actuals", "Averages"]],
                        value = 'Actuals',
                        style = {'width':dimensions['week_div']['dropdown_width']}
                    )
                ],
                style = week_dropdown_style
            )
        ],
        style = {
            'borderBottom': header_colors['border'],
            'borderRight': header_colors['border'],
            'backgroundColor': header_colors['background'],
            'padding': '10px 5px'
        }
    )
    
    week_graphs = html.Div(
        [
            html.Div(
                [week_graph(report + ' week view')],
                style = {
                    'display': 'inline-block',
                    'height':dimensions['week']['height'],
                    'width':dimensions['week']['width']
                }
            ),
            html.Div(
                [week_graph(report + ' week covers')],
                style = {
                    'display': 'inline-block',
                    'height':dimensions['week']['height'],
                    'width':dimensions['week']['width']
                }
            )
        ]
    )
    
    if report == 'daily':
        layout = html.Div(children = [title, summary_dropdowns, summary_graphs])
    else:
        layout = html.Div(children = [title, summary_dropdowns, summary_graphs, week_dropdowns, week_graphs])
    
    return layout                             
    
def tracker_layout_template(report):
    
    tracker_weeks = [
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
    
    tracker_metrics = [
        'vs. LW',
        'vs. LY',
        'Totals Last Week',
        'Totals Last Year'
    ]
    
    if report == 'tracker':
        title_string = 'Cover Tracker'
    else:
        title_string = 'Daily Pickup'
        
    title = html.Div(
        [
            html.H1(
                children = title_string,
                style = h1_style
            )
        ]
    )
    
    dropdowns = html.Div(
        [
            html.Div(
                [
                    html.P(
                        ['Choose the metric of the report:']
                    ),
                    dcc.Dropdown(
                        id=report + '_metric_dropdown',
                        options = [{'label':i,'value':i} for i in tracker_metrics],
                        value = tracker_metrics[default_metric_index],
                        style={'width':dimensions['div']['dropdown_width']}
                    )
                ],
                style = div_style_simple(dimensions['div']['width'])
            ), 
            html.Div(
                [
                    html.P(
                        ['Choose the week of the report:']
                    ),
                    dcc.Dropdown(
                        id=report + '_week_dropdown',
                        options = [{'label':i, 'value':i} for i in tracker_weeks],
                        value="This Week",
                        style={'width':dimensions['div']['dropdown_width']}
                    )
                ],
                style = div_style_simple(dimensions['div']['width'])
            ),
            html.Div(
                [
                    html.P(
                        ['Choose the restaurant of the site analysis:']
                    ),
                    dcc.Dropdown(
                        id=report + '_site_dropdown',
                        options=[{'label':i,'value':i} for i in dropdown_values['restaurants']],
                        value=dropdown_values['restaurants'],
                        style={'width':dimensions['div']['dropdown_width']}
                    )
                ],
                style = div_style_simple(dimensions['div']['width'])
            )
        ],
        style = dropdown_row_style
    )
    
    graphs = html.Div(
        [
            html.Div(
                [
                    tracker_graph(report + '_group_8_weeks'),
                    tracker_graph(report + '_group_week')
                ],
                style = {
                    'display': 'inline-block',
                    'height':dimensions['main']['height'],
                    'width':dimensions['main']['width']
                }
            ),
            html.Div(
                [
                    dcc.Graph(
                        id=report + '_breakdown',
                        config={'displayModeBar':False}
                    )
                ],    
                style = {
                    'display': 'inline-block',
                    'height':dimensions['main']['height'],
                    'width':dimensions['main']['width']}
            ),
            html.Div(
                [
                    tracker_graph(report + '_site_8_weeks'),
                    tracker_graph(report + '_site_week')
                ],
                style = {
                    'display': 'inline-block',
                    'height':dimensions['main']['height'],
                    'width':dimensions['main']['width']
                }
            )
        ]
    )
    
    return html.Div(children = [title, dropdowns, graphs])

def future():
    return html.Div(
        children=[
            html.Div(
                [
                    html.H1(
                        children = 'Future Bookings',
                        style = h1_style
                    )
                ]
            ),
            html.Div(
                [
                    dcc.Dropdown(
                        id='future dropdown',
                        options=[{'label':i, 'value':i} for i in ['Total Bookings', 'vs. LW']],
                        value='Total Bookings',
                        style={
                            'textAlign':'center',
                            'width':'100%',
                        }
                    )
                ],
                style = {
                    'width': '100%', 
                    'display': 'flex', 
                    'align-items': 'center', 
                    'justify-content': 'center',
                    'borderBottom': header_colors['border'],
                    'borderRight': header_colors['border'],
                    'backgroundColor': header_colors['background'],
                    'padding': '10px 5px'
                }
            ),
            html.Div(
                [
                    dcc.Graph(
                        id='future graph',
                        config={'displayModeBar':False},
                        style={'width':'100%'}
                    )
                ],
                style = {
                    'width': '100%', 
                    'display': 'flex', 
                    'align-items': 'center', 
                    'justify-content': 'center'
                }
            )
        ]
    )

def trends():

    today_weekday_num = date.today().weekday()
    today_week = date.today().isocalendar()[1]
    
    return html.Div(
        children=[
            html.Div(
                [
                    html.H1(
                        children = 'Booking Trends',
                        style = h1_style
                    )
                ]
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.P(
                                ['Choose the restaurant of the right-hand graphs:']
                            ),
                            dcc.Dropdown(
                                id='trends site dropdown',
                                options = [{'label':i,'value':i} for i in user_restaurants['dandd']['bookings']],
                                value=user_restaurants['dandd']['bookings'][0],
                                style={
                                    'textAlign':'center',
                                    'width':'100%',
                                }
                            )
                        ],
                    )
                ],
                style = {
                    'width': '100%', 
                    'display': 'flex', 
                    'align-items': 'center', 
                    'justify-content': 'center',
                    'borderBottom': header_colors['border'],
                    'borderRight': header_colors['border'],
                    'backgroundColor': header_colors['background'],
                    'padding': '10px 5px'
                }
            ),
            html.Div(
                [
                    html.Div(
                        [
                            dcc.Graph(
                                id='trends group pickup',
                                figure=trends_group_pickup_figure(
                                    trends_df,
                                    today_week,
                                    today_weekday_num
                                ),
                                config = {'displayModeBar':False}
                            )
                        ],
                        style = styles['trends_graph_div']
                    ),
                    html.Div(
                        [
                            dcc.Graph(
                                id='trends site pickup',
                                config = {'displayModeBar':False}
                            )
                        ],
                        style = styles['trends_graph_div']
                    )
                ]
            ),
            html.Div(
                [
                    html.Div(
                        [
                            dcc.Graph(
                                id='trends group future',
                                config = {'displayModeBar':False},
                                figure=trends_group_future_figure(
                                    trends_df,
                                    today_week,
                                    today_weekday_num
                                )
                            )
                        ],
                        style = styles['trends_graph_div']
                    ),
                    html.Div(
                        [
                            dcc.Graph(
                                id='trends site future',
                                config = {'displayModeBar':False}
                            )
                        ],
                        style = styles['trends_graph_div']
                    )
                ]
            )
        ]
    )

home_page_layout = home_page()
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
