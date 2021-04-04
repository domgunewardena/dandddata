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

graph_colors = {
    'background':'#f9f9f9',
    'covers':'lightskyblue',
    'revenue':'plum',
    'scores':'darkturquoise',
    'scores_scale':'Teal',
}


def week_colors_totals(measure, shift, metric):
    return week_colors[measure][shift][metric]

def week_colors_change(shift, val):
    return week_colors['Change'][shift]['Rise'] if val>0 else week_colors['Change'][shift]['Fall']


plus = lambda i: ("+" if i > 0 else "") + str(i)

def capitalize_report_title(report):
    if report in ['wtd', 'mtd']:
        return report.upper()
    else:
        return report.capitalize()