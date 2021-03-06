import math
import pandas as pd

import plotly.graph_objs as go
from plotly.subplots import make_subplots
import dash_table
import plotly.figure_factory as ff

from data.functions import (
    trends_site_filter, 
    trends_table_filter, 
    get_abbreviation, 
    get_sitename, 
    remove_no_ly,
    k_converter,
    k_change_converter,
    round_converter,
    spend_converter,
    pchange_converter, 
    color_change,
    color_scale_num,
)

from data.date_bounds import date_columns

from frontend.styling import (
    review_colors, 
    graph_colors, 
    title_font_size, 
    sales_table_header_colors,
    sales_table_current_column_colors,
    zero_margin_dict,
    title_margin_dict,
)



# Sales Figures

def sales_totals_figure(
    dff, 
    xcolumn, 
    color_ty, 
    color_ly, 
    template, 
    title, 
    measure,
    current_col,
    change_col,
    base_col
):

    x = dff[xcolumn]
    y_ly = dff[base_col]
    y_ty = dff[current_col]
    customdata_ly = dff[base_col]/1000
    customdata_ty = dff[current_col]/1000
    textposition = 'outside'
#     texttemplate = '%{customdata:+.0f}%'

    max_value = (max(max(y_ly),max(y_ty)))
    y_limit = max_value*1.3

    fig = go.Figure()
    
    fig.add_trace(
        go.Bar(
            x=x,
            y=y_ly,
            customdata=customdata_ly,
            name=base_col,
            marker_color=color_ly,
            hovertemplate=template,
            text=customdata_ly,
            textposition=textposition,
            texttemplate=template
        )
    )
    
    fig.add_trace(
        go.Bar(
            x=x,
            y=y_ty,
            customdata=customdata_ty,
            name=current_col,
            marker_color=color_ty,
            hovertemplate=template,
            text=customdata_ty,
            textposition=textposition,
            texttemplate=template
        )
    )
    
    fig.update_layout(
        title=title,
        yaxis=dict(
            title=measure,
            range=[0,y_limit]
        ),
        paper_bgcolor = graph_colors['background'],
    )
    
    return fig


def sales_change_figure(dff,xcolumn,hovertemplate,title,measure,current_col,change_col,base_col):

    x = dff[xcolumn]
    y = dff[change_col]
    customdata = dff[change_col + ' %']*100
    color = dff[change_col + ' %']
    coloraxis = 'coloraxis'
    cmin=-1
    cmax=1
    textposition = 'outside'
    texttemplate = '%{customdata:+.0f}%'

    max_change = (max(max(y),-min(y)))
    y_limit = max_change*1.4

    fig = go.Figure()
    
    fig.add_trace(
        go.Bar(
            x=x,
            y=y,
            customdata=customdata,
            name=change_col,
            marker=dict(
                color=color,
                coloraxis=coloraxis,
                cmin=cmin,
                cmax=cmax
            ),
            text=customdata,
            textposition=textposition,
            texttemplate=texttemplate,
            hovertemplate=hovertemplate
        )
    )
    
    fig.update_layout(
        title=title,
        yaxis=dict(
            title=measure+' ' + change_col,
            range=[-y_limit,y_limit]
        ),
        coloraxis=dict(
            colorscale='RdYlGn',
            cmin=-1,
            cmax=1,
            showscale=False
        ),
        paper_bgcolor = graph_colors['background'],
    )
    
    return fig

                  
def sales_breakdown_change_figure(dff, title, template, current_col, change_col, base_col):

    x = dff[change_col]
    y = dff["SiteName"]
    customdata = dff[change_col + ' %']*100
    color = dff[change_col + ' %']
    coloraxis = 'coloraxis'
    cmin=-1
    cmax=1
    textposition = 'outside'
    texttemplate = '%{customdata:+.0f}%'

    max_change = (max(max(x),-min(x)))
    x_limit = max_change*1.3
                 
    fig = go.Figure()
    
    fig.add_trace(
        go.Bar(
            x=x,
            y=y,
            customdata=customdata,
            name=change_col,
            orientation='h',
            marker=dict(
                color=color,
                coloraxis = coloraxis,
                cmin=cmin,
                cmax=cmax
            ),
            text=customdata,
            textposition=textposition,
            texttemplate=texttemplate,
            hovertemplate=template
        )
    )
    
    fig.update_layout(
        title=title,
        height=900,
        yaxis=dict(automargin=True),
        xaxis=dict(
            range=[-x_limit,x_limit],
            side='top'
        ),
        coloraxis=dict(
            colorscale='RdYlGn',
            cmin=-1,
            cmax=1,
            showscale=False
        ),
        paper_bgcolor = graph_colors['background'],
    )
    return fig

                  
def sales_breakdown_totals_figure(dff, title, template, color_ly, color_ty, current_col, change_col, base_col):

    x_ty = dff[current_col]
    x_ly = dff[base_col]
    y = dff["SiteName"]
    customdata_ty = (dff[current_col]/1000)
    customdata_ly = (dff[base_col]/1000)
    textposition = 'outside'
    texttemplate = '%{customdata:+.0f}%'

    max_value = (max(max(x_ly),max(x_ty)))
    x_limit = max_value*1.3
                  
    fig = go.Figure()
    
    fig.add_trace(
        go.Bar(
            x=x_ty,
            y=y,
            customdata=customdata_ty,
            name=current_col,
            orientation='h',
            marker_color=color_ty,
            text=customdata_ty,
            textposition=textposition,
            texttemplate=template,
            hovertemplate=template
        )
    )
    
    fig.add_trace(
        go.Bar(
            x=x_ly,
            y=y,
            customdata=customdata_ly,
            name=base_col,
            orientation='h',
            marker_color=color_ly,
            text=customdata_ly,
            textposition=textposition,
            texttemplate=template,
            hovertemplate=template
        )
    )
    
    fig.update_layout(
        title=title,
        showlegend=True,
        height=900,
        yaxis=dict(automargin=True),
        xaxis=dict(side='top'),
        paper_bgcolor = graph_colors['background'],
    )
    return fig

def sales_week_totals_figure(
    dff, 
    y_ly, 
    y_ty,
    color_ly,
    color_ty,
    template, 
    title, 
    measure,
    current_col,
    base_col
):

    x = dff["Day"].astype('str') + ' ' + dff['Session'].astype('str')
    textposition = 'outside'
    
    fig = go.Figure()
    
    fig.add_trace(
        go.Bar(
            x=x,
            y=y_ly,
            customdata=y_ly/1000,
            name=base_col,
            marker_color=color_ly,
            text=y_ly/1000,
            textposition=textposition,
            texttemplate=template,
            hovertemplate=template
        )
    )
    
    fig.add_trace(
        go.Bar(
            x=x,
            y=y_ty,
            customdata=y_ty/1000,
            name=current_col,
            marker_color=color_ty,
            text=y_ty/1000,
            textposition=textposition,
            texttemplate=template,
            hovertemplate=template
        )
    )
    
    fig.update_layout(
        title=title,
        yaxis=dict(
            title=measure
        ),
        paper_bgcolor = graph_colors['background'],
    )
    
    return fig


