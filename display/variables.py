import dash

# Daily Variables

daily_dropdown_ids = ['daily shift dropdown', 'daily area dropdown', 'daily measure dropdown', 'daily metric dropdown', 'daily site dropdown']
daily_dropdown_dependencies = [dash.dependencies.Input(x, 'value') for x in daily_dropdown_ids]

daily_metrics = ['vs. LW','vs. LY', 'Last Week', 'Last Year']

daily_current_col = 'Today'
daily_last_col = 'Last Week'
daily_vs_col = 'vs. LW'

# WTD Variables

wtd_dropdown_ids = ['wtd shift dropdown', 'wtd area dropdown', 'wtd measure dropdown', 'wtd metric dropdown', 'wtd site dropdown']
wtd_dropdown_dependencies = [dash.dependencies.Input(x, 'value') for x in wtd_dropdown_ids]

wtd_week_dropdown_ids = ['wtd site week dropdown','wtd area week dropdown','wtd category week dropdown','wtd measure week dropdown','wtd metric dropdown','wtd metric week dropdown']
wtd_week_dropdown_dependencies = [dash.dependencies.Input(x, 'value') for x in wtd_week_dropdown_ids]

wtd_metrics = ['vs. LW','vs. LY', 'Last Week', 'Last Year']

wtd_current_col = 'This Week'
wtd_last_col = 'Last Week'
wtd_vs_col = 'vs. LW'

# MTD Variables

mtd_dropdown_ids = ['mtd shift dropdown', 'mtd area dropdown', 'mtd measure dropdown', 'mtd metric dropdown', 'mtd site dropdown']
mtd_dropdown_dependencies = [dash.dependencies.Input(x, 'value') for x in mtd_dropdown_ids]

mtd_week_dropdown_ids = ['mtd site week dropdown','mtd area week dropdown','mtd category week dropdown','mtd measure week dropdown','mtd metric dropdown','mtd metric week dropdown']
mtd_week_dropdown_dependencies = [dash.dependencies.Input(x, 'value') for x in mtd_week_dropdown_ids]

mtd_metrics = ['vs. LM','vs. LY', 'Last Month', 'Last Year']

mtd_current_col = 'This Month'
mtd_last_col = 'Last Month'
mtd_vs_col = 'vs. LM'

# Weekly Variables

weekly_dropdown_ids = ['weekly shift dropdown', 'weekly area dropdown', 'weekly measure dropdown', 'weekly metric dropdown', 'weekly site dropdown']
weekly_dropdown_dependencies = [dash.dependencies.Input(x, 'value') for x in weekly_dropdown_ids]

weekly_week_dropdown_ids = ['weekly site week dropdown','weekly area week dropdown','weekly category week dropdown','weekly measure week dropdown','weekly metric dropdown','weekly metric week dropdown']
weekly_week_dropdown_dependencies = [dash.dependencies.Input(x, 'value') for x in weekly_week_dropdown_ids]

weekly_metrics = ['vs. LW','vs. LY', 'Last Week', 'Last Year']

weekly_current_col = 'This Week'
weekly_last_col = 'Last Week'
weekly_vs_col = 'vs. LW'

# Monthly Variables

monthly_dropdown_ids = ['monthly shift dropdown', 'monthly area dropdown', 'monthly measure dropdown', 'monthly metric dropdown', 'monthly site dropdown']
monthly_dropdown_dependencies = [dash.dependencies.Input(x, 'value') for x in monthly_dropdown_ids]

monthly_week_dropdown_ids = ['monthly site week dropdown','monthly area week dropdown','monthly category week dropdown','monthly measure week dropdown','monthly metric dropdown','monthly metric week dropdown']
monthly_week_dropdown_dependencies = [dash.dependencies.Input(x, 'value') for x in monthly_week_dropdown_ids]

monthly_metrics = ['vs. LM','vs. LY', 'Last Month', 'Last Year']

monthly_current_col = 'This Month'
monthly_last_col = 'Last Month'
monthly_vs_col = 'vs. LM'

# Tracker Variables

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

tracker_dropdown_ids = ['tracker_week_dropdown','tracker_metric_dropdown','tracker_site_dropdown']
tracker_dropdown_dependencies = [dash.dependencies.Input(x, 'value') for x in tracker_dropdown_ids]

# Pickup Variables

pickup_dropdown_ids = ['pickup_week_dropdown','pickup_metric_dropdown','pickup_site_dropdown']
pickup_dropdown_dependencies = [dash.dependencies.Input(x, 'value') for x in pickup_dropdown_ids]
