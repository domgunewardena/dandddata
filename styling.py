import dash_core_components as dcc

user_restaurants = {
    'dandd':[
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
        'White City'],
    'michaelf':[
        '100 Wardour Street',
        'Avenue',
        'Bluebird Chelsea',
        'Madison', 
        'Quaglinos', 
        'Skylon', 
        'White City'],
    'jb':[
        '20 Stories', 
        'Aster', 
        "Coq d'Argent", 
        'East 59th', 
        'German Gymnasium', 
        'Issho',
        'New Street Warehouse',
        'Paternoster Chophouse', 
        'Plateau', 
        'Trinity'],
    'sharon':[
        'Butlers Wharf Chophouse', 
        'Cantina', 
        'Fiume',
        'Launceston Place',
        'Le Pont de la Tour', 
        'Orrery', 
        'Radici',
        'Sartoria']
}

bookings_user_restaurants = {
    'dandd':[
        '100 Wardour St',
        '14 Hills',
        '20 Stories',
        'Angelica',
        'Angler Restaurant',
        'Aster',
        'Avenue',
        'Bluebird Chelsea Restaurant',
        'Bluebird White City',
        'Butlers Wharf Chophouse Restaurant',
        'Cantina del Ponte',
        "Coq d'Argent",
        'Crafthouse',
        'East 59th',
        'Fish Market',
        'Fiume',
        'German Gymnasium',
        'Issho Restaurant',
        'Klosterhaus',
        'Launceston Place',
        'Madison Restaurant',
        'New Street Grill',
        'Orrery',
        'Paternoster Chophouse',
        'Plateau',
        'Pont de la Tour',
        'Quaglino’s Restaurant',
        'Radici',
        'Sartoria',
        'Skylon Restaurant',
        'South Place Chop House',
        'The Modern Pantry'
    ],
    'michaelf':[
        '100 Wardour St',
         '14 Hills',
         'Avenue',
         'Bluebird Chelsea Restaurant',
         'Bluebird White City',
         'Madison Restaurant',
         'Quaglino’s Restaurant',
         'Skylon Restaurant'
    ],
    'sharon':[
         'Butlers Wharf Chophouse Restaurant',
         'Cantina del Ponte',
         'Fiume',
         'Launceston Place',
         'Orrery',
         'Pont de la Tour',
         'Radici',
         'Sartoria',
         'The Modern Pantry'
    ],
    'jb':[
        '20 Stories',
         'Angelica',
         'Angler Restaurant',
         'Aster',
         "Coq d'Argent",
         'Crafthouse',
         'East 59th',
         'Fish Market',
         'German Gymnasium',
         'Issho Restaurant',
         'Klosterhaus',
         'New Street Grill',
         'Orrery',
         'Paternoster Chophouse',
         'Plateau'
    ]
}

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
        'width':width
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
            'Total':'£%{x:+.0f}',
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

def tracker_graph(graph_id):
    return dcc.Graph(
        id=graph_id,
        style={
            'height':450,
            'width':'100%'
        },
        config={'displayModeBar':False})