def sales_week_change_figure(
    dff, 
    y, 
    hovertemplate, 
    title, 
    measure,
    change_col
):

    x = dff["Day"].astype('str') + ' ' + dff['Session'].astype('str')
    color = dff[change_col + ' %']
    coloraxis = 'coloraxis'
    cmin=-1
    cmax=1
    texttemplate = '%{customdata:+.0f}%'
    textposition = 'outside'
    customdata = dff[change_col + ' %']*100
    
    max_change = max(max(y),-min(y))
    y_limit = max_change*1.2
    
    fig = go.Figure()
    
    fig.add_trace(
        go.Bar(
            x=x,
            y=y,
            customdata=customdata,
            name=change_col,
            marker=dict(
                color=color,
                coloraxis=coloraxis,
                cmin=cmin,
                cmax=cmax
            ),
            text=customdata,
            textposition=textposition,
            texttemplate=texttemplate,
            hovertemplate=hovertemplate
    )
    )
    
    fig.update_layout(
        title=title,
        yaxis=dict(
            title=measure + ' ' + change_col,
            range=[-y_limit,y_limit]
        ),
        coloraxis=dict(
            colorscale='RdYlGn',
            cmin=-1,
            cmax=1,
            showscale=False
        ),
        paper_bgcolor = graph_colors['background'],
    )
    return fig

# Tracker Figures

def tracker_totals_figure(dff,x,metric,graph,measure):
    
    if metric=='Last Year':
        y_label,y_acr,y_color = 'Last Year','LY','lightgrey'
    else:
        y_label,y_acr,y_color = 'Last Week','LW','powderblue'

    y_tw = dff['This Week']
    y_comp = dff[y_label]
    name_tw = 'This Week'
    name_comp = y_label
    customdata = dff['vs. '+y_acr+' %']*100
    text_comp = dff['vs. '+y_acr+' %']
    color_tw = 'steelblue'
    color_comp = y_color
    title = graph
    textposition = 'outside'
#     texttemplate = '%{customdata:+.0f}%'
    texttemplate = '%{y:.0f}' if measure == 'Booked Covers' else '%{y:+.0f}'
    hovertemplate = '%{x} %{y:.0f}' if measure == 'Booked Covers' else '%{x} %{y:+.0f}'
    max_change = max(max(y_tw),max(y_comp))
    min_change = min(min(y_tw),min(y_comp))

    y_limit = max_change*1.2
    y_limit_lower = min(min_change, 0)*1.2

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=x,
            y=y_comp,
            customdata=customdata,
            name=name_comp,
            marker=dict(color=color_comp),
            text=customdata,
            textposition=textposition,
            texttemplate=texttemplate,
            hovertemplate=hovertemplate
        )
    )
    fig.add_trace(
        go.Bar(
            x=x,
            y=y_tw,
            customdata=customdata,
            name=name_tw,
            marker=dict(color=color_tw),
            text=customdata,
            textposition=textposition,
            texttemplate=texttemplate,
            hovertemplate=hovertemplate
        )
    )
    fig.update_layout(
        title=title,
        yaxis=dict(
            title=measure + ' ' + metric,
            range=[y_limit_lower,y_limit]
        ),
        paper_bgcolor = graph_colors['background'],
    )

    return fig

def tracker_change_figure(dff,x,metric,graph,measure):

    y = dff[metric]
    name = metric
    customdata = dff[metric + ' %']*100
    text = dff[metric + ' %']
    color = dff[metric + ' %']
    title = graph + ' ' + metric
    textposition = 'outside'
    texttemplate = '%{customdata:+.0f}%'
    hovertemplate = '%{x} %{y:+.0f}'
    coloraxis = 'coloraxis'
    cmin=-1
    cmax=1
    max_change = (max(max(y),-min(y)))
    y_limit = max_change*1.2

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=x,
            y=y,
            customdata=customdata,
            name=metric,
            marker=dict(
                color=color,
                coloraxis = coloraxis,
                cmin=cmin,
                cmax=cmax
            ),
            text=customdata,
            textposition=textposition,
            texttemplate=texttemplate,
            hovertemplate=hovertemplate
        )
    )

    fig.update_layout(
        title=title,
        yaxis=dict(
            title=measure + ' ' + metric,
            range=[-y_limit,y_limit]
        ),
        coloraxis=dict(
            colorscale='RdYlGn',
            cmin=-1,
            cmax=1,
            showscale=False
        ),
        paper_bgcolor = graph_colors['background'],
    )

    return fig

def tracker_breakdown_totals_figure(dff,metric,graph,measure):
    
    x = dff['Restaurant']
    if metric=='Last Year':
        y_label,y_acr,y_color = 'Last Year','LY','lightgrey'
    else:
        y_label,y_acr,y_color = 'Last Week','LW','powderblue'

    y_tw = dff['This Week']
    y_comp = dff[y_label]
    name_tw = 'This Week'
    name_comp = y_label
    customdata = dff['vs. '+y_acr+' %']*100
    text_comp = dff['vs. '+y_acr+' %']
    color_tw = 'steelblue'
    color_comp = y_color
    title = graph + ' ' + metric
    textposition = 'outside'
#     texttemplate = '%{customdata:+.0f}%'
    texttemplate = '%{x:.0f}' if measure=='Booked Covers' else '%{x:+.0f}'
    hovertemplate = '%{y} %{x:.0f}' if measure=='Booked Covers' else '%{y} %{x:+.0f}'
    max_change = max(max(y_tw),max(y_comp))
    min_change = min(min(y_tw),min(y_comp))

    y_limit = max_change*1.2
    y_limit_lower = min(min_change, 0)*1.2

    fig = go.Figure()
    
    fig.add_trace(
        go.Bar(
            orientation='h',
            x=y_tw,
            y=x,
            customdata=customdata,
            name=name_tw,
            marker=dict(color=color_tw),
            text=customdata,
            textposition=textposition,
            texttemplate=texttemplate,
            hovertemplate=hovertemplate
        )
    )
    fig.add_trace(
        go.Bar(
            orientation='h',
            x=y_comp,
            y=x,
            customdata=customdata,
            name=name_comp,
            marker=dict(color=color_comp),
            text=customdata,
            textposition=textposition,
            texttemplate=texttemplate,
            hovertemplate=hovertemplate
        )
    )
    fig.update_layout(
        height=1000,
        title=title,
        xaxis=dict(
            title=measure + ' ' + metric,
            range=[0,y_limit],
            side='bottom'
        ),
        paper_bgcolor = graph_colors['background'],
    )

    return fig

