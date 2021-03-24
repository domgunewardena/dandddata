import dash
import dash_bootstrap_components as dbc

def Navbar():
    
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Breakdown", href="/breakdown")),
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
