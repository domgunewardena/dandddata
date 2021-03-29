import dash_core_components as dcc
import dash_html_components as html
from authentication.users import sales_restaurants

dropdown_values = {
    'restaurants':sales_restaurants,
    'restaurants_week': ['Group'] + sales_restaurants,
    'shifts':[
        'All Shifts', 
        'Lunch', 
        'Dinner'
    ],
    'measures':[
        'Revenue', 
        'Covers', 
        'Spend'
    ],
    'areas':[
        "Full Site", 
        "Restaurant", 
        "Bar", 
        "PDR", 
        "Events & Ex Hires", 
        "Retail & Other"
    ],
    'types':[
        "Total", 
        "Food", 
        "Beverage", 
        "Wine", 
        "Non-Wine"
    ]
}

metrics = ['vs. LW','vs. LY', 'Totals Last Week', 'Totals Last Year']
default_metric_index = 1

dimensions = {
    'main':{
        'height':900,
        'width':'33%'
    },
    'mini':{
        'height':300,
        'width':'100%'
    },
    'mini_tracker':{
        'height':350,
        'width':'100%'
    },
    'week':{
        'height':450,
        'width':'50%'
    },
    'div':{
        'width':'33%',
        'dropdown_width':'99%'
    },
    'week_div':{
        'width':'20%',
        'dropdown_width':'99%'
    },
    'trends':{
        'height':400,
        'width':'50%'
    },
    'homepage':{
        'dropdowns':{
            'div_width':'50%',
            'dropdown_width':'99%'
        }
    }
}

header_colors = {
    'background':"rgb(250,250,250)",
    'border':'thin lightgrey solid'
}

styles = {
    'H1':{
        'textAlign':"center",
        'borderBottom': header_colors['border'],
        'borderRight': header_colors['border'],
        'backgroundColor': header_colors['background']
    },
    'dropdown_row':{
        'borderBottom': header_colors['border'],
        'borderRight': header_colors['border'],
        'backgroundColor': header_colors['background'],
        'padding': '10px 5px'
    },
    'week_dropdown':{
        'textAlign':'center',
        'display': 'inline-block',
        'width': dimensions['week_div']['width']
    },
    'trends_graph_div':{
        'display': 'inline-block',
        'height':dimensions['trends']['height'],
        'width':dimensions['trends']['width']
    }
}

        

h1_style = {
    'textAlign':"center",
    'borderBottom': header_colors['border'],
    'borderRight': header_colors['border'],
    'backgroundColor': header_colors['background']
}

week_dropdown_style = {
    'textAlign':'center',
    'display': 'inline-block',
    'width': dimensions['week_div']['width']
}

dropdown_row_style = {
    'borderBottom': header_colors['border'],
    'borderRight': header_colors['border'],
    'backgroundColor': header_colors['background'],
    'padding': '10px 5px'
}

def div_style_simple(width):
    return {
        'textAlign':'center',
        'display': 'inline-block',
        'width':width,
        'align-items':'center',
        'justify-content':'center',
    }

def small_graph(graph_id):
    return dcc.Graph(
        id=graph_id,
        style={
            'height':dimensions['mini']['height'],
            'width':'100%'
        },
        config={'displayModeBar':False})

def week_graph(graph_id):
    return dcc.Graph(
        id=graph_id,
        style={
            'height':dimensions['week']['height'],
            'width':'100%'
        },
        config={'displayModeBar':False})


templates = {
    'Sales':{
        'Revenue':{
            'Total':'£%{customdata:.0f}k',
            'Change':'£%{y:+.0f}'
        },
        'Covers':{
            'Total':'%{y:.0f}',
            'Change':'%{y:+.0f}'
        },
        'Spend':{
            'Total':'£%{y:.0f}',
            'Change':'£%{y:+.2f}'
        }
    },
    'Sales Breakdown':{
        'Revenue':{
            'Total':'£%{customdata:.0f}k',
            'Change':'£%{x:+.0f}'
        },
        'Covers':{
            'Total':'%{x:.0f}',
            'Change':'%{x:+.0f}'
        },
        'Spend':{
            'Total':'£%{x:.0f}',
            'Change':'£%{x:+.2f}'
        }
    },
    'Future Bookings':{
        'Bookings':{
            'Total':'%{y} - %{customdata} %{x}',
            'Change':'%{y:+.0f} - %{customdata} %{x}'
        },
        'Capacity':'%{y}'
    }
}

