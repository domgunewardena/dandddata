import dash_core_components as dcc

available_restaurants = [
    '100 Wardour Street', 
     '20 Stories', 
     'Aster', 
     'Avenue', 
     'Bluebird Chelsea', 
     'Blueprint Café', 
     'Butlers Wharf Chophouse', 
     'Cantina', 
     "Coq d'Argent", 
     'East 59th', 
     'Fiume', 
     'German Gymnasium', 
     'Issho', 
     'Launceston Place', 
     'Le Pont de la Tour', 
     'Madison', 
     'New Street Warehouse', 
     'Orrery', 
     'Paternoster Chophouse', 
     'Plateau', 
     'Quaglinos', 
     'Radici', 
     'Sartoria', 
     'Skylon', 
     'South Place Hotel', 
     'Trinity', 
     'White City']

dropdown_values = {
    'restaurants':available_restaurants,
    'restaurants_week': ['Group'] + available_restaurants,
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


dimensions = {
    'main':{
        'height':900,
        'width':'33%'
    },
    'mini':{
        'height':300,
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
            'dropdown_width':'100%'
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
#         'display':'inline-flex',
#         'display':'flex',
        'width':width,
        'align-items':'center',
        'justify-content':'center',
    }

def small_graph(graph_id):
    return dcc.Graph(
        id=graph_id,
        style={
            'height':dimensions['mini']['height'],
#             'width':dimensions['mini']['width']
            'width':'100%'
        },
        config={'displayModeBar':False})

def week_graph(graph_id):
    return dcc.Graph(
        id=graph_id,
        style={
            'height':dimensions['week']['height'],
#             'width':dimensions['week']['width']
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

def capitalize_report_title(report):
    
    if report in ['wtd', 'mtd']:
        return report.upper()
    else:
        return report.capitalize()