def tracker_breakdown_change_figure(dff,metric,graph,measure):
    
    x = dff['Restaurant']
    y = dff[metric]
    customdata = dff[metric + ' %']*100
    text = dff[metric + ' %']
    color = dff[metric + ' %']
    title = graph + ' ' + metric
    textposition = 'outside'
    texttemplate = '%{customdata:+.0f}%'
    hovertemplate = '%{y} %{x:+.0f}'
    coloraxis = 'coloraxis'
    cmin=-1
    cmax=1
    max_change = (max(max(y),-min(y)))
    y_limit = max_change*1.4

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            orientation='h',
            x=y,
            y=x,
            customdata=customdata,
            name=metric,
            marker=dict(
                color=color,
                coloraxis = coloraxis,
                cmin=cmin,
                cmax=cmax
            ),
            text=customdata,
            textposition=textposition,
            texttemplate=texttemplate,
            hovertemplate=hovertemplate
        )
    )

    fig.update_layout(
        height=1000,
        title=title,
        xaxis=dict(
            range=[-y_limit,y_limit],
            title=measure + ' ' + metric,
        ),
        coloraxis=dict(
            colorscale='RdYlGn',
            cmin=-1,
            cmax=1,
            showscale=False
        ),
        paper_bgcolor = graph_colors['background'],
    )

    return fig


# Future Bookings Figures

def future_totals_figure(restaurant_list, df):
    
    def add_totals(df, i, num, restaurant_list, fig):

        dff = df[df['restaurant'] == restaurant_list[i]]
        ymax = max(max(dff['max_guests TW'], default=0), max(dff['capacity'], default=0))
        
#         row = (i*2)+num
#         col = 1
        row = i+1
        col = num
        
        bookings_template = '%{y} - %{customdata} %{x}'
        capacity_template = '%{y}'
        text_template = '%{y}'

        fig.add_trace(
            go.Bar(
                x=dff['visit_day'], 
                y=dff['max_guests TW'],
                name='Covers',
                customdata=dff['weekday'],
                hovertemplate=bookings_template,
                text=dff['max_guests TW'],
                textposition='auto',
                texttemplate=text_template,
                textangle=0,
                marker=dict(
                    color=dff['full TW'],
                    coloraxis='coloraxis'
                )
            ),
            row=row, col=col
        )   
        fig.add_trace(
            go.Scatter(
                x=dff['visit_day'],
                y=dff['capacity'],
                name='Capacity',
                hovertemplate=capacity_template,
                marker=dict(color='black')
            ),
            row=row, col=col
        ) 

        return fig
    
    lunch_df = df[df['shift'] == 'LUNCH']
    dinner_df = df[df['shift'] == 'DINNER']
    mondays = [x for x in df['visit_day'].unique() if pd.to_datetime(x).date().weekday() == 0]

    title_strings = [[x + ' - Lunch Bookings', x + ' - Dinner Bookings'] for x in restaurant_list]
    titles = tuple(title_strings[i][j] for i in range(len(restaurant_list)) for j in [0,1])
    
    fig = make_subplots(
#         rows=len(restaurant_list)*2,
#         cols=1,
        rows=len(restaurant_list),
        cols=2,
        subplot_titles = titles
    )
    
    for i in range(len(restaurant_list)):
        fig = add_totals(lunch_df, i, 1, restaurant_list, fig)
        fig = add_totals(dinner_df, i, 2, restaurant_list, fig)    
        
    fig.update_layout(
        height=len(restaurant_list)*200,
        coloraxis=dict(
            colorscale='RdYlGn',
            cmin=0,
            cmax=1,
            showscale=False),
        showlegend=False,
        margin=dict(t=30,b=10,l=10,r=10),
        paper_bgcolor = graph_colors['background'],
    )
    
    fig.update_xaxes(
        tickmode='array',
        tickvals=mondays,
        ticktext=['M' for x in range(len(mondays))]
    )
    
    return fig

def future_changes_figure(restaurant_list,df):
    
    def add_changes(df, i, num, restaurant_list, fig):
    
        dff = df[df['restaurant'] == restaurant_list[i]]
        
#         row = (i*2)+num
#         col = 1
        row = i+1
        col = num
        
        bookings_template = '%{y:+.0f} - %{customdata} %{x}'

        fig.add_trace(
            go.Bar(
                x=dff['visit_day'],
                y=dff['max_guests vs LW'],
                name='Covers vs. LW',
                customdata=dff['weekday'],
                hovertemplate=bookings_template,
                marker=dict(
                    color=dff['max_guests vs LW %'],
                    coloraxis='coloraxis'
                )
            ),
            row=row, col=col
        )  

        return fig
    
    lunch_df = df[df['shift'] == 'LUNCH']
    dinner_df = df[df['shift'] == 'DINNER']
    mondays = [x for x in df['visit_day'].unique() if pd.to_datetime(x).date().weekday() == 0]

    title_strings = [[x + ' - Lunch Bookings', x + ' - Dinner Bookings'] for x in restaurant_list]
    titles = tuple(title_strings[i][j] for i in range(len(restaurant_list)) for j in [0,1])
    
    fig_change = make_subplots(
#         rows=len(restaurant_list)*2,
#         cols=1,
        rows=len(restaurant_list),
        cols=2,
        subplot_titles = titles
    )   
    
    for i in range(len(restaurant_list)):
        fig_change = add_changes(lunch_df, i, 1, restaurant_list, fig_change)
        fig_change = add_changes(dinner_df, i, 2, restaurant_list, fig_change) 

    fig_change.update_layout(
        height=len(restaurant_list)*300,
        coloraxis=dict(
            colorscale='RdYlGn',
            cmin=-1,
            cmax=1,
            showscale=False),
        showlegend=False,
        margin=dict(t=30,b=10,l=10,r=10),
        paper_bgcolor = graph_colors['background'],
    )

    fig_change.add_hline(
        y=0,
        opacity=0.2,
        row='all',col='all'
    )
        
    fig_change.update_xaxes(
        tickmode='array',
        tickvals=mondays,
        ticktext=['M' for x in range(len(mondays))]
    )
    return fig_change


# Trends Figures

def trends_group_pickup_figure(df,today_week,today_weekday_num):
    
    weeknums = [today_week + i for i in range(-5,3)]
    weeks = ['5 Weeks Ago', '4 Weeks Ago', '3 Weeks Ago','2 Weeks Ago','Last Week','This Week', 'Next Week', '2 Weeks Time']
    colors = ['Blue']*4 + ['Orange', 'Red', 'Purple', 'Black']
    alphas = [0.2,0.4,0.6,0.8] + [1]*4
    widths = [1]*4 + [4]*4
    weekdays = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

    fig = go.Figure()
    dff = trends_site_filter(trends_table_filter(df, 'This Week Pickup'), 'Group')
    
    ylimit = max(dff['Covers'])*1.05
    for i in range(len(weeks)-2):
        df = dff[dff['Reservation Week'] == weeknums[i]]
        fig.add_trace(
            go.Scatter(
                x = -df['Days Before Week Commencing'],
                y = df['Covers'],
                name = weeks[i],
                mode = 'lines',
                opacity = alphas[i],
                line=dict(color = colors[i],width = widths[i])
            )
        )
    fig.update_layout(
        xaxis=dict(
            tickmode = 'array',
            tickvals = [x for x in range(-14,today_weekday_num+1)],
            ticktext = weekdays*2 + weekdays[:today_weekday_num+1]
        ),
        title=dict(
            text='This Week Pickup - Group',
            x=0.5,
            y=0.85
        ),
        paper_bgcolor = graph_colors['background'],
    )
    fig.add_shape(
        type='line',
        x0=-7,y0=0,x1=-7,y1=ylimit,
        opacity = 0.2
    )
    return fig

