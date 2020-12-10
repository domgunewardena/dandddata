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

# Home Page

home_page = html.Div(
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

# Daily Sales Layout

daily_layout =  html.Div(
    children=[
        html.Div(
            [
                html.H1(
                    children = 'Daily Sales',
                    style = h1_style
                )
            ]
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            ['Choose the metric and shift of the report:']
                        ),
                        dcc.Dropdown(
                            id='daily metric dropdown',
                            options = [{'label':i, 'value':i} for i in daily_metrics],
                            value=daily_metrics[0],
                            style={'width':dimensions['div']['dropdown_width']}
                        ),
                        dcc.Dropdown(
                            id='daily shift dropdown',
                            options=[{'label':i, 'value':i} for i in dropdown_values['shifts']],
                            value='All Shifts',
                            style={
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
                            id='daily area dropdown',
                            options = [{'label':i,'value':i} for i in dropdown_values['areas']],
                            value='Full Site',
                            style={'width':dimensions['div']['dropdown_width']}
                        ),
                        dcc.Dropdown(
                            id='daily measure dropdown',
                            options = [{'label':i,'value':i} for i in dropdown_values['measures']],
                            value='Revenue',
                            style={'width':dimensions['div']['dropdown_width'],'padding':'2px 0px'}
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
                            id='daily site dropdown',
                            options=[{'label':i,'value':i} for i in dropdown_values['restaurants']],
                            value='100 Wardour Street',
                            style={'width':dimensions['div']['dropdown_width']}
                        )
                    ],
                    style = div_style_simple(dimensions['div']['width'])
                )
            ],
            style = dropdown_row_style),
        html.Div(
            [
                html.Div(
                    [
                        small_graph('daily group revenue'),
                        small_graph('daily group covers'),
                        small_graph('daily group spend')
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
                            id='daily sales total',
                            config={'displayModeBar':False}
                        )
                    ],    
                    style = {
                        'display': 'inline-block',
                        'height':dimensions['main']['height'],
                        'width':dimensions['main']['width']
                    }
                ),
                html.Div(
                    [
                        small_graph('daily site revenue'),
                        small_graph('daily site covers'),
                        small_graph('daily site spend')
                    ],
                    style = {
                        'display': 'inline-block',
                        'height':dimensions['main']['height'],
                        'width':dimensions['main']['width']
                    }
                )
            ]
        )
    ]
)

# WTD Sales Layout

