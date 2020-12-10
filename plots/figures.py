import plotly.graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd

from data import trends_site_filter, trends_table_filter

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
        ))
    
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
        ))
    
    fig.update_layout(
        title=title,
        yaxis=dict(
            title=measure,
            range=[0,y_limit]
        ))
    
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
    ))
    
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
        ))
    
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
        ))
    
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
        ))
    
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
        ))
    
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
        ))
    
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
        ))
    
    fig.update_layout(
        title=title,
        yaxis=dict(
            title=measure
        ))
    
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
    ))
    
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
        ymax = max(max(dff['max_guests TW']), max(dff['capacity']))
        row = (i*2)+num
        bookings_template = '%{y} - %{customdata} %{x}'
        capacity_template = '%{y}'

        fig.add_trace(
            go.Bar(
                x=dff['visit_day'], 
                y=dff['max_guests TW'],
                name='Covers',
                customdata=dff['weekday'],
                hovertemplate=bookings_template,
                marker=dict(
                    color=dff['full TW'],
                    coloraxis='coloraxis'
                )
            ),
            row=row, col=1
        )   
        fig.add_trace(
            go.Scatter(
                x=dff['visit_day'],
                y=dff['capacity'],
                name='Capacity',
                hovertemplate=capacity_template,
                marker=dict(color='black')
            ),
            row=row, col=1
        ) 

        return fig
    
    lunch_df = df[df['shift_category'] == 'LUNCH']
    dinner_df = df[df['shift_category'] == 'DINNER']
    mondays = [x for x in df['visit_day'].unique() if pd.to_datetime(x).date().weekday() == 0]

    title_strings = [[x + ' - Lunch', x + ' - Dinner'] for x in restaurant_list]
    titles = tuple(title_strings[i][j] for i in range(len(restaurant_list)) for j in [0,1])
    
    fig = make_subplots(
        rows=len(restaurant_list)*2,
        cols=1,
        subplot_titles = titles
    )
    
    for i in range(len(restaurant_list)):
        fig = add_totals(lunch_df, i, 1, restaurant_list, fig)
        fig = add_totals(dinner_df, i, 2, restaurant_list, fig)    
        
    fig.update_layout(
        height=len(restaurant_list)*300,
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
        row = (i*2)+num
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
            row=row, col=1
        )  

        return fig
    
    lunch_df = df[df['shift_category'] == 'LUNCH']
    dinner_df = df[df['shift_category'] == 'DINNER']
    mondays = [x for x in df['visit_day'].unique() if pd.to_datetime(x).date().weekday() == 0]

    title_strings = [[x + ' - Lunch', x + ' - Dinner'] for x in restaurant_list]
    titles = tuple(title_strings[i][j] for i in range(len(restaurant_list)) for j in [0,1])
    
    fig_change = make_subplots(
        rows=len(restaurant_list)*2,
        cols=1,
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
        row='all',col=1
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