def trends_site_pickup_figure(df,restaurant,today_week,today_weekday_num):
    
    weeknums = [today_week + i for i in range(-5,3)]
    weeks = ['5 Weeks Ago', '4 Weeks Ago', '3 Weeks Ago','2 Weeks Ago','Last Week','This Week', 'Next Week', '2 Weeks Time']
    colors = ['Blue']*4 + ['Orange', 'Red', 'Purple', 'Black']
    alphas = [0.2,0.4,0.6,0.8] + [1]*4
    widths = [1]*4 + [4]*4
    weekdays = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    
    fig = go.Figure()
    df = trends_site_filter(trends_table_filter(df, 'This Week Pickup'), 'Sites')
    dff = df[df['Restaurant'] == restaurant]
    ylimit = max(dff['Covers'])*1.05
    for i in range(len(weeks)-2):
        df = dff[dff['Reservation Week'] == weeknums[i]]
        fig.add_trace(
            go.Scatter(
                x = -df['Days Before Week Commencing'],
                y = df['Covers'],
                name = weeks[i],
                mode = 'lines',
                opacity = alphas[i],
                line=dict(color = colors[i],width = widths[i])
            )
        )
    fig.update_layout(
        xaxis=dict(
            tickmode = 'array',
            tickvals = [x for x in range(-14,today_weekday_num+1)],
            ticktext = weekdays*2 + weekdays[:today_weekday_num+1]
        ),
        title=dict(
            text='This Week Pickup - ' + restaurant,
            x=0.5,
            y=0.85
        ),
        paper_bgcolor = graph_colors['background'],
    )
    fig.add_shape(
        type='line',
        x0=-7,y0=0,x1=-7,y1=ylimit,
        opacity = 0.2
    )
    return fig

def trends_group_future_figure(df,today_week,today_weekday_num):
    
    weeknums = [today_week + i for i in range(-5,3)]
    weeks = ['5 Weeks Ago', '4 Weeks Ago', '3 Weeks Ago','2 Weeks Ago','Last Week','This Week', 'Next Week', '2 Weeks Time']
    colors = ['Blue']*4 + ['Orange', 'Red', 'Purple', 'Black']
    alphas = [0.2,0.4,0.6,0.8] + [1]*4
    widths = [1]*4 + [4]*4
    weekdays = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    
    fig = go.Figure()
    dff = trends_site_filter(trends_table_filter(df, 'Future Weeks'), 'Group')
    ylimit = max(dff['Covers'])*1.05
    for i in range(len(weeks)):
        df = dff[dff['Reservation Week'] == weeknums[i]]
        fig.add_trace(
            go.Scatter(
                x = -df['Days Before Week Commencing'],
                y = df['Covers'],
                name = weeks[i],
                mode = 'lines',
                opacity = alphas[i],
                line=dict(color = colors[i],width = widths[i])
            )
        )
    fig.update_layout(
        xaxis=dict(
            tickmode = 'array',
            tickvals = [x for x in range(-21,1)],
            ticktext = weekdays*3 + ['Monday']),
        title=dict(
            text='Future Weeks - Group',
            x=0.5,
            y=0.85
        ),
        paper_bgcolor = graph_colors['background'],
    )
    for i in [-14,-7]:
        fig.add_shape(
            type='line',
            x0=i,y0=0,x1=i,y1=ylimit,
            opacity = 0.2
        )
    return fig

def trends_site_future_figure(df,restaurant,today_week,today_weekday_num):
    
    weeknums = [today_week + i for i in range(-5,3)]
    weeks = ['5 Weeks Ago', '4 Weeks Ago', '3 Weeks Ago','2 Weeks Ago','Last Week','This Week', 'Next Week', '2 Weeks Time']
    colors = ['Blue']*4 + ['Orange', 'Red', 'Purple', 'Black']
    alphas = [0.2,0.4,0.6,0.8] + [1]*4
    widths = [1]*4 + [4]*4
    weekdays = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    
    fig = go.Figure()
    df = trends_site_filter(trends_table_filter(df, 'Future Weeks'), 'Sites')
    dff = df[df['Restaurant'] == restaurant]
    ylimit = max(dff['Covers'])*1.05
    for i in range(len(weeks)):
        df = dff[dff['Reservation Week'] == weeknums[i]]
        fig.add_trace(
            go.Scatter(
                x = -df['Days Before Week Commencing'],
                y = df['Covers'],
                name = weeks[i],
                mode = 'lines',
                opacity = alphas[i],
                line=dict(
                    color = colors[i],
                    width = widths[i]
                )
            )
        )

    fig.update_layout(
        xaxis=dict(
            tickmode = 'array',
            tickvals = [x for x in range(-21,1)],
            ticktext = weekdays*3 + ['Monday']),
        title=dict(
            text='Future Weeks - ' + restaurant,
            x=0.5,
            y=0.85
        ),
        paper_bgcolor = graph_colors['background'],
    )

    for i in [-14,-7]:
        fig.add_shape(
            type='line',
            x0=i,y0=0,x1=i,y1=ylimit,
            opacity = 0.2
        )
    return fig


def score_figure(dff, category):
    
    fig = go.Figure()
    
    fig.add_trace(
        go.Bar(
            x = dff['weeks'],
            y = dff[category],
            customdata = dff[category + '_count'],
            name = category.capitalize() + ' Score',
            marker = {
                'color':dff[category],
                'coloraxis':'coloraxis'
            },
            hovertemplate = '%{y:.1f} - from %{customdata} reviews'
        )
    )

    fig.update_layout(
        title = category.capitalize() + ' Score',
        yaxis = {'range':[0,5]},
        coloraxis={
            'colorscale':'RdYlGn',
            'cmin':0,
            'cmax':5,
            'showscale':False
        },
        paper_bgcolor = graph_colors['background'],
    )
    
    return fig

def score_breakdown_figure(dff, category):
    
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            y = dff[category],
            x = dff['restaurant'],
            customdata = dff[category + '_count'],
            name = category.capitalize() + ' Score',
            marker = {
                'color':dff[category],
                'coloraxis':'coloraxis'
            },
            texttemplate = '%{y:.1f}',
            textposition = 'outside',
            textangle = 0,
            hovertemplate = '%{y:.1f} - from %{customdata} reviews'
        )
    )

    fig.update_layout(
        title = category.capitalize() + ' Scores - Last 4 Weeks',
        yaxis = {'range':[0,6]},
        coloraxis={
            'colorscale':'RdYlGn',
            'cmin':0,
            'cmax':5,
            'showscale':False
        },
        paper_bgcolor = graph_colors['background'],
    )
    
    return fig