wtd_layout =  html.Div(
    children=[
        html.Div(
            [
                html.H1(
                    children = 'WTD Sales',
                    style = h1_style
                )
            ]
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            ['Choose the metric and shift of the report:']
                        ),
                        dcc.Dropdown(
                            id='wtd metric dropdown',
                            options = [{'label':i, 'value':i} for i in wtd_metrics],
                            value=wtd_metrics[0],
                            style={'width':dimensions['div']['dropdown_width']}
                        ),
                        dcc.Dropdown(
                            id='wtd shift dropdown',
                            options=[{'label':i, 'value':i} for i in dropdown_values['shifts']],
                            value='All Shifts',
                            style={
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
                            id='wtd area dropdown',
                            options = [{'label':i,'value':i} for i in dropdown_values['areas']],
                            value='Full Site',
                            style={'width':dimensions['div']['dropdown_width']}
                        ),
                        dcc.Dropdown(
                            id='wtd measure dropdown',
                            options = [{'label':i,'value':i} for i in dropdown_values['measures']],
                            value='Revenue',
                            style={
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
                            id='wtd site dropdown',
                            options=[{'label':i,'value':i} for i in dropdown_values['restaurants']],
                            value='100 Wardour Street',
                            style={'width':dimensions['div']['dropdown_width']}
                        )
                    ],
                    style = div_style_simple(dimensions['div']['width'])
                )
            ],
            style = dropdown_row_style
        ),
        html.Div(
            [
                html.Div(
                    [
                        small_graph('wtd group revenue'),
                        small_graph('wtd group covers'),
                        small_graph('wtd group spend')
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
                            id='wtd sales total',
                            config={'displayModeBar':False}
                        )
                    ],    
                    style = {
                        'display': 'inline-block',
                        'height':dimensions['main']['height'],
                        'width':dimensions['main']['width']
                    }
                ),
                html.Div(
                    [
                        small_graph('wtd site revenue'),
                        small_graph('wtd site covers'),
                        small_graph('wtd site spend')
                    ],
                    style = {
                        'display': 'inline-block',
                        'height':dimensions['main']['height'],
                        'width':dimensions['main']['width']
                    }
                )
            ]
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            ['Choose the restaurant of the week view:']
                        ),
                        dcc.Dropdown(
                            id='wtd site week dropdown',
                            options=[{'label':i,'value':i} for i in dropdown_values['restaurants_week']],
                            value='Group',
                            style={'width':dimensions['week_div']['dropdown_width']}
                        )
                    ],
                    style=week_dropdown_style
                ),
                html.Div(
                    [
                        html.P(
                            ['Choose the area of the week view:']
                        ),
                        dcc.Dropdown(
                            id='wtd area week dropdown',
                            options = [{'label':i,'value':i} for i in dropdown_values['areas']],
                            value='Full Site',
                            style={'width':dimensions['week_div']['dropdown_width']}
                        )
                    ],
                    style=week_dropdown_style
                ),
                html.Div(
                    [
                        html.P(
                            ['Choose the revenue category of the week view:']
                        ),
                        dcc.Dropdown(
                            id='wtd category week dropdown',
                            options = [{'label':i,'value':i} for i in dropdown_values['types']],
                            value='Total',
                            style={'width':dimensions['week_div']['dropdown_width']}
                        )
                    ],
                    style=week_dropdown_style
                ),
                html.Div(
                    [
                        html.P(
                            ['Choose the measure of the week view:']
                        ),
                        dcc.Dropdown(
                            id='wtd measure week dropdown',
                            options = [{'label':i, 'value':i} for i in ["Revenue","Spend"]],
                            value='Revenue',
                            style={'width':dimensions['week_div']['dropdown_width']}
                        )
                    ],
                    style=week_dropdown_style
                ),
                html.Div(
                    [
                        html.P(
                            ['Choose the metric of the week view:']
                        ),
                        dcc.Dropdown(
                            id='wtd metric week dropdown',
                            options = [{'label':i, 'value':i} for i in ["Actuals", "Averages"]],
                            value='Actuals',
                            style={'width':dimensions['week_div']['dropdown_width']}
                        )
                    ],
                    style=week_dropdown_style
                )
            ],
            style = {
                'borderBottom': header_colors['border'],
                'borderRight': header_colors['border'],
                'backgroundColor': header_colors['background'],
                'padding': '10px 5px'
            }
        ),
        html.Div(
            [
                html.Div(
                    [week_graph('wtd week view')],
                    style = {
                        'display': 'inline-block',
                        'height':dimensions['week']['height'],
                        'width':dimensions['week']['width']
                    }
                ),
                html.Div(
                    [week_graph('wtd week covers')],
                    style = {
                        'display': 'inline-block',
                        'height':dimensions['week']['height'],
                        'width':dimensions['week']['width']
                    }
                )
            ]
        )
    ]
)

# MTD Sales Layout

