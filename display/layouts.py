import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from datetime import date, datetime, timedelta

from display.variables import *
from display.styling import *
from authentication.users import bookings_user_restaurants

from plots.figures import trends_group_pickup_figure, trends_group_future_figure
from data.data import trends_df

def home_page():
    
    return html.Div(
        children=[
            html.Div(
                [
                    html.H1(
                        children = 'D&D Data',
                        style = h1_style
                    )
                ]
            )
        ]
    )

def sales_layout_template(report):
        
    week_metrics = ['vs. LW','vs. LY', 'Last Week', 'Last Year']
    month_metrics = ['vs. LM','vs. LY', 'Last Month', 'Last Year']
    
    week_reports = ['Daily', 'WTD', 'Weekly']
    month_reports = ['MTD','Monthly']

    if report in week_reports:
        metrics = week_metrics
    elif report in month_reports:
        metrics = month_metrics
    
    title = html.Div(
        [
            html.H1(
                children = report.upper() + ' Sales',
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
                        value = metrics[0],
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
    
    if report == 'Daily':
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
        'Last Week',
        'Last Year'
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
                        value='vs. LW',
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
                        options=[{'label':i,'value':i} for i in available_restaurants],
                        value='100 Wardour Street',
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
                        style={'width':'50%'}
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

    today_weekday_num = date.today().weekday()
    today_week = date.today().isocalendar()[1]

def trends():
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
                                options = [{'label':i,'value':i} for i in bookings_user_restaurants['dandd']],
                                value=bookings_user_restaurants['dandd'][0],
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
daily_layout = sales_layout_template('daily')
wtd_layout = sales_layout_template('wtd')
mtd_layout = sales_layout_template('mtd')
weekly_layout = sales_layout_template('weekly')
monthly_layout = sales_layout_template('monthly')
tracker_layout = tracker_layout_template('tracker')
pickup_layout = tracker_layout_template('pickup')
future_layout = future()
trends_layout = trends()