def future_breakdown_figure(dff, week):
    
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x = dff['full']*100,
            y = dff['restaurant'],
            marker = {
                'color':dff['full'],
                'coloraxis':'coloraxis'
            },
            orientation = 'h',
            text = dff['full']*100,
            texttemplate = '%{x:.0f}%',
            textposition = 'auto',
            hovertemplate = '%{x:.0f}%',
            name = "Full"
        )
    )

    fig.update_layout(
        title = week + ' Bookings',
        coloraxis={
            'colorscale':'RdYlGn',
            'cmin':0,
            'cmax':1,
            'showscale':False
        },
        xaxis = {'title':'% Full'},
        paper_bgcolor = graph_colors['background'],
    )

    fig.add_vline(
        x=100,
    )
    
    return fig

def homepage_future_summary_figure(covers, empty, full, site):
    
    if site == 'Group':
        title = '% Full'
    else:
        site_name = get_sitename(site)
        title = get_abbreviation(site_name) + ' % Full'
        
    bar_color = graph_colors['covers']
    background_color = graph_colors['background']

    labels = ['Covers', 'Empty Seats']
    values = [covers, empty]
    colors = [bar_color,'lightgrey']
    
    fig = go.Figure()

    fig.add_trace(
        go.Pie(
            labels = labels,
            values = values,
            hole = .6,
            marker = {
                'colors':colors,    
            },
            hoverinfo = 'label+value',
            textinfo = 'none',
        )
    )

    fig.update_layout(
        title = {
            'text':title,
            'font':{'size':title_font_size}
        },
        annotations = [
            dict(
                text = str(int(full*100)) + '%',
                x = 0.5,
                y = 0.5,
                font_size = 40,
                showarrow = False
            ),
        ],
        showlegend = False,
        paper_bgcolor = background_color,
    )

    return fig

def homepage_future_worst_figure(dff, site):
        
    bar_color = graph_colors['covers']
    background_color = graph_colors['background']
    
    if site == 'Group':
        y = dff['restaurant'].apply(get_abbreviation)
        title = 'Emptiest Restaurant'
    else:                
        y = dff['weeks']
        site_name = get_sitename(site)
        title = get_abbreviation(site_name) + ' Upcoming Weeks'
    
    fig = go.Figure()
    
    fig.add_trace(
        go.Bar(
            x = dff['full']*100,
            y = y,
            marker = {
                'color': bar_color,
                'line_color':bar_color,
                'line_width':1.5,
            },
            orientation = 'h',
            text = dff['full']*100,
            texttemplate = '%{x:.0f}%',
            textposition = 'auto',
            hovertemplate = '%{x:.0f}%',
            name = "Full",
        )
    )
    fig.add_trace(
        go.Bar(
            x = 100-dff['full']*100,
            y = y,
            marker = {'color':'white'},
            orientation = 'h',
            hovertemplate = '%{x:.0f}% Empty',
            name = "Empty",
            opacity = 0.5,
        )
    )


    fig.update_layout(
        title = {
            'text':title,
            'font':{'size':title_font_size}
        },
        xaxis = {
            'title':'% Full',
            'range':[0,100]
        },
        barmode="relative",
        showlegend = False,
        paper_bgcolor = graph_colors['background'],
    )

    return fig

def homepage_future_weeks_pie_figure(dff, site):
        
    bar_color = graph_colors['covers']
    background_color = graph_colors['background']
    
    import math
    labels = ['Full','Empty']
    colors = [bar_color,'white']

    specs = [[{'type':'pie'}, {'type':'pie'}], [{'type':'pie'}, {'type':'pie'}]]
    fig = make_subplots(
        rows=2, 
        cols=2, 
        specs=specs,
        subplot_titles = dff['weeks']
    )

    for i in range(len(dff)):

        row = math.floor(i/2) + 1
        col = i%2 + 1

        week = dff['weeks'][i]
        covers = dff['max_guests TW'][i]
        empty = dff.capacity[i] - covers
        full = str(int(dff.full[i]*100)) + '%'

        if empty > 0:
            values = [covers, empty]
        else:
            values = [covers, None]

        fig.add_trace(
            go.Pie(
                labels = labels,
                values = values,
                name = week,
                marker_colors = colors,
                text = [full, None],
                textinfo = 'text',
                textfont_size = 20,
                hoverinfo = 'value'
            ),row, col
        )

        fig.update_layout(
            showlegend = False,
            paper_bgcolor = graph_colors['background'],
        )

    fig.show()
    
    

def homepage_future_weeks_figure(dff, site):
        
    bar_color = graph_colors['covers']
    background_color = graph_colors['background']
    
    sums = dff[['capacity','max_guests TW','empty']].sum()
    capacity = sums[0]
    covers = sums[1]
    empty = capacity-covers
    full = covers/capacity
    full_string = str(int(full*100)) + '%'
    
    if site == 'Group':
        title = '% Full: ' + full_string
    else:                
        site_name = get_sitename(site)
        title = get_abbreviation(site_name) + ' % Full: ' + full_string
        
    x = dff['weeks'].apply(get_abbreviation)
    
    full_y = dff['full']*100    
    full_template = '%{y:.0f}%'
    
    empty_y = 100-dff['full']*100
    empty_template = '%{y:.0f}% Empty'
    
    max_y = max((max(dff['full'])*100), 100)
    y_range = [0,100]    
    
    fig = go.Figure()
    
    fig.add_trace(
        go.Bar(
            x = x,
            y = full_y,
            marker = {
                'color': bar_color,
                'line_color':bar_color,
                'line_width':1.5,
                'opacity':0.5,
            },
            text = full_y,
            texttemplate = full_template,
            textposition = 'auto',
            textfont = {'color':'black'},
            textangle = 0,
            hovertemplate = full_template,
            name = "Full",
        )
    )
    fig.add_trace(
        go.Bar(
            x = x,
            y = empty_y,
            marker = {'color':'white'},
            hovertemplate = empty_template,
            name = "Empty",
            opacity = 0.5,
        )
    )


    fig.update_layout(
        title = {
            'text':title,
            'font':{'size':title_font_size}
        },
        yaxis = {
            'title':'% Full',
            'range':y_range,
        },
        barmode="relative",
        showlegend = False,
        paper_bgcolor = graph_colors['background'],
        margin = title_margin_dict,
    )

    return fig

def homepage_summary_figure(thisyear, lastyear, pchange, measure, site):
    
    if site == 'Group':
        title = measure + ' vs. LY'
    else:
        site_name = get_sitename(site)
        title = get_abbreviation(site_name) + ' ' + measure + ' vs. LY'
      
    ylim = max([lastyear*1.1, thisyear*1.35])
    
    plus_sign = '+' if pchange > 0 else ''  
    annotation_text = plus_sign + str(int(pchange)) + '%'
    
    background_color = graph_colors['background']

    if measure == 'Covers':
        name = 'Booked Covers'
        hovertemplate = '%{x} %{customdata:.1f}k'
        bar_color = graph_colors['covers']
    else:
        name = 'Revenue'
        hovertemplate = '%{x} £%{customdata:.1f}k'
        bar_color = graph_colors['revenue']

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x = ['Last Year', 'This Year'],
            y = [lastyear, thisyear],
            customdata = [lastyear/1000, thisyear/1000],
            name = name,
            text = [None, annotation_text],
            textposition = 'outside',
            textfont_size = 40,
            textangle = 0,
            hovertemplate = hovertemplate,
            marker = {
                'color':bar_color
            },
        )
    )

    fig.update_layout(
        yaxis = {
            'range':[0,ylim]
        },
        title = {
            'text': title,
            'font':{'size':title_font_size}
        },
        paper_bgcolor = background_color,
    )
    
    return fig
    