mtd_layout =  html.Div(
    children=[
        html.Div(
            [
                html.H1(
                    children = 'MTD Sales',
                    style = h1_style
                )
            ]
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            ['Choose the metric and shift of the report:']
                        ),
                        dcc.Dropdown(
                            id='mtd metric dropdown',
                            options = [{'label':i, 'value':i} for i in mtd_metrics],
                            value=mtd_metrics[0],
                            style={'width':dimensions['div']['dropdown_width']}
                        ),
                        dcc.Dropdown(
                            id='mtd shift dropdown',
                            options=[{'label':i, 'value':i} for i in dropdown_values['shifts']],
                            value='All Shifts',
                            style={
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
                            id='mtd area dropdown',
                            options = [{'label':i,'value':i} for i in dropdown_values['areas']],
                            value='Full Site',
                            style={'width':dimensions['div']['dropdown_width']}
                        ),
                        dcc.Dropdown(
                            id='mtd measure dropdown',
                            options = [{'label':i,'value':i} for i in dropdown_values['measures']],
                            value='Revenue',
                            style={'width':dimensions['div']['dropdown_width'],'padding':'2px 0px'}
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
                            id='mtd site dropdown',
                            options=[{'label':i,'value':i} for i in dropdown_values['restaurants']],
                            value='100 Wardour Street',
                            style={'width':dimensions['div']['dropdown_width']}
                        )
                    ],
                    style = div_style_simple(dimensions['div']['width'])
                )
            ],
            style = dropdown_row_style
        ),
        html.Div(
            [
                html.Div(
                    [
                        small_graph('mtd group revenue'),
                        small_graph('mtd group covers'),
                        small_graph('mtd group spend')
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
                            id='mtd sales total',
                            config={'displayModeBar':False}
                        )
                    ],    
                    style = {
                        'display': 'inline-block',
                        'height':dimensions['main']['height'],
                        'width':dimensions['main']['width']
                    }
                ),
                html.Div(
                    [
                        small_graph('mtd site revenue'),
                        small_graph('mtd site covers'),
                        small_graph('mtd site spend')
                    ],
                    style = {
                        'display': 'inline-block',
                        'height':dimensions['main']['height'],
                        'width':dimensions['main']['width']
                    }
                )
            ]
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            ['Choose the restaurant of the week view:']
                        ),
                        dcc.Dropdown(
                            id='mtd site week dropdown',
                            options=[{'label':i,'value':i} for i in dropdown_values['restaurants_week']],
                            value='Group',
                            style={'width':dimensions['week_div']['dropdown_width']}
                        )
                    ],
                    style=week_dropdown_style
                ),
                html.Div(
                    [
                        html.P(
                            ['Choose the area of the week view:']
                        ),
                        dcc.Dropdown(
                            id='mtd area week dropdown',
                            options = [{'label':i,'value':i} for i in dropdown_values['areas']],
                            value='Full Site',
                            style={'width':dimensions['week_div']['dropdown_width']}
                        )
                    ],
                    style=week_dropdown_style
                ),
                html.Div(
                    [
                        html.P(
                            ['Choose the revenue category of the week view:']
                        ),
                        dcc.Dropdown(
                            id='mtd category week dropdown',
                            options = [{'label':i,'value':i} for i in dropdown_values['types']],
                            value='Total',
                            style={'width':dimensions['week_div']['dropdown_width']}
                        )
                    ],
                    style=week_dropdown_style
                ),
                html.Div(
                    [
                        html.P(
                            ['Choose the measure of the week view:']
                        ),
                        dcc.Dropdown(
                            id='mtd measure week dropdown',
                            options = [{'label':i, 'value':i} for i in ["Revenue","Spend"]],
                            value='Revenue',
                            style={'width':dimensions['week_div']['dropdown_width']}
                        )
                    ],
                    style=week_dropdown_style
                ),
                html.Div(
                    [
                        html.P(
                            ['Choose the metric of the week view:']
                        ),
                        dcc.Dropdown(
                            id='mtd metric week dropdown',
                            options = [{'label':i, 'value':i} for i in ["Actuals", "Averages"]],
                            value='Actuals',
                            style={'width':dimensions['week_div']['dropdown_width']}
                        )
                    ],
                    style=week_dropdown_style
                )
            ],
            style = {
                'borderBottom': header_colors['border'],
                'borderRight': header_colors['border'],
                'backgroundColor': header_colors['background'],
                'padding': '10px 5px'
            }
        ),
        html.Div(
            [
                html.Div(
                    [week_graph('mtd week view')],
                    style = {
                        'display': 'inline-block',
                        'height':dimensions['week']['height'],
                        'width':dimensions['week']['width']
                    }
                ),
                html.Div(
                    [week_graph('mtd week covers')],
                    style = {
                        'display': 'inline-block',
                        'height':dimensions['week']['height'],
                        'width':dimensions['week']['width']
                    }
                )
            ]
        )
    ]
)


# Weekly Sales Layout

