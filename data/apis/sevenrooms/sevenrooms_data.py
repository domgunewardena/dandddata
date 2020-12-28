from datetime import datetime, date, timedelta
import pandas as pd
import glob

import restaurant_mapping

class SevenRoomsData:
    
    C_Drive = "C:/Users/domg/"
    C_Drive_Database = C_Drive + 'Databases/Reservations Database/'
    
    N_Drive = "//ddlfp02/headoffice$/marketing/Dom/"
    N_Drive_Database = N_Drive + "Databases/Reservations/"
    N_Drive_Forecasts = N_Drive + "Operations/Forecasts/"
    
    def __init__(self, reservations, restaurant_ids, location):
        
        self.reservations = reservations
        self.restaurant_ids = restaurant_ids
        self.location = location
        
        self.sr_data = self.generate_sr_data()
        self.sevenrooms_data = self.generate_sevenrooms_data()
        self.tracker_data = self.generate_tracker_data_data()
        self.historic_tracker_data = self.generate_historic_tracker_data()
        self.shift_covers_data = self.generate_shift_covers_data()
        self.future_bookings_data = self.generate_future_bookings_data()
        self.booking_trends_data = self.generate_booking_trends_data()
        self.tracker_app_data,self.pickup_data = self.generate_app_tracker_data()
        
    def generate_sr_data(self):
        
        def merge_api_results():
            
            return pd.merge(
                self.reservations, 
                self.restaurant_ids,
                how="outer",
                left_on="venue_id",
                right_on="venue_id"
            ).dropna(subset=["updated"])
        
        def add_date_columns(df):
            
            date_columns = ['updated','created']
            
            for date_col in date_columns:
                
                df[date_col + '_day'] = df[date_col].str.split('T',expand=True)[0]
                df[date_col + '_time'] = df[date_col].str.split('T',expand=True)[1].str.split(".", expand=True)[0]
                df[date_col + '_date'] = pd.to_datetime(df[[date_col + "_day",date_col + "_time"]].astype(str).apply(' '.join, axis=1))

            df["visit_date"] = pd.to_datetime(df[["date","arrival_time"]].astype(str).apply(' '.join, axis=1))

            return df
        
        def add_name_columns(df):
            
            df["first"] = df["first_name"].str.strip()
            df["last"] = df["last_name"].str.strip()
            df["guest_name"] = df[["first","last"]].astype(str).apply(' '.join, axis=1)
            
            return df

        return add_name_columns(
            add_date_columns(
                merge_api_results()
            )
        )
    
    def generate_sevenrooms_data(self):
        
        def get_sevenrooms_data_columns(df):
            
            target_columns = [
                "restaurant",
                 "visit_date",
                 "created_date",
                 "client_id",
                 "guest_name",
                 "email",
                 "reservation_type",
                 "status_simple",
                 "booked_by",
                 "phone_number",
                 "shift_category",
                 "max_guests",
                 "notes"
            ]

            return df[target_columns]
        
        def add_date_columns(df):

            date_columns = ['visit', 'created']

            for date_column in date_columns:
                df[date_column + "_day"] = df[date_column + "_date"].dt.date.astype(str)
                df[date_column + "_time"] = df[date_column + "_date"].dt.time.astype(str)
                df[date_column + "_week"] = df[date_column + "_date"].dt.week
                df[date_column + "_dayofweeknum"] = df[date_column + "_date"].dt.dayofweek+1
                df[date_column + "_dayofweek"] = df[date_column + "_date"].dt.weekday_name
                df[date_column + "_dayofmonth"] = df[date_column + "_date"].dt.day
                df[date_column + "_monthnum"] = df[date_column + "_date"].dt.month
                df[date_column + "_month"] = df[date_column + "_date"].dt.month_name()
                df[date_column + "_year"] = df[date_column + "_date"].dt.year

            return df
        
        df = self.sr_data.copy()
        
        return add_date_columns(
            get_sevenrooms_data_columns(
                df
            )
        )
    
    def generate_tracker_data_data(self):
        
        def add_cancelled_day_column(df):
            
            df["cancelled_day"] = ""
            return df
        
        def map_restaurants_to_looker_values(df):
            
            restaurant_map = restaurant_mapping.sevenrooms_to_looker_map
            df["restaurant2"] = df["restaurant"].map(restaurant_map)
            return df

        def map_statuses_to_looker_values(df):
            
            status_map = {
                'Canceled':'Cancelled',
                'Incomplete':'Future Reservation',
                'No Show': 'No Show',
                'Complete':'Completed'
            }

            df["state"] = df["status_simple"].map(status_map)
            
            return df

            
        def group_by_tracker_data_columns(df):
            
            df_columns = [
                "restaurant2", 
                "state",
                "visit_day",
                "created_day",
                "cancelled_day",
                'shift_category',
                "max_guests"
            ]

            groupby_columns = df_columns[:-1]

            return df[df_columns].groupby(by=groupby_columns).sum().reset_index()
        
        df = self.sevenrooms_data.copy()
        
        return group_by_tracker_data_columns(
            map_statuses_to_looker_values(
                map_restaurants_to_looker_values(
                    add_cancelled_day_column(
                        df
                    )
                )
            )
        )
    
    def generate_historic_tracker_data(self):
        
        def filter_reservations_by_future(df):
            
            return df[df["state"] == "Future Reservation"]
        
        def group_by_historic_data_columns(df):
            
            df_columns = ["restaurant2", "visit_day", "max_guests"]
            groupby_columns = ["restaurant2", "visit_day"]
            
            return df[df_columns].groupby(groupby_columns).sum().reset_index()
        
        def add_as_of_column(df):

            today = date.today().strftime("%Y-%m-%d")
            df['As of'] = today
            return df

        def append_to_historic_tracker_csv(df):
            
            csv = "Historic_Tracker_Data.csv"
            columns = ["restaurant2", "visit_day", "max_guests", "As of"]
            historic_tracker = pd.read_csv(csv)[columns]

            return pd.concat([historic_tracker, df])
        
        df = self.tracker_data.copy()
        
        return append_to_historic_tracker_csv(
            add_as_of_column(
                group_by_historic_data_columns(
                    filter_reservations_by_future(
                        df
                    )
                )
            )
        )
    
    def generate_shift_covers_data(self):
        
        def filter_reservations_by_future(df):
            
            return df[df['status_simple'] == 'Incomplete']
        
        def create_new_shift_column(df):
            
            def get_lunch_values(restaurant, time, shift):
    
                if restaurant in ['Madison Restaurant', '20 Stories']:
                    return 'LUNCH' if time < '17:00:00' else 'DINNER'
                else:
                    return 'LUNCH' if shift in ['BREAKFAST', 'BRUNCH', 'DAY', 'LUNCH'] else shift
            
            df['shift'] = df.apply(lambda x: get_lunch_values(x['restaurant'],x['visit_time'],x['shift_category']), axis=1)
            
            return df
            
        def group_by_shift_covers_columns(df):
            
            df_columns = ['visit_day','restaurant','shift', 'max_guests']
            groupby_columns = df_columns[:-1]

            return df[df_columns].groupby(groupby_columns).sum().reset_index()
        
        df = self.sevenrooms_data.copy()
        
        return group_by_shift_covers_columns(
            create_new_shift_column(
                filter_reservations_by_future(
                    df
                )
            )
        )

    def generate_future_bookings_data(self):
        
        def read_old_csv(self):
            
            if self.location == 'laptop':
                old_csv_path = "ShiftCovers/ShiftCovers "
            else:
                old_csv_path = self.N_Drive_Forecasts + "Future Bookings/ShiftCovers/ShiftCovers "

            date_string = (date.today()-timedelta(7)).strftime('%d-%b-%Y')

            return pd.read_csv(glob.glob(old_csv_path + date_string + '*')[0]).iloc[:,1:]

        def future_bookings_df(input_df, week):
            
            def convert_date_to_correct_format(df, week):
                
                # add 7 days to last week's data to produce an accurate vs. LW comparison
                days = 7 if week=='last' else 0
                df['visit_day'] = (pd.to_datetime(df['visit_day']) + timedelta(days)).dt.strftime('%Y-%m-%d')
                return df
            
            def map_restaurants_to_app_values(df):
                
                restaurant_map = restaurant_mapping.shift_covers_to_app_map
                df['restaurant'] = df['restaurant'].map(restaurant_map)
                return df
            
            def group_by_future_columns(df):

                df_columns = ['visit_day','restaurant','shift','max_guests']
                groupby_columns = df_columns[:-1]
                return df[df_columns].groupby(groupby_columns).sum().reset_index()
                
            def create_skeleton_df():
                
                report_restaurants = restaurant_mapping.app_restaurants
            
                today = datetime.today()
                dates = [x.date().strftime('%Y-%m-%d') for x in pd.date_range(start=today, periods=30)]
                skeleton = pd.DataFrame([[date, restaurant, shift] for date in dates for restaurant in report_restaurants for shift in ['LUNCH', 'DINNER']])
                skeleton.columns=['visit_day', 'restaurant', 'shift']
                return skeleton
                
            def merge_with_skeleton_df(input_df):
                
                skeleton = create_skeleton_df()
                
                return pd.merge(
                    left=skeleton, 
                    right=input_df, 
                    how='outer'
                ).fillna(0)
            
            def filter_by_skeleton_dates(df):
                
                skeleton = create_skeleton_df()
                
                mask1 = df['visit_day'] <= skeleton.visit_day.unique()[-1]
                mask2 = df['visit_day'] >= skeleton.visit_day.unique()[0]
                
                return df[mask1 & mask2]
            
            def create_capacity_columns(df):
                
                capacities = restaurant_mapping.capacities
                df['capacity'] = df['restaurant'].map(capacities)
                df['full'] = (df['max_guests']/df['capacity']).fillna(0)
                return df
            
            df = input_df.copy()
            
            return create_capacity_columns(
                filter_by_skeleton_dates(
                    merge_with_skeleton_df(
                        group_by_future_columns(
                            map_restaurants_to_app_values(
                                convert_date_to_correct_format(
                                    df,week
                                )
                            )
                        )
                    )
                )
            )

        shift_covers = self.shift_covers_data.copy()
        old_shift_covers = read_old_csv(self)
        
        current = future_bookings_df(shift_covers,'this')
        lastweek = future_bookings_df(old_shift_covers,'last')
        
        def merge_week_dfs(current,lastweek):

            return pd.merge(
                left=current,
                right=lastweek,
                how='outer',
                on=['visit_day','restaurant','shift','capacity'],
                suffixes=(' TW',' LW')
            ).fillna(0)
        
        def add_comparison_columns(df):
            
            df['max_guests vs LW'] = (df['max_guests TW']-df['max_guests LW'])
            df['max_guests vs LW %'] = ((df['max_guests TW'].replace(0,1)/df['max_guests LW'].replace(0,1))-1).fillna(0)
            return df

        return add_comparison_columns(
            merge_week_dfs(
                current,
                lastweek
            )
        )
    
    def generate_booking_trends_data(self):

        today_weekday_num = date.today().weekday()
        today_week = date.today().isocalendar()[1]

        def read_csv(csv_path):

            date_columns = ['visit_day', 'As of']

            df = pd.read_csv(csv_path).iloc[:,1:5]

            for x in date_columns:
                df[x] = pd.to_datetime(df[x])

            df.columns = ['Restaurant', 'Reservation Date','Covers','As Of Date']

            return df

        def add_date_columns(df):

            def week_commencing(x):
                return x[0] - timedelta(x[1])

            df["Reservation Week"] = df["Reservation Date"].dt.week
            df['Reservation Weekday Num'] = df["Reservation Date"].dt.weekday
            df["Reservation Day"] = df["Reservation Date"].dt.day_name()
            df["As Of Day"] = df['As Of Date'].dt.day_name()
            df['Week Commencing'] = df[['Reservation Date', 'Reservation Weekday Num']].apply(week_commencing, axis=1)
            df['Days Before Week Commencing'] = (df['Week Commencing'] - df['As Of Date']).dt.days

            return df

        def map_restaurants_to_app_values(df):

            restaurant_map = restaurant_mapping.tracker_data_to_app_map
            df['Restaurant'] = df['Restaurant'].map(restaurant_map)
            return df
            
        def filter_by_days_left_in_the_week(df, graph):
            
            if graph == 'This Week Pickup':
                return df[df['Reservation Weekday Num'] >= today_weekday_num]
            else:
                return df

        def filter_by_days_before_week_commencing(df, graph):    
            
            if graph == 'This Week Pickup':
                lower_limit = -today_weekday_num
                upper_limit = 15
            else:
                lower_limit = 0
                upper_limit = 22   
                
            mask1 = df['Days Before Week Commencing'] >= lower_limit
            mask2 = df['Days Before Week Commencing'] < upper_limit
            
            return df[mask1 & mask2]

        def group_by_booking_trends_columns(df):

            df_columns = [
                "Restaurant",
                "As Of Day", 
                "Days Before Week Commencing",
                "Reservation Week", 
                "Covers"
            ]

            groupby_columns = df_columns[:-1]

            return df[df_columns].groupby(groupby_columns).sum().reset_index().fillna(0).sort_values('Days Before Week Commencing', ascending=False)

        def create_group_df(df):
            
            df_columns = ['As Of Day', 'Days Before Week Commencing', 'Reservation Week', 'Covers']
            groupby_columns = df_columns[:-1]
            
            return df[df_columns].groupby(groupby_columns).sum().reset_index().sort_values(by='Days Before Week Commencing', ascending = False)
        
        def merge_group_and_restaurants_dfs(restaurant_df, group_df):
            
            group_df['Restaurant'] = 'Group'
            group_df = group_df[['Restaurant','As Of Day', 'Days Before Week Commencing', 'Reservation Week','Covers']]
            
            return group_df.append(restaurant_df, ignore_index=True)
        
        def combine_pickup_and_future_dfs(this_week_pickup,future_weeks):
            
            this_week_pickup['Table'] = 'This Week Pickup'
            future_weeks['Table'] = 'Future Weeks'

            return this_week_pickup.append(future_weeks, ignore_index=True)
        
        def filter_by_weeks(df):
            
            five_weeks_ago = today_week-5
            two_weeks_ahead = today_week+2

            mask1 = df['Reservation Week'] >= five_weeks_ago
            mask2 = df['Reservation Week'] <= two_weeks_ahead

            return df[mask1 & mask2]
        
        def add_weekname_and_color_and_alpha_columns(df):

            weeknums = [today_week + i for i in range(-5,3)]
            weeks = ['5 Weeks Ago', '4 Weeks Ago', '3 Weeks Ago','2 Weeks Ago','Last Week','This Week', 'Next Week', '2 Weeks Time']
            colors = ['Blue']*4 + ['Orange', 'Red', 'Purple', 'Black']
            alphas = [0.2,0.4,0.6,0.8,1,1,1,1]

            week_map = dict(zip(weeknums, weeks))
            color_map = dict(zip(weeknums, colors))
            alpha_map = dict(zip(weeknums, alphas))

            cols = ['Week', 'Color', 'Alpha']
            maps = [week_map, color_map, alpha_map]

            for i in range(len(cols)):
                df[cols[i]] = df['Reservation Week'].map(maps[i])

            return df
        
        
        if self.location == 'laptop':
            csv_path = "Historic_Tracker_Data.csv"
        else:
            csv_path = self.C_Drive_Database + "Historic_Tracker_Data.csv"            
        
        graph = "This Week Pickup"
        this_week_pickup_restaurant_df = group_by_booking_trends_columns(
            filter_by_days_before_week_commencing(
                filter_by_days_left_in_the_week(
                    map_restaurants_to_app_values(
                        add_date_columns(
                            read_csv(csv_path)
                        )
                    ),graph
                ),graph
            )
        )
        this_week_pickup_group_df = create_group_df(this_week_pickup_restaurant_df)
        
        graph = "Future Weeks"
        future_weeks_restaurant_df = group_by_booking_trends_columns(
            filter_by_days_before_week_commencing(
                filter_by_days_left_in_the_week(
                    map_restaurants_to_app_values(
                        add_date_columns(
                            read_csv(csv_path)
                        )
                    ),graph
                ),graph
            )
        )
        future_weeks_group_df = create_group_df(future_weeks_restaurant_df)
        
        this_week_pickup = merge_group_and_restaurants_dfs(this_week_pickup_restaurant_df, this_week_pickup_group_df)
        future_weeks = merge_group_and_restaurants_dfs(future_weeks_restaurant_df, future_weeks_group_df)
        
        return add_weekname_and_color_and_alpha_columns(
            filter_by_weeks(
                combine_pickup_and_future_dfs(
                    this_week_pickup,
                    future_weeks
                )
            )
        )
    
    def generate_app_tracker_data(self):
        
        def pull_csv(csv_string):
            return pd.read_csv(csv_string).iloc[:,1:]

        def create_year_df(df,year):

            def add_date_columns(df, year):

                date_columns = ['visit_day', 'As of'] if year=='this' else ['Date','Created','Canceled Date']

                for column in date_columns:
                    df[column] = pd.to_datetime(df[column])

                df['Day'] = df[date_columns[0]].dt.day_name()

                for column in date_columns:
                    df[column] = df[column].dt.date

                return df

            def map_restaurants_to_app_values(df, year):
                
                if year == 'this':
                    restaurant_column = 'restaurant2'
                    restaurant_map = restaurant_mapping.tracker_data_to_app_map
                else:
                    restaurant_column = 'Venue'
                    restaurant_map = restaurant_mapping.sevenrooms_portal_to_app_map
                    
                df['Restaurant'] = df[restaurant_column].map(restaurant_map)
                return df

            return map_restaurants_to_app_values(add_date_columns(df,year),year)


        def create_tracker_df(df, week_date, as_of_date, year):

            def add_week_column(df, week_date, year):

                date_column = 'visit_day' if year=='this' else 'Date'

                def mon_next(date):
                    return date + timedelta(((7*1)+1)-date.isocalendar()[2])
                def mon_two(date):
                    return date + timedelta(((7*2)+1)-date.isocalendar()[2])
                def mon_three(date):
                    return date + timedelta(((7*3)+1)-date.isocalendar()[2])
                def mon_four(date):
                    return date + timedelta(((7*4)+1)-date.isocalendar()[2])
                def mon_five(date):
                    return date + timedelta(((7*5)+1)-date.isocalendar()[2])
                def mon_six(date):
                    return date + timedelta(((7*6)+1)-date.isocalendar()[2])
                def mon_seven(date):
                    return date + timedelta(((7*7)+1)-date.isocalendar()[2])
                def mon_eight(date):
                    return date + timedelta(((7*8)+1)-date.isocalendar()[2])
                def mon_nine(date):
                    return date + timedelta(((7*9)+1)-date.isocalendar()[2])

                def week_definer(as_of_date, res_date):
                    if res_date >= as_of_date and res_date < mon_next(as_of_date):
                        return 'This Week'
                    elif res_date >= mon_next(as_of_date) and res_date < mon_two(as_of_date):
                        return 'Next Week'
                    elif res_date >= mon_two(as_of_date) and res_date < mon_three(as_of_date):
                        return 'Two Weeks'
                    elif res_date >= mon_three(as_of_date) and res_date < mon_four(as_of_date):
                        return 'Three Weeks'
                    elif res_date >= mon_four(as_of_date) and res_date < mon_five(as_of_date):
                        return 'Four Weeks'
                    elif res_date >= mon_five(as_of_date) and res_date < mon_six(as_of_date):
                        return 'Five Weeks'
                    elif res_date >= mon_six(as_of_date) and res_date < mon_seven(as_of_date):
                        return 'Six Weeks'
                    elif res_date >= mon_seven(as_of_date) and res_date < mon_eight(as_of_date):
                        return 'Seven Weeks'
                    elif res_date >= mon_eight(as_of_date) and res_date < mon_nine(as_of_date):
                        return 'Eight Weeks'
                    else:
                        return ''

                df['Week'] = df[date_column].apply(lambda x: week_definer(week_date, x))
                return df

            def filter_by_status_and_date(df, as_of_date, year):

                if year == 'this':

                    as_of_today_mask = df['As of'] == as_of_date

                    df_columns = ['Restaurant', 'Week', 'Day', 'max_guests']
                    groupby_columns = df_columns[:-1]
                    df = df[as_of_today_mask][df_columns].groupby(groupby_columns).sum().reset_index()

                    df_columns = ['Restaurant', 'Week', 'Day','Covers']
                    df.columns = df_columns

                    return df

                else:

                    created_date_mask = df['Created'] < as_of_date
                    canceled_date_mask = df['Canceled Date'] >= as_of_date
                    completed_mask = df['Looker Status'] == 'Completed'
                    no_show_mask = df['Looker Status'] == 'No Show'
                    canceled_mask = df['Looker Status'] == 'Canceled'

                    return df[(created_date_mask & (completed_mask | no_show_mask)) | (created_date_mask & canceled_mask & canceled_date_mask)][['Restaurant', 'Week', 'Day','Covers']].groupby(['Restaurant', 'Week', 'Day']).sum().reset_index()

            return filter_by_status_and_date(add_week_column(df, week_date, year), as_of_date, year)



        def create_pickup_df(today_df, yesterday_df):

            def merge_today_and_yesterday(today_df, yesterday_df):

                return pd.merge(
                    left = today_df, 
                    right = yesterday_df,
                    how='outer',
                    on=['Restaurant','Week','Day']
                ).fillna(0)

            def rename_day_columns(df):

                df.columns = ['Restaurant','Week','Day','Today','Yesterday']
                return df

            def group_by_pickup_columns(df):

                df_columns = ['Restaurant','Week','Day','Today','Yesterday']
                groupby_columns = df_columns[:-2]
                return df[df_columns].groupby(groupby_columns).sum().reset_index()

            def calculate_pickup_column(df):

                df['Pickup'] = df['Today'] - df['Yesterday']
                return df

            def return_pickup_columns(df):

                return df[['Restaurant','Week','Day','Pickup']]

            return return_pickup_columns(
                calculate_pickup_column(
                    group_by_pickup_columns(
                        rename_day_columns(
                            merge_today_and_yesterday(
                                today_df,
                                yesterday_df
                            )
                        )
                    )
                )
            )

        def merge_tw_lw_ly(tw,lw,ly):

            def merge_tw_and_lw(tw,lw):

                return pd.merge(
                    left=tw,
                    right=lw,
                    how='outer',
                    on=['Restaurant','Week','Day'],
                    suffixes=('_TW', '_LW')
                ).fillna(0)

            def merge_ty_and_ly(ty, ly):

                return pd.merge(
                    left=ty,
                    right=ly,
                    how='outer',
                    on=['Restaurant','Week','Day']
                ).fillna(0)

            def filter_restaurants(df):

                bookings_restaurants = restaurant_mapping.app_restaurants
                return df[df['Restaurant'].isin(bookings_restaurants)]

            def filter_weeks(df):

                return df[df['Week'] != '']

            def rename_columns(df):

                df.columns = ['Restaurant','Week','Day','This Week','Last Week','Last Year']
                return df

            return rename_columns(
                filter_weeks(
                    filter_restaurants(
                        merge_ty_and_ly(
                            merge_tw_and_lw(
                                tw,
                                lw
                            ),ly
                        )
                    )
                )
            )

        def add_full_week_row(df):

            def group_by_restaurant_and_week(df):

                df_columns = ['Restaurant','Week','This Week','Last Week','Last Year']
                groupby_columns = df_columns[:-3]
                new_df = df[df_columns].groupby(groupby_columns).sum().reset_index().dropna()
                new_df['Day'] = 'Full Week'
                return new_df[['Restaurant','Week','Day','This Week','Last Week','Last Year']]

            def add_week_column(df):

                df['Day'] = 'Full Week'
                return df[['Restaurant','Week','Day','This Week','Last Week','Last Year']]

            week_df = group_by_restaurant_and_week(df)
            return pd.concat([week_df,df])

        def sort_columns(df):

            week_sorter = [
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

            day_sorter = [
                'Monday',
                'Tuesday',
                'Wednesday',
                'Thursday',
                'Friday',
                'Saturday',
                'Sunday',
                'Full Week'
            ]

            columns = ['Week','Day']
            sorters = [week_sorter, day_sorter]

            for i in range(2):
                df[columns[i]] = df[columns[i]].astype('category')
                df[columns[i]].cat.set_categories(sorters[i], inplace=True)

            return df.sort_values(['Restaurant','Week','Day'])

        def add_comparison_columns(df):

            df['vs. LW'] = df['This Week'] - df['Last Week']
            df['vs. LW %'] = (df['vs. LW'].replace(0,1) / df['Last Week'].replace(0,1))
            df['vs. LY'] = df['This Week'] - df['Last Year']
            df['vs. LY %'] = (df['vs. LY'].replace(0,1)  / df['Last Year'].replace(0,1))

            return df

        def create_final_df(tw,lw,ly):

            return add_comparison_columns(
                sort_columns(
                    add_full_week_row(
                        merge_tw_lw_ly(tw,lw,ly)
                    )
                )
            )


        today = date.today()
        todayLW = today - timedelta(7)
        todayLY = today - timedelta(364)
        yesterday = today - timedelta(1)
        yesterdayLW = todayLW - timedelta(1)
        yesterdayLY = todayLY - timedelta(1)
        daynum = today.isocalendar()[2]

        thisyear = self.historic_tracker_data.copy()
        lastyear_csv = 'SevenRooms Portal.csv'
        lastyear = pull_csv(lastyear_csv)

        this_year_df = create_year_df(thisyear, 'this')
        last_year_df = create_year_df(lastyear, 'last')

        tracker_tw_tday = create_tracker_df(this_year_df, today, today, 'this')
        tracker_tw_yday = create_tracker_df(this_year_df, today, yesterday, 'this')
        tracker_lw_tday = create_tracker_df(this_year_df, todayLW, todayLW, 'this')
        tracker_lw_yday = create_tracker_df(this_year_df, todayLW, yesterdayLW, 'this')
        tracker_ly_tday = create_tracker_df(last_year_df, todayLY, todayLY, 'last')
        tracker_ly_yday = create_tracker_df(last_year_df, todayLY, yesterdayLY, 'last')

        pickup_tw = create_pickup_df(tracker_tw_tday, tracker_tw_yday)
        pickup_lw = create_pickup_df(tracker_lw_tday, tracker_lw_yday)
        pickup_ly = create_pickup_df(tracker_ly_tday, tracker_ly_yday)

        tracker_df = create_final_df(
            tracker_tw_tday,
            tracker_lw_tday,
            tracker_ly_tday
        )

        pickup_df = create_final_df(
            pickup_tw,
            pickup_lw,
            pickup_ly
        )

        return tracker_df,pickup_df
        
    
    def generate_csvs(self):
        
        C_Drive_Database = self.C_Drive_Database
        N_Drive_Database = self.N_Drive_Database
        N_Drive_Forecasts = self.N_Drive_Forecasts

        def save_old_csv(current_csv_path, old_csv_path):

            now = datetime.now().strftime("%d-%b-%Y %H-%M")
            old_file = pd.read_csv(current_csv_path).iloc[:,1:]
            old_file.to_csv(old_csv_path + now + ".csv")

        def save_new_csv(df, current_csv_path):

            df.to_csv(current_csv_path)         

        def generate_sevenrooms_csv():
            
            df = self.sevenrooms_data
            
            if self.location == 'laptop':

                current_csv_path = "SevenRooms.csv"
                old_csv_path = "SevenRooms/SevenRooms "

                save_old_csv(current_csv_path, old_csv_path)
                save_new_csv(df, current_csv_path)
                
            else:

                current_csv_path = C_Drive_Database + "SevenRooms.csv"
                old_csv_path = C_Drive_Database + "SevenRooms/SevenRooms "

                save_old_csv(current_csv_path, old_csv_path)
                save_new_csv(df, current_csv_path)

                current_csv_path = N_Drive_Database + "SevenRooms.csv"
                old_csv_path = N_Drive_Database + "SevenRooms/SevenRooms "

                save_old_csv(current_csv_path, old_csv_path)
                save_new_csv(df, current_csv_path)

        def generate_tracker_data_csv():
            
            df = self.tracker_data

            if self.location == 'laptop':
                
                current_csv_path = "Tracker Data.csv"
                old_csv_path = "Tracker Data/Tracker Data "
                
            else:

                current_csv_path = N_Drive_Forecasts + "Tracker Data.csv"
                old_csv_path = N_Drive_Forecasts + "Tracker Data/Tracker Data "

            save_old_csv(current_csv_path, old_csv_path)
            save_new_csv(df, current_csv_path)

        def generate_historic_tracker_csv():
            
            df = self.historic_tracker_data
            
            if self.location == 'laptop':

                current_csv_path = "Historic_Tracker_Data.csv"
                save_new_csv(df, current_csv_path)
            
            else:
                
                current_csv_path = C_Drive_Database + "Historic_Tracker_Data.csv"
                save_new_csv(df, current_csv_path)

                current_csv_path = N_Drive_Database + "Historic_Tracker_Data.csv"
                save_new_csv(df, current_csv_path)

        def generate_shift_covers_csv():
            
            df = self.shift_covers_data
            
            if self.location == 'laptop':

                current_csv_path = "ShiftCovers.csv"
                old_csv_path = "ShiftCovers/ShiftCovers "
            
            else:
                
                current_csv_path = N_Drive_Forecasts + "Future Bookings/ShiftCovers.csv"
                old_csv_path = N_Drive_Forecasts + "Future Bookings/ShiftCovers/ShiftCovers "

            save_old_csv(current_csv_path, old_csv_path)
            save_new_csv(df, current_csv_path)

        def generate_future_bookings_csv():
            
            df = self.future_bookings_data
            current_csv_path = 'Future Bookings.csv'
            save_new_csv(df, current_csv_path)

        def generate_booking_trends_csv():
            
            df = self.booking_trends_data
            current_csv_path = 'Booking Trends.csv'
            save_new_csv(df, current_csv_path)

        def generate_app_tracker_csv():
            
            df = self.tracker_app_data
            current_csv_path = 'Tracker.csv'
            save_new_csv(df, current_csv_path)

        def generate_pickup_csv():
            
            df = self.pickup_data
            current_csv_path = 'Pickup.csv'
            save_new_csv(df, current_csv_path)
         
        generate_sevenrooms_csv()
        generate_tracker_data_csv()
        generate_historic_tracker_csv()
        generate_shift_covers_csv()
        generate_future_bookings_csv()
        generate_booking_trends_csv()
        generate_app_tracker_csv()
        generate_pickup_csv()
        
    def send_to_database(self):
        
        import psycopg2
        from sqlalchemy import create_engine
        from secrets import postgres_host, postgres_database, postgres_user, postgres_password
       
        host = postgres_host
        database = postgres_database
        user = postgres_user
        password = postgres_password
        
        tracker = self.tracker_app_data.copy()
        pickup = self.pickup_data.copy()
        future = self.future_bookings_data.copy()
        trends = self.booking_trends_data.copy()
        
        tracker_columns = {
            'Restaurant':'restaurant',
            'Week':'week',
            'Day':'day',
            'This Week':'this_week',
            'Last Week':'last_week',
            'Last Year':'last_year',
            'vs. LW':'vs_lw',
            'vs. LW %':'vs_lw_p',
            'vs. LY':'vs_ly',
            'vs. LY %':'vs_ly_p'
        }

        pickup_columns = {
            'Restaurant':'restaurant',
            'Week':'week',
            'Day':'day',
            'This Week':'this_week',
            'Last Week':'last_week',
            'Last Year':'last_year',
            'vs. LW':'vs_lw',
            'vs. LW %':'vs_lw_p',
            'vs. LY':'vs_ly',
            'vs. LY %':'vs_ly_p'
        }

        future_columns={
            'max_guests TW':'max_guests_tw',
            'max_guests LW':'max_guests_lw',
            'max_guests vs LW':'max_guests_vs_lw',
            'max_guests vs LW %':'max_guests_vs_lw_p',
            'full TW':'full_tw',
            'full LW':'full_lw'
        }

        trends_columns={
            'Restaurant':'restaurant',
            'As Of Day':'as_of_day',
            'Days Before Week Commencing':'days_before_week_commencing',
            'Reservation Week':'reservation_week',
            'Covers':'covers',
            'Table':'table',
            'Reservation Week':'reservation_week',
            'Covers':'covers',
            'Table':'table',
            'Week':'week',
            'Color':'color',
            'Alpha':'alpha'
        }

        tracker = tracker.rename(columns=tracker_columns)
        pickup = pickup.rename(columns=pickup_columns)
        future = future.rename(columns=future_columns)
        trends = trends.rename(columns=trends_columns)

        dfs = [tracker, pickup, future, trends]
        df_strings = ['tracker','pickup','future','booking_trends']
        
        engine_string = 'postgresql://' + user + ':' + password + '@' + host + '/' + database

        engine = create_engine(engine_string)
        con = engine.connect()

        for i in range(len(dfs)):
            dfs[i].to_sql(
                df_strings[i],
                con=con,
                index=False,
                if_exists='replace'
            )

        con.close()
      