def homepage_worst_figure(dff, measure, site):
    
    background_color = graph_colors['background']
    
    if measure == 'Covers':
        
        restaurant_column = 'Restaurant'
        site_column = 'Week'
        
        bar_color = graph_colors['covers']
        xtitle_string = 'Booked '
        
    elif measure == 'Revenue':
        
        restaurant_column = 'SiteName'
        site_column = 'LocationName'
        
        bar_color = graph_colors['revenue']
        xtitle_string = ''
        
    if site == 'Group':
        y = dff[restaurant_column].apply(get_abbreviation)
        title = 'Lowest ' + measure + ' vs. LY'
    else:
        y = dff[site_column].apply(get_abbreviation)
        site_name = get_sitename(site)
        title = get_abbreviation(site_name) + ' ' + measure + ' vs. LY'

    xmin = min(dff['vs. LY'])
    xmax = max(dff['vs. LY'])
    
    max_change = max(-xmin, xmax)
    
    if xmax > 0:
        xrange = [-max_change*1.8, max_change*1.8]
    else:
        xrange = [xmin*1.5,0]
    
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x = dff['vs. LY'],
            y = y,
            customdata = dff['vs. LY %']*100,
            marker = {
                'color':bar_color
            },
            orientation = 'h',
            text = dff['vs. LY %'],
            texttemplate = '%{customdata:.0f}%',
            textposition = 'outside',
            textangle = 0,
            hovertemplate = '%{x:.0f}',
            name = "vs. LY",
        )
    )

    fig.update_layout(
        title = {
            'text':title,
            'font':{'size':title_font_size}
        },
        xaxis = {
            'title': xtitle_string + measure + ' vs. LY',
            'range':xrange,
        },
        paper_bgcolor = background_color,
    )
    
    return fig

def homepage_sites_figure(df, measure, site):
    
    background_color = graph_colors['background']
    
    if measure == 'Covers':
        
        restaurant_column = 'Restaurant'
        bar_color = graph_colors['covers']
        xtitle = 'Booked Covers vs. LY'
        df_columns = ['This Week','Last Week','Last Year']
        
    elif measure == 'Revenue':
        
        restaurant_column = 'SiteName'
        bar_color = graph_colors['revenue']
        xtitle = 'Revenue vs. LY'
        df_columns = ['This Month','Last Month','Last Year']
    
    sums = remove_no_ly(df, restaurant_column)[df_columns].sum()
    thisyear = sums[0]
    lastyear = sums[2]
    pchange = ((thisyear - lastyear) / lastyear)*100
    pchange_string = str(int(pchange)) + '%'
    pchange_string = '+' + pchange_string if pchange>0 else pchange_string
    title = measure + ' vs. LY: ' + pchange_string
        
    x = df['vs. LY'].fillna(0)
    xmax = max(max(x),-min(x))
    xrange = [-xmax*2.5,xmax*1.7]
    customdata = df['vs. LY %']*100
    
    y = df[restaurant_column].apply(get_abbreviation)
    
    hovertemplate = '%{customdata:+.0f}%'
    texttemplate = '%{x:+.0f}'
    name = "vs. LY"
    
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x = x,
            y = y,
            customdata = customdata,
            marker = {'color':bar_color,'opacity':0.5},
            orientation = 'h',
            text = customdata,
            texttemplate = texttemplate,
            textposition = 'outside',
            textangle = 0,
            textfont = {'color':'black'},
            hovertemplate = hovertemplate,
            name = name,
        )
    )
    
    
    length = len(df)

    for i in range(length):

        fig.add_annotation(
            y = i,
            x = -xmax*2,
            text = int(list(df[df_columns[0]])[i]),
            showarrow = False,
        )
    
    fig.update_layout(
        xaxis = {
            'range': xrange,
            'visible': False,
        },
        title = {
            'text': title,
            'font':{'size':title_font_size}
        },
        paper_bgcolor = background_color,
        margin = title_margin_dict,
    )
    
    return fig


def homepage_tracker_weeks_figure(dff, site):
    
    background_color = graph_colors['background']
    bar_color = graph_colors['covers']
        
    if site == 'Group':
        title = 'Covers vs. LY'
    else:
        site_name = get_sitename(site)
        title = get_abbreviation(site_name) + ' Covers vs. LY'
        
    y = dff['vs. LY']
    ymax = max(max(y),-min(y))
    ylim = ymax*1.5
    yrange = [-ylim, ylim]
    ytitle = 'Booked Covers vs. LY'
    customdata = dff['vs. LY %']*100
    
    x = dff['Week'].apply(get_abbreviation)
    
    texttemplate = '%{customdata:+.0f}%'
    hovertemplate = '%{y:+.0f}'
    name = "vs. LY"
    
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x = x,
            y = y,
            customdata = customdata,
            marker = {'color':bar_color,'opacity':0.5,},
            text = customdata,
            texttemplate = texttemplate,
            textposition = 'outside',
            textfont = {'color':'black'},
            textangle = 0,
            hovertemplate = hovertemplate,
            name = name,
        )
    )

    fig.update_layout(
        title = {
            'text':title,
            'font':{'size':title_font_size}
        },
        yaxis = {
            'title': ytitle,
            'range': yrange,
        },
        paper_bgcolor = background_color,
        margin = title_margin_dict,
    )
    
    return fig

def homepage_score_figure(df, site):
    
    overall = df['overall'].mean()
    
    colorscale = graph_colors['scores_scale']
    background_color = graph_colors['background']
    
    if site == 'Group':
        
        y = df.restaurant.apply(get_abbreviation)
        x = df.overall
        customdata = df.overall_count
        name = 'Overall Score'
        title = 'Feedback Rating: ' + str(round(overall,1))
        
    else:
        
        y = ['TOTAL','FOOD','SERV','AMBI','VALU'][::-1]
        x = df.score[::-1]
        customdata = df['count'][::-1]
        name = 'Overall Score'
        
        site_name = get_sitename(site)
        title = get_abbreviation(site_name) + ' Scores'
    
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            y = y,
            x = x,
            customdata = customdata,
            mode = 'markers+text',
            marker = dict(
                size = [1]*len(y),
                sizemode = 'area',
                sizeref = .001,
                sizemin = 10,
                color = x,
                coloraxis = 'coloraxis'
            ),
            text = x,
            texttemplate = '%{x:.1f}',
            textposition = 'middle center',
            textfont_size = 20,
            hovertemplate = 'From %{customdata} reviews',
            name = 'Overall Score'
        )
    )

    fig.update_layout(
        coloraxis={
            'colorscale':colorscale,
            'cmin':0,
            'cmax':5,
            'showscale':False,
            'reversescale':True
        },
        title={
            'text':title,
            'font':{'size':title_font_size},
        },
        xaxis={'title':'Average Score'},
        paper_bgcolor = background_color,
        margin = title_margin_dict,
    )
    
    return fig
    
    