total_colors = {
    'Revenue':{
        'Last':'powderblue',
        'Current':'steelblue'
    },
    'Covers':{
        'Last':'lightgrey',
        'Current':'darkslategrey'
    },
    'Spend':{
        'Last':'pink',
        'Current':'mediumvioletred'
    }
}

week_colors = {
    'Revenue':{
        'Lunch':{
            'Current':'navy',
            'Last':'lightsteelblue'
        },
        'Dinner':{
            'Current':'steelblue',
            'Last':'powderblue'
        },
    },
    'Covers':{
        'Lunch':{
            'Current':'teal',
            'Last':'paleturquoise'
        },
        'Dinner':{
            'Current':'darkslategrey',
            'Last':'lightgrey'
        },
    },
    'Spend':{
        'Lunch':{
            'Current':'mediumvioletred',
            'Last':'pink'
        },
        'Dinner':{
            'Current':'purple',
            'Last':'plum'
        },
    },
    'Change':{
        'Lunch':{
            'Rise':'lime',
            'Fall':'salmon'
        },
        'Dinner':{
            'Rise':'limegreen',
            'Fall':'red'
        }
    }
}

review_colors = {
    'overall':'blue',
    'food':'green',
    'service':'red',
    'ambience':'orange',
    'value':'purple'
}


def week_colors_totals(measure, shift, metric):
    return week_colors[measure][shift][metric]

def week_colors_change(shift, val):
    return week_colors['Change'][shift]['Rise'] if val>0 else week_colors['Change'][shift]['Fall']

plus = lambda i: ("+" if i > 0 else "") + str(i)

def tracker_graph(graph_id):
    return dcc.Graph(
        id=graph_id,
        style={
            'height':'50%',
            'width':'100%'
        },
        config={'displayModeBar':False})

def home_tracker_graph(graph_id):
    return dcc.Graph(
        id=graph_id,
        style={
            'height':'100%',
            'width':'100%'
        },
        config={'displayModeBar':False})

def review_graph(graph_id):
    return dcc.Graph(
        id=graph_id,
        style={
            'height':'100%',
            'width':'100%'
        },
        config={'displayModeBar':False}
    )

def breakdown_sales_div(graph_id):
    
    return html.Div(
        [
            dcc.Graph(
                id = graph_id,
                config = {'displayModeBar':False}
            )
        ],    
        style = {
            'display':'inline-block',
            'height':dimensions['main']['height'],
            'width':dimensions['main']['width']
        }
    )

def breakdown_tracker_div(graph_id):
    
    tracker_graphs_extra_height = 100
    
    return html.Div(
        [
            dcc.Graph(
                id = graph_id,
                config = {'displayModeBar':False},
                style={
                    'height':'100%',
                    'width':'100%'
                }
            )
        ],    
        style = {
            'display':'inline-block',
            'height':dimensions['main']['height']+tracker_graphs_extra_height,
            'width':dimensions['main']['width']
        }
    )

def breakdown_review_div(graph_id):
    
    return html.Div(
        [
            review_graph(graph_id),
        ],
        style = {
            'display':'inline-block',
            'height':dimensions['main']['height'],
            'width':'20%'
        }
    )

def breakdown_future_div(graph_id):
    
    return html.Div(
        [
            dcc.Graph(
                id = graph_id,
                config = {'displayModeBar':False},
                style={
                    'height':'100%',
                    'width':'100%'
                }
            )
        ],    
        style = {
            'display':'inline-block',
            'height':dimensions['main']['height']+100,
            'width':dimensions['main']['width']
        }
    )
    

def capitalize_report_title(report):
    if report in ['wtd', 'mtd']:
        return report.upper()
    else:
        return report.capitalize()
