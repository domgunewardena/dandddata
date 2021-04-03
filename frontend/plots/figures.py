import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

from data.functions import trends_site_filter, trends_table_filter, get_abbreviation
from frontend.styling import review_colors, homepage_colors

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
        )
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
        )
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
        )
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
        xaxis=dict(side='top')
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
        )
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
        )
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
        )
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
        )
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
        )
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
        )
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
        margin=dict(t=30,b=10,l=10,r=10)
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
        )
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
        )
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
        )
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
        )
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
        xaxis = {'title':'% Full'}
    )

    fig.add_vline(
        x=100,
    )
    
    return fig

def homepage_future_summary_figure(covers, empty, full):
        
    bar_color = homepage_colors['covers']
    background_color = homepage_colors['future']

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
            opacity = 0.5
        )
    )

    fig.update_layout(
        title = {
            'text':'Bookings % Full',
            'font':{
                'size':30
            }
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

def homepage_future_worst_figure(dff):
        
    bar_color = homepage_colors['covers']
    background_color = homepage_colors['future']
    
    fig = go.Figure()
    
    fig.add_trace(
        go.Bar(
            x = dff['full']*100,
            y = dff['restaurant'].apply(get_abbreviation),
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
            opacity = 0.5
        )
    )
    fig.add_trace(
        go.Bar(
            x = 100-dff['full']*100,
            y = dff['restaurant'].apply(get_abbreviation),
            marker = {'color':'white'},
            orientation = 'h',
            hovertemplate = '%{x:.0f}% Empty',
            name = "Empty",
            opacity = 0.5
        )
    )


    fig.update_layout(
        title = {
            'text':'Emptiest Restaurants',
            'font':{
                'size':30
            }
        },
        xaxis = {
            'title':'% Full',
            'range':[0,100]
        },
        barmode="relative",
        showlegend = False,
        paper_bgcolor = background_color,
    )

    return fig

def homepage_summary_figure(thisyear, lastyear, pchange, measure):
      
    ylim = max([lastyear*1.1, thisyear*1.35])
    
    plus_sign = '+' if pchange > 0 else ''  
    annotation_text = plus_sign + str(int(pchange)) + '%'

    if measure == 'Covers':
        name = 'Booked Covers'
        hovertemplate = '%{x} %{customdata:.1f}k'
        bar_color = homepage_colors['covers']
        background_color = homepage_colors['future']
    else:
        name = 'Revenue'
        hovertemplate = '%{x} £%{customdata:.1f}k'
        bar_color = homepage_colors['revenue']
        background_color = homepage_colors['past']

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x = ['Last Year', 'This Year'],
            y = [lastyear, thisyear],
            customdata = [lastyear/1000, thisyear/1000],
            name = 'Booked Covers',
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
            'text': measure + ' vs. LY',
            'font':{
                'size':30
            }
        },
        paper_bgcolor = background_color,
    )
    
    return fig
    
def homepage_worst_figure(dff, measure):
    
    if measure == 'Covers':
        restaurant_column = 'Restaurant'
        bar_color = homepage_colors['covers']
        background_color = homepage_colors['future']
        xtitle_string = 'Booked'
    elif measure == 'Revenue':
        restaurant_column = 'SiteName'
        bar_color = homepage_colors['revenue']
        background_color = homepage_colors['past']
        xtitle_string = ''

    ymin = min(dff['vs. LY'])
    
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x = dff['vs. LY'],
            y = dff[restaurant_column].apply(get_abbreviation),
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
            'text':'Lowest ' + measure + ' vs. LY',
            'font':{
                'size':30
            }
        },
        xaxis = {
            'title': xtitle_string + measure + ' vs. LY',
            'range':[ymin*1.5,0]
        },
        paper_bgcolor = background_color,
    )
    
    return fig

def homepage_score_summary_figure(overall):
    
    color = homepage_colors['scores']
    background_color = homepage_colors['past']

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
            'text':'Overall Score',
            'font':{
                'size':30
            }
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

def homepage_score_worst_figure(df):
    
    colorscale = homepage_colors['scores_scale']
    background_color = homepage_colors['past']
    
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            y = df.restaurant.apply(get_abbreviation),
            x = df.overall,
            customdata = df.overall_count,
            mode = 'markers+text',
            marker = dict(
                size = [1,1,1,1,1],
                sizemode='area',
                sizeref=.001,
                sizemin=10,
                color = df.overall,
                coloraxis = 'coloraxis'
            ),
            text = df.overall,
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
            'text':'Lowest Scores',
            'font':{
                'size':30
            }
        },
        xaxis={
            'title':'Average Score'
        },
        paper_bgcolor = background_color,
    )
    
    return fig