def homepage_score_summary_figure(overall, site):
    
    if site == 'Group':
        title = 'Overall Score'
    else:
        site_name = get_sitename(site)
        title = get_abbreviation(site_name) + ' Overall Score'
    
    color = graph_colors['scores']
    background_color = graph_colors['background']

    labels = ['Overall', None]
    values = [overall, 5-overall]
    colors = [color,'lightgrey']
    
    fig = go.Figure()

    fig.add_trace(
        go.Pie(
            labels = labels,
            values = values,
            hole = .5,
            marker = {
                'colors':colors,    
            },
            hoverinfo = 'label+value',
            textinfo = 'none'
        )
    )

    fig.update_layout(
        title = {
            'text':title,
            'font':{'size':title_font_size}
        },
        annotations = [
            dict(
                text = str(round(overall,1)),
                x = 0.5,
                y = 0.5,
                font_size = 50,
                showarrow = False
            ),
        ],
        showlegend = False,
        paper_bgcolor = background_color,
    )
    
    return fig

def homepage_score_worst_figure(df, site):
    
    colorscale = graph_colors['scores_scale']
    background_color = graph_colors['background']
    
    if site == 'Group':
        
        y = df.restaurant.apply(get_abbreviation)
        x = df.overall
        customdata = df.overall_count
        name = 'Overall Score'
        title = 'Lowest Scores'
        
    else:
        
        y = ['TOTAL','FOOD','SERV','AMBI','VALU'][::-1]
        x = df.score[::-1]
        customdata = df['count'][::-1]
        name = 'Overall Score'
        
        site_name = get_sitename(site)
        title = get_abbreviation(site_name) + ' Scores'
    
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            y = y,
            x = x,
            customdata = customdata,
            mode = 'markers+text',
            marker = dict(
                size = [1,1,1,1,1],
                sizemode='area',
                sizeref=.001,
                sizemin=10,
                color = x,
                coloraxis = 'coloraxis'
            ),
            text = x,
            texttemplate = '%{x:.1f}',
            textposition = 'middle center',
            textfont_size=20,
            hovertemplate = 'From %{customdata} reviews',
            name = 'Overall Score'
        )
    )

    fig.update_layout(
        coloraxis={
            'colorscale':colorscale,
            'cmin':0,
            'cmax':5,
            'showscale':False,
            'reversescale':True
        },
        title={
            'text':title,
            'font':{'size':title_font_size}
        },
        xaxis={
            'title':'Average Score'
        },
        paper_bgcolor = background_color,
    )
    
    return fig

def detail_sales_figure(df, ycolumn):
    
    background_color = graph_colors['background']
    bar_color = graph_colors['revenue']
    
    sums = df[['This Month','Last Month','Last Year']].sum()
    thisyear = sums[0]
    lastyear = sums[2]
    pchange = ((thisyear - lastyear) / lastyear)*100
    pchange_string = str(int(pchange)) + '%'
    pchange_string = '+' + pchange_string if pchange>0 else pchange_string

    y = df[ycolumn]

    x = df['vs. LY']
    xmax = max(max(x), -min(x))
    xrange = [-xmax*1.3,xmax*1.3]

    customdata = df['vs. LY %']*100
    texttemplate = '%{customdata:+.0f}%'
    hovertemplate = '£%{x:.0f}'

    title = measure.capitalize() + ' vs. LY'

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x = x,
            y = y,
            customdata = customdata,
            marker = {'color':bar_color,'opacity':0.5},
            text = customdata,
            texttemplate = texttemplate,
            textposition = 'outside',
            hovertemplate = hovertemplate,
            name = 'vs. LY',
            orientation = 'h',
        )
    )
    fig.update_layout(
        title = {
            'text':title,
            'font':{'size':title_font_size}
        },
        xaxis = {
            'title':title,
            'range':xrange,
        },
    )

    return fig
    
def detail_tracker_figure(df):
    
    background_color = graph_colors['background']
    bar_color = graph_colors['covers']
    
    x = df['Week']

    y = df['vs. LY']
    ymax = max(max(y),-min(y))
    yrange = [-ymax*1.3,ymax*1.3]

    customdata = df['vs. LY %']*100
    texttemplate = '%{customdata:+.0f}%'
    hovertemplate = '%{y:+.0f}'

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x = x,
            y = y,
            customdata = customdata,
            text = customdata,
            texttemplate = texttemplate,
            textposition = 'outside',
        )
    )

    fig.update_layout(
        yaxis={
            'range':yrange, 
            'title':'Booked Covers vs LY'
        },
        paper_bgcolor = background_color,
    )
    
    return fig

def detail_future_figure(dff):
    
    lunch_df = dff[dff['shift']=='LUNCH']
    dinner_df = dff[dff['shift']=='DINNER']

    x1 = lunch_df.visit_day
    y1 = lunch_df['full']*100
    customdata1 = lunch_df.weekday

    x2 = dinner_df.visit_day
    y2 = dinner_df['full']*100
    customdata2 = dinner_df.weekday

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x = x2,
            y = 100-y2,
            marker={'color':'white','opacity':0.5},
            hovertemplate = '%{x}',
            texttemplate = '%{y}',
            textangle = 0,
        )
    )

    fig.add_trace(
        go.Bar(
            x = x2,
            y = y2,
            customdata = customdata2,
            marker={'color':'blue','opacity':0.5},
            name = 'Dinner Covers',
            hovertemplate = '%{customdata} %{x}',
        )
    )

    fig.add_trace(
        go.Bar(
            x = x1,
            y = y1,
            customdata = customdata1,
            marker={'color':'green','opacity':0.5},
            name = 'Lunch Covers',
            hovertemplate = '%{customdata} %{x}',
        )
    )

    fig.add_trace(
        go.Bar(
            x = x1,
            y = 100-y1,
            marker={'color':'white','opacity':0.5},
            hovertemplate = '%{y}'  ,
            texttemplate = '%{y}',
            textangle = 0,
        )
    )

    for i in range(len(lunch_df.weekday)):

        color = 'white' if list(y2)[i] > 10 else 'black'

        fig.add_annotation(
            x = list(x1)[i],
            y = 95,
            text = list(lunch_df.weekday)[i][0],
            showarrow = False,
            font = {'color':color}
        )

    fig.update_layout(
        barmode = 'stack',
        showlegend = False,
        xaxis = {'tickvals':customdata},
        yaxis = {'range':[0,200]}
    )
    
    