weekly_layout =  html.Div(
    children=[
        html.Div(
            [
                html.H1(
                    children = 'Weekly Sales',
                    style = h1_style
                )
            ]
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            ['Choose the metric and shift of the report:']
                        ),
                        dcc.Dropdown(
                            id='weekly metric dropdown',
                            options = [{'label':i, 'value':i} for i in weekly_metrics],
                            value=weekly_metrics[0],
                            style={'width':dimensions['div']['dropdown_width']}
                        ),
                        dcc.Dropdown(
                            id='weekly shift dropdown',
                            options=[{'label':i, 'value':i} for i in dropdown_values['shifts']],
                            value='All Shifts',
                            style={
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
                            id='weekly area dropdown',
                            options = [{'label':i,'value':i} for i in dropdown_values['areas']],
                            value='Full Site',
                            style={'width':dimensions['div']['dropdown_width']}
                        ),
                        dcc.Dropdown(
                            id='weekly measure dropdown',
                            options = [{'label':i,'value':i} for i in dropdown_values['measures']],
                            value='Revenue',
                            style={'width':dimensions['div']['dropdown_width'],'padding':'2px 0px'}
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
                            id='weekly site dropdown',
                            options=[{'label':i,'value':i} for i in dropdown_values['restaurants']],
                            value='100 Wardour Street',
                            style={'width':dimensions['div']['dropdown_width']}
                        )
                    ],
                    style = div_style_simple(dimensions['div']['width'])
                )
            ],
            style = dropdown_row_style
        ),
        html.Div(
            [
                html.Div(
                    [
                        small_graph('weekly group revenue'),
                        small_graph('weekly group covers'),
                        small_graph('weekly group spend')
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
                            id='weekly sales total',
                            config={'displayModeBar':False}
                        )
                    ],    
                    style = {
                        'display': 'inline-block',
                        'height':dimensions['main']['height'],
                        'width':dimensions['main']['width']
                    }
                ),
                html.Div(
                    [
                        small_graph('weekly site revenue'),
                        small_graph('weekly site covers'),
                        small_graph('weekly site spend')
                    ],
                    style = {
                        'display': 'inline-block',
                        'height':dimensions['main']['height'],
                        'width':dimensions['main']['width']
                    }
                )
            ]
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            ['Choose the restaurant of the week view:']
                        ),
                        dcc.Dropdown(
                            id='weekly site week dropdown',
                            options=[{'label':i,'value':i} for i in dropdown_values['restaurants_week']],
                            value='Group',
                            style={'width':dimensions['week_div']['dropdown_width']}
                        )
                    ],
                    style=week_dropdown_style
                ),
                html.Div(
                    [
                        html.P(
                            ['Choose the area of the week view:']
                        ),
                        dcc.Dropdown(
                            id='weekly area week dropdown',
                            options = [{'label':i,'value':i} for i in dropdown_values['areas']],
                            value='Full Site',
                            style={'width':dimensions['week_div']['dropdown_width']}
                        )
                    ],
                    style=week_dropdown_style
                ),
                html.Div(
                    [
                        html.P(
                            ['Choose the revenue category of the week view:']
                        ),
                        dcc.Dropdown(
                            id='weekly category week dropdown',
                            options = [{'label':i,'value':i} for i in dropdown_values['types']],
                            value='Total',
                            style={'width':dimensions['week_div']['dropdown_width']}
                        )
                    ],
                    style=week_dropdown_style
                ),
                html.Div(
                    [
                        html.P(
                            ['Choose the measure of the week view:']
                        ),
                        dcc.Dropdown(
                            id='weekly measure week dropdown',
                            options = [{'label':i, 'value':i} for i in ["Revenue","Spend"]],
                            value='Revenue',
                            style={'width':dimensions['week_div']['dropdown_width']}
                        )
                    ],
                    style=week_dropdown_style
                ),
                html.Div(
                    [
                        html.P(
                            ['Choose the metric of the week view:']
                        ),
                        dcc.Dropdown(
                            id='weekly metric week dropdown',
                            options = [{'label':i, 'value':i} for i in ["Actuals", "Averages"]],
                            value='Actuals',
                            style={'width':dimensions['week_div']['dropdown_width']}
                        )
                    ],
                    style=week_dropdown_style
                )
            ],
            style = {
                'borderBottom': header_colors['border'],
                'borderRight': header_colors['border'],
                'backgroundColor': header_colors['background'],
                'padding': '10px 5px'
            }
        ),
        html.Div(
            [
                html.Div(
                    [week_graph('weekly week view')],
                    style = {
                        'display': 'inline-block',
                        'height':dimensions['week']['height'],
                        'width':dimensions['week']['width']
                    }
                ),
                html.Div(
                    [week_graph('weekly week covers')],
                    style = {
                        'display': 'inline-block',
                        'height':dimensions['week']['height'],
                        'width':dimensions['week']['width']
                    }
                )
            ]
        )
    ]
)

