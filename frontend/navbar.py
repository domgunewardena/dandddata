import dash
import dash_bootstrap_components as dbc
import dash_html_components as html

# NavBar

def Navbar():
    
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Breakdown", href="/breakdown")),
            dbc.NavItem(dbc.NavLink("Restaurant", href="/restaurant")),
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem(
                        'Sales Reports', 
                        header=True
                    ),
                    dbc.DropdownMenuItem(
                        'Daily Sales', 
                        href="/daily-sales"
                    ),
                    dbc.DropdownMenuItem(
                        'WTD Sales', 
                        href="/wtd-sales"
                    ),
                    dbc.DropdownMenuItem(
                        'MTD Sales', 
                        href="/mtd-sales"
                    ),
                    dbc.DropdownMenuItem(
                        'Weekly Sales', 
                        href="/weekly-sales"
                    ),
                    dbc.DropdownMenuItem(
                        'Monthly Sales', 
                        href="/monthly-sales"
                    ),
                ],
                nav=True,
                in_navbar=True,
                label='Sales',
            ),
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem(
                        'Bookings Reports', 
                        header=True
                    ),
                    dbc.DropdownMenuItem(
                        'Cover Tracker', 
                        href="/tracker"
                    ),
                    dbc.DropdownMenuItem(
                        'Daily Pickup', 
                        href="/pickup"
                    ),
                    dbc.DropdownMenuItem(
                        'Future Bookings', 
                        href="/future"
                    ),
                    dbc.DropdownMenuItem(
                        'Booking Trends', 
                        href="/trends"
                    ),
                ],
                nav=True,
                in_navbar=True,
                label='Bookings',
            ),
        ],
        brand="D&D Data",
        brand_href="/",
        sticky="top"
    )
    
    return navbar

nav = Navbar()

# SideBar

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "20rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

sidebar = html.Div(
    [
        html.H2("D&D Data", className="display-4"),
        html.Hr(),
        html.P(
            "Click below to navigate the app", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavItem(dbc.NavLink("Group", href="/", active="exact")),
                dbc.NavItem(dbc.NavLink("Breakdown", href="/breakdown", active="exact")),
                dbc.NavItem(dbc.NavLink("Restaurant", href="/restaurant", active="exact")),
                dbc.DropdownMenu(
                    children=[
                        dbc.DropdownMenuItem(
                            'Sales Reports', 
                            header=True
                        ),
                        dbc.DropdownMenuItem(
                            'Daily Sales', 
                            href="/daily-sales"
                        ),
                        dbc.DropdownMenuItem(
                            'WTD Sales', 
                            href="/wtd-sales"
                        ),
                        dbc.DropdownMenuItem(
                            'MTD Sales', 
                            href="/mtd-sales"
                        ),
                        dbc.DropdownMenuItem(
                            'Weekly Sales', 
                            href="/weekly-sales"
                        ),
                        dbc.DropdownMenuItem(
                            'Monthly Sales', 
                            href="/monthly-sales"
                        ),
                    ],
                    nav=True,
                    in_navbar=True,
                    label='Sales',
                ),
                dbc.DropdownMenu(
                    children=[
                        dbc.DropdownMenuItem(
                            'Bookings Reports', 
                            header=True
                        ),
                        dbc.DropdownMenuItem(
                            'Cover Tracker', 
                            href="/tracker"
                        ),
                        dbc.DropdownMenuItem(
                            'Daily Pickup', 
                            href="/pickup"
                        ),
                        dbc.DropdownMenuItem(
                            'Future Bookings', 
                            href="/future"
                        ),
                        dbc.DropdownMenuItem(
                            'Booking Trends', 
                            href="/trends"
                        ),
                    ],
                    nav=True,
                    in_navbar=True,
                    label='Bookings',
                ),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)