def homepage_sales_figure(df, current_column):
    
    background_color = graph_colors['background']
    bar_color = graph_colors['revenue']
    
    sums = df.iloc[:,1:].sum()
    lastyear = sums[2]
    vsly = sums[4]
    pchange = (vsly / lastyear)*100
    pchange_string = str(int(pchange)) + '%'
    pchange_string = '+' + pchange_string if pchange>0 else pchange_string
    title = 'Revenue vs. LY: ' + pchange_string
    
    y = df['SiteName'].apply(get_abbreviation)
    x = df['vs. LY']

    xmax = max(max(x.fillna(0)),-min(x.fillna(0)))
    customdata = df['vs. LY %']*100

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x = x,
            y = y,
            customdata = customdata,
            marker = {'color':bar_color,},
            orientation = 'h',
            text = customdata,
            texttemplate = '%{customdata:.0f}%',
            textposition = 'outside',
            textangle = 0,
            hovertemplate = '£%{x:.0f}',
            name = "vs. LY",
        )
    )

    length = len(df)

    for i in range(length):

        fig.add_annotation(
            y = i,
            x = -xmax*2.5,
            text = currency_k(list(df[current_column])[i]),
            showarrow = False,
        )

        if currency_k(list(df['Last Year'])[i]):

            fig.add_annotation(
                y = i,
                x = -xmax*2,
                text = currency_k(list(df['Last Year'])[i]),
                showarrow = False,
            )

    fig.update_layout(
        title = {
            'text': title,
            'font':{'size':title_font_size}
        },
        xaxis = {
            'range' : [-xmax*3,xmax*1.3],
            'visible':False,

        },
        paper_bgcolor = background_color,
    )

    return fig
    
    
def homepage_sales_table_figure(df, current_column):

    row_height = 30
    font_size = 15
    restaurant_column_width = 200
    column_width = 50

    fig = go.Figure()

    fig.add_trace(
        go.Table(
            columnwidth = [restaurant_column_width] + [column_width]*4,
            header = {
                'values':['Restaurant','TY','LY','vs LY', '%'],
                'align':['left','right','right'],
                'fill_color':'navy',
                'font':{
                    'color':'white',
                    'size':font_size,
                    'family':"Open Sans, sans-serif"
                },
                'height':row_height,
            },
            cells = {
                'values':[
                    df['SiteName'].apply(get_abbreviation),
                    df[current_column].apply(currency_k),
                    df['Last Year'].apply(currency_k),     
                    df['vs. LY'].apply(currency_k_change),
                    df['vs. LY %'].apply(pchange),
                ],
                'font':{'size':font_size},
                'align':['left'] + ['right']*4,
                'height':row_height,
                'fill_color':[(['AliceBlue','white']*math.floor(len(df)/2) + ['AliceBlue']*(len(df)%2))]*3 + [list(df['vs. LY'].apply(color_change))] + [list(df['vs. LY %'].apply(color_change))]
            },
        ),
    )

    fig.show()
    
def homepage_sales_datatable_figure(df, report):
        
    current_column = date_columns['current'][report]
    last_column = date_columns['last'][report]
    vs_column = date_columns['vs'][report]
    vs_p_column = date_columns['vs'][report] + ' %'
    
    current_abbr = date_columns['curr_abbr'][report]
    last_abbr = date_columns['last_abbr'][report]
    p_abbr = date_columns['p_abbr'][report]
    
    cols = ['SiteName', current_column, last_column, vs_p_column, 'Last Year', 'vs. LY %']
    
    column_rename_map = {
        'SiteName':'REST',
        current_column:current_abbr,
        last_column:last_abbr,
        vs_p_column:p_abbr,
        'Last Year':'LY',
        'vs. LY %':'LY%',
    }
    
    df = df[cols].rename(columns = column_rename_map)
    
    actual_cols = [current_abbr,last_abbr,'LY']
    pchange_cols = [p_abbr, 'LY%']
    
    df['REST'] = df['REST'].apply(get_abbreviation)
    
    for col in actual_cols:
        df[col] = df[col].apply(currency_k)
        
    for col in pchange_cols:
        df[col] = df[col].apply(pchange)
        
    header_color = sales_table_header_colors[report]
    row_1_color = 'rgb(230,230,230)'
    row_2_color = 'GhostWhite'
    colorscale = [
        [0, header_color],
        [.5, row_1_color],
        [1, row_2_color],
    ]
    
    fig = ff.create_table(
        df.fillna(''),
        colorscale = colorscale,
    )
    
    return fig
    
def sales_heatmap_figure(df, timeframe, measure, report):
    
    df_length = len(df)
    
    if report == 'homepage':
        blank_row_index_pos = df_length - 3
    elif report == 'breakdown':
        blank_row_index_pos = df_length - 1
    
    background_color = graph_colors['background']
        
    current_column = date_columns['current'][timeframe]
    last_column = date_columns['last'][timeframe]
    vs_column = date_columns['vs'][timeframe]
    vs_p_column = date_columns['vs'][timeframe] + ' %'
    
    current_abbr = date_columns['curr_abbr'][timeframe]
    last_abbr = date_columns['last_abbr'][timeframe]
    p_abbr = date_columns['p_abbr'][timeframe]
    
    red = 'rgb(255,0,0)'
    green = 'rgb(0,255,0)'
    grey = 'rgb(230,230,230)'
    current_column_color = sales_table_current_column_colors[timeframe]
    
    if measure == 'Revenue':
        actuals_converter = k_converter
    elif measure == 'Covers':
        actuals_converter = round_converter
    elif measure == 'Spend':
        actuals_converter = spend_converter
    
    color_scale = [
        [.0, red],
        [.25, 'white'],
        [.5, green],
        [.6, 'white'],
        [.8, grey],
        [1, current_column_color],
    ]

    z = [
        [
            round(0.9 + (i%2)*0.1,1),
            round(0.7 + (i%2)*0.1,1),
            df[vs_p_column].apply(color_scale_num).fillna(.25)[i],
            round(0.7 + (i%2)*0.1,1),
            df['vs. LY %'].apply(color_scale_num).fillna(.25)[i],
        ] for i in range(df_length)
    ][::-1]
    
    z.insert(blank_row_index_pos, [.7]*5)
    
#     hover_text = [
#         [
#             round(df[current_column][i]),
#             round(df[last_column][i]),
#             round(df[vs_column][i]),
#             round(df['Last Year'][i]),
#             round(df['vs. LY'][i]),
#         ] for i in range(df_length)
#     ][::-1]

    z_text = [
        [
            df.apply(lambda x: actuals_converter(x[current_column],x['SiteName']),axis=1)[i],
            df.apply(lambda x: actuals_converter(x[last_column],x['SiteName']),axis=1)[i],
            df[vs_p_column].apply(pchange_converter)[i],
            df.apply(lambda x: actuals_converter(x['Last Year'],x['SiteName']),axis=1)[i],
            df['vs. LY %'].apply(pchange_converter)[i],
        ] for i in range(df_length)
    ][::-1]
    
    z_text.insert(blank_row_index_pos, ['']*5)

    y = list(df.SiteName.apply(get_abbreviation))[::-1]
    y.insert(blank_row_index_pos,'')
    
    x = [
        current_abbr,
        last_abbr,
        p_abbr,
        'LY',
        'LY%'
    ]


    fig = ff.create_annotated_heatmap(
        z, 
        x = x,
        y = y,
        annotation_text = z_text,
        colorscale = color_scale,
#         text = hover_text,
#         hoverinfo = 'text',
        font_colors = ['black','black'],
    )

    fig.update_layout(
        paper_bgcolor = background_color,
        margin = zero_margin_dict,
    )
    
    return fig