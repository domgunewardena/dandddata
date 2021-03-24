import dash
import dash_core_components as dcc
import dash_html_components as html

from app import app
from app import server
from frontend.layouts import *
from frontend.callbacks import *
from frontend.navbar import nav
from authentication.authentication import auth

app.layout = html.Div(
    [
        dcc.Location(
            id='url', 
            refresh=False
        ),
        html.Div([nav]),
        html.Div(id='page-content')
    ]
)

app.title='D&D Data'

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/breakdown':
        return breakdown_layout
    if pathname == '/daily-sales':
        return daily_layout
    if pathname == '/wtd-sales':
        return wtd_layout
    if pathname == '/mtd-sales':
        return mtd_layout
    if pathname == '/weekly-sales':
        return weekly_layout
    if pathname == '/monthly-sales':
        return monthly_layout
    if pathname == '/tracker':
        return tracker_layout
    if pathname == '/pickup':
        return pickup_layout
    if pathname == '/future':
        return future_layout
    if pathname == '/trends':
        return trends_layout
    else:
        return home_page_layout
    
if __name__ == '__main__':
#     app.run_server(debug=False, processes=4)
    app.run_server(debug=False)
