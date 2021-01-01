
import dash

# Sales Dependencies

def dropdown_dependencies(report):
    
    def dropdown_ids(report):
        dropdowns = ['shift','area','measure','metric','site']
        return [report + ' ' + dropdown + ' dropdown' for dropdown in dropdowns]
    
    dropdown_ids = dropdown_ids(report)
    return [dash.dependencies.Input(x, 'value') for x in dropdown_ids]

def week_dropdown_dependencies(report):
    
    def week_dropdown_ids(report):
        dropdowns = ['site','area','category','measure']
        return [report + ' ' + dropdown + ' week dropdown' for dropdown in dropdowns] + [report + ' metric dropdown'] + [report + ' metric week dropdown']

    dropdown_ids = week_dropdown_ids(report)
    return [dash.dependencies.Input(x, 'value') for x in dropdown_ids]

daily_dropdown_dependencies = dropdown_dependencies('daily')
wtd_dropdown_dependencies = dropdown_dependencies('wtd')
mtd_dropdown_dependencies = dropdown_dependencies('mtd')
weekly_dropdown_dependencies = dropdown_dependencies('weekly')
monthly_dropdown_dependencies = dropdown_dependencies('monthly')

wtd_week_dropdown_dependencies = week_dropdown_dependencies('wtd')
mtd_week_dropdown_dependencies = week_dropdown_dependencies('mtd')
weekly_week_dropdown_dependencies = week_dropdown_dependencies('weekly')
monthly_week_dropdown_dependencies = week_dropdown_dependencies('monthly')

tracker_dropdown_ids = ['tracker_week_dropdown','tracker_metric_dropdown','tracker_site_dropdown']
tracker_dropdown_dependencies = [dash.dependencies.Input(x, 'value') for x in tracker_dropdown_ids]

pickup_dropdown_ids = ['pickup_week_dropdown','pickup_metric_dropdown','pickup_site_dropdown']
pickup_dropdown_dependencies = [dash.dependencies.Input(x, 'value') for x in pickup_dropdown_ids]