# Monthly Sales Layout

monthly_layout =  html.Div(
    children=[
        html.Div(
            [
                html.H1(
                    children = 'Monthly Sales',
                    style = h1_style
                )
            ]
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            ['Choose the metric and shift of the report:']
                        ),
                        dcc.Dropdown(
                            id='monthly metric dropdown',
                            options = [{'label':i, 'value':i} for i in monthly_metrics],
                            value=monthly_metrics[0],
                            style={'width':dimensions['div']['dropdown_width']}
                        ),
                        dcc.Dropdown(
                            id='monthly shift dropdown',
                            options=[{'label':i, 'value':i} for i in dropdown_values['shifts']],
                            value='All Shifts',
                            style={
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
                            id='monthly area dropdown',
                            options = [{'label':i,'value':i} for i in dropdown_values['areas']],
                            value='Full Site',
                            style={'width':dimensions['div']['dropdown_width']}
                        ),
                        dcc.Dropdown(
                            id='monthly measure dropdown',
                            options = [{'label':i,'value':i} for i in dropdown_values['measures']],
                            value='Revenue',
                            style={'width':dimensions['div']['dropdown_width'],'padding':'2px 0px'}
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
                            id='monthly site dropdown',
                            options=[{'label':i,'value':i} for i in dropdown_values['restaurants']],
                            value='100 Wardour Street',
                            style={'width':dimensions['div']['dropdown_width']}
                        )
                    ],
                    style = div_style_simple(dimensions['div']['width'])
                )
            ],
            style = dropdown_row_style
        ),
        html.Div(
            [
                html.Div(
                    [
                        small_graph('monthly group revenue'),
                        small_graph('monthly group covers'),
                        small_graph('monthly group spend')
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
                            id='monthly sales total',
                            config={'displayModeBar':False}
                        )
                    ],    
                    style = {
                        'display': 'inline-block',
                        'height':dimensions['main']['height'],
                        'width':dimensions['main']['width']
                    }
                ),
                html.Div(
                    [
                        small_graph('monthly site revenue'),
                        small_graph('monthly site covers'),
                        small_graph('monthly site spend')
                    ],
                    style = {
                        'display': 'inline-block',
                        'height':dimensions['main']['height'],
                        'width':dimensions['main']['width']
                    }
                )
            ]
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            ['Choose the restaurant of the week view:']
                        ),
                        dcc.Dropdown(
                            id='monthly site week dropdown',
                            options=[{'label':i,'value':i} for i in dropdown_values['restaurants_week']],
                            value='Group',
                            style={'width':dimensions['week_div']['dropdown_width']}
                        )
                    ],
                    style=week_dropdown_style
                ),
                html.Div(
                    [
                        html.P(
                            ['Choose the area of the week view:']
                        ),
                        dcc.Dropdown(
                            id='monthly area week dropdown',
                            options = [{'label':i,'value':i} for i in dropdown_values['areas']],
                            value='Full Site',
                            style={'width':dimensions['week_div']['dropdown_width']}
                        )
                    ],
                    style=week_dropdown_style
                ),
                html.Div(
                    [
                        html.P(
                            ['Choose the revenue category of the week view:']
                        ),
                        dcc.Dropdown(
                            id='monthly category week dropdown',
                            options = [{'label':i,'value':i} for i in dropdown_values['types']],
                            value='Total',
                            style={'width':dimensions['week_div']['dropdown_width']}
                        )
                    ],
                    style=week_dropdown_style
                ),
                html.Div(
                    [
                        html.P(
                            ['Choose the measure of the week view:']
                        ),
                        dcc.Dropdown(
                            id='monthly measure week dropdown',
                            options = [{'label':i, 'value':i} for i in ["Revenue","Spend"]],
                            value='Revenue',
                            style={'width':dimensions['week_div']['dropdown_width']}
                        )
                    ],
                    style=week_dropdown_style
                ),
                html.Div(
                    [
                        html.P(
                            ['Choose the metric of the week view:']
                        ),
                        dcc.Dropdown(
                            id='monthly metric week dropdown',
                            options = [{'label':i, 'value':i} for i in ["Actuals", "Averages"]],
                            value='Actuals',
                            style={'width':dimensions['week_div']['dropdown_width']}
                        )
                    ],
                    style=week_dropdown_style
                )
            ],
            style = {
                'borderBottom': header_colors['border'],
                'borderRight': header_colors['border'],
                'backgroundColor': header_colors['background'],
                'padding': '10px 5px'
            }
        ),
        html.Div(
            [
                html.Div(
                    [week_graph('monthly week view')],
                    style = {
                        'display': 'inline-block',
                        'height':dimensions['week']['height'],
                        'width':dimensions['week']['width']
                    }
                ),
                html.Div(
                    [week_graph('monthly week covers')],
                    style = {
                        'display': 'inline-block',
                        'height':dimensions['week']['height'],
                        'width':dimensions['week']['width']
                    }
                )
            ]
        )
    ]
)

tracker_layout =  html.Div(
    children=[
        html.Div(
            [
                html.H1(
                    children = 'Cover Tracker',
                    style = h1_style
                )
            ]
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            ['Choose the metric of the report:']
                        ),
                        dcc.Dropdown(
                            id='tracker_metric_dropdown',
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
                            id='tracker_week_dropdown',
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
                            id='tracker_site_dropdown',
                            options=[{'label':i,'value':i} for i in available_restaurants],
                            value='100 Wardour Street',
                            style={'width':dimensions['div']['dropdown_width']}
                        )
                    ],
                    style = div_style_simple(dimensions['div']['width'])
                )
            ],
            style = dropdown_row_style
        ),
        html.Div(
            [
                html.Div(
                    [
                        tracker_graph('tracker_group_8_weeks'),
                        tracker_graph('tracker_group_week')
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
                            id='tracker_breakdown',
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
                        tracker_graph('tracker_site_8_weeks'),
                        tracker_graph('tracker_site_week')
                    ],
                    style = {
                        'display': 'inline-block',
                        'height':dimensions['main']['height'],
                        'width':dimensions['main']['width']
                    }
                )
            ]
        )
    ]
)


pickup_layout =  html.Div(
    children=[
        html.Div(
            [
                html.H1(
                    children = 'Daily Pickup',
                    style = h1_style
                )
            ]
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            ['Choose the metric of the report:']
                        ),
                        dcc.Dropdown(
                            id='pickup_metric_dropdown',
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
                            id='pickup_week_dropdown',
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
                            id='pickup_site_dropdown',
                            options=[{'label':i,'value':i} for i in available_restaurants],
                            value='100 Wardour Street',
                            style={'width':dimensions['div']['dropdown_width']}
                        )
                    ],
                    style = div_style_simple(dimensions['div']['width'])
                )
            ],
            style = dropdown_row_style
        ),
        html.Div(
            [
                html.Div(
                    [
                        tracker_graph('pickup_group_8_weeks'),
                        tracker_graph('pickup_group_week')
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
                            id='pickup_breakdown',
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
                        tracker_graph('pickup_site_8_weeks'),
                        tracker_graph('pickup_site_week')
                    ],
                    style = {
                        'display': 'inline-block',
                        'height':dimensions['main']['height'],
                        'width':dimensions['main']['width']
                    }
                )
            ]
        )
    ]
)

future_layout = html.Div(
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

trends_layout = html.Div(
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
