create = {
    'tracker':"""
        CREATE TABLE tracker (
            index INTEGER PRIMARY KEY,
            restaurant VARCHAR(50),
            week VARCHAR(15),
            day VARCHAR(10),
            this_week INTEGER,
            last_week INTEGER,
            last_year INTEGER,
            vs_lw INTEGER,
            vw_lw_p DECIMAL,
            vs_ly INTEGER,
            vs_ly_p DECIMAL
        );
        """,
    'pickup':"""
        CREATE TABLE pickup (
            index INTEGER PRIMARY KEY,
            restaurant VARCHAR(50),
            week VARCHAR(15),
            day VARCHAR(10),
            this_week INTEGER,
            last_week INTEGER,
            last_year INTEGER,
            vs_lw INTEGER,
            vw_lw_p DECIMAL,
            vs_ly INTEGER,
            vs_ly_p DECIMAL
        );
        """,
    'trends':"""
        CREATE TABLE booking_trends (
            index INTEGER PRIMARY KEY,
            restaurant VARCHAR(50),
            as_of_day VARCHAR(10),
            days_before_week_commencing INTEGER,
            reservation_week INTEGER,
            covers INTEGER,
            table_name VARCHAR(20),
            week VARCHAR(15),
            color VARCHAR(10),
            alpha NUMERIC(2,1)
        );
        """,
    'future':"""
        CREATE TABLE future_bookings (
            index INTEGER PRIMARY KEY,
            visit_day VARCHAR(10),
            restaurant VARCHAR(50),
            shift VARCHAR(10),
            max_guests_tw INTEGER,
            capacity INTEGER,
            full_tw DECIMAL,
            max_guests_lw INTEGER,
            full_lw DECIMAL,
            max_guests_vs_lw INTEGER,
            max_guests_vs_lw_p INTEGER
        );
        """,
    'revenue':"""
        CREATE TABLE revenue (
            index INTEGER PRIMARY KEY,
            site_name VARCHAR(40),
            location_name VARCHAR(30),
            generic_location VARCHAR(20),
            session VARCHAR(10),
            ord_session INTEGER,
            revenue_type VARCHAR(15),
            wine VARCHAR(10),
            date VARCHAR(10),
            day VARCHAR(10),
            ord_day VARCHAR(15),
            revenue DECIMAL
        );
    """,
    'covers':"""
        CREATE TABLE covers (
            index INTEGER PRIMARY KEY,
            site_name VARCHAR(40),
            location_name VARCHAR(30),
            generic_location VARCHAR(20),
            session VARCHAR(10),
            ord_session INTEGER,
            date VARCHAR(10),
            day VARCHAR(10),
            ord_day VARCHAR(15),
            covers INTEGER
        );
    """,
    'reviews':"""
        CREATE TABLE reviews (
            source VARCHAR(11),
            restaurant VARCHAR(25),
            title VARCHAR(150),
            date VARCHAR(10),
            score INTEGER,
            food INTEGER,
            service INTEGER,
            value INTEGER,
            ambience INTEGER,
            review TEXT,
            link TEXT
        );
    """
}

select = {
    'tracker':'SELECT * FROM tracker',
    'pickup':'SELECT * FROM pickup',
    'trends':'SELECT * FROM booking_trends',
    'future':'SELECT * FROM future',
    'revenue':'SELECT * FROM revenue',
    'covers':'SELECT * FROM covers',
    'reviews':'SELECT * FROM reviews'
}

column_names = {
    'tracker':[
        'Restaurant',
        'Week',
        'Day',
        'This Week',
        'Last Week',
        'Last Year',
        'vs. LW',
        'vs. LW %',
        'vs. LY',
        'vs. LY %',
    ],
    'pickup':[
        'Restaurant',
        'Week',
        'Day',
        'This Week',
        'Last Week',
        'Last Year',
        'vs. LW',
        'vs. LW %',
        'vs. LY',
        'vs. LY %',
    ],
    'future':[
        'visit_day',
        'restaurant',
        'shift',
        'max_guests TW',
        'capacity',
        'full TW',
        'max_guests LW',
        'full LW',
        'max_guests vs LW',
        'max_guests vs LW %',
    ],
    'trends':[
        'Restaurant',
        'As Of Day',
        'Days Before Week Commencing',
        'Reservation Week',
        'Covers',
        'Table',
        'Week',
        'Color',
        'Alpha'
    ],
    'revenue':[
        'SiteName',
        'LocationName',
        'GenericLocation',
        'Session',
        'OrdSession',
        'RevenueType',
        'Wine',
        'Date',
        'Day',
        'OrdDay',
        'Revenue'
    ],
    'covers':[
        'SiteName',
        'LocationName',
        'GenericLocation',
        'Session',
        'Date',
        'Day',
        'OrdDay',
        'Covers',
    ],
    'reviews': [
        'source',
        'restaurant',
        'title',
        'date',
        'visit_date',
        'score',
        'food',
        'service',
        'value',
        'ambience',
        'review',
        'link',
    ]
}

column_renaming_map = {
    'tracker':{
        'restaurant':'Restaurant',
        'week':'Week',
        'day':'Day',
        'this_week':'This Week',
        'last_week':'Last Week',
        'last_year':'Last Year',
        'vs_lw':'vs. LW',
        'vs_lw_p':'vs. LW %',
        'vs_ly':'vs. LY',
        'vs_ly_p':'vs. LY %',
    },
    'pickup':{
        'restaurant':'Restaurant',
        'week':'Week',
        'day':'Day',
        'this_week':'This Week',
        'last_week':'Last Week',
        'last_year':'Last Year',
        'vs_lw':'vs. LW',
        'vs_lw_p':'vs. LW %',
        'vs_ly':'vs. LY',
        'vs_ly_p':'vs. LY %',
    },
    'future':{
        'max_guests_tw':'max_guests TW',
        'full_tw':'full TW',
        'max_guests_lw':'max_guests LW',
        'full_lw':'full LW',
        'max_guests_vs_lw':'max_guests vs LW',
        'max_guests_vs_lw_p':'max_guests vs LW %',
    },
    'trends':{
        'restaurant':'Restaurant',
        'as_of_day':'As Of Day',
        'days_before_week_commencing':'Days Before Week Commencing',
        'reservation_week':'Reservation Week',
        'covers':'Covers',
        'table':'Table',
        'week':'Week',
        'color':'Color',
        'alpha':'Alpha'
    },
    'revenue':{
        'site_name':'SiteName',
        'location_name':'LocationName',
        'generic_location':'GenericLocation',
        'session':'Session',
        'ord_session':'OrdSession',
        'revenue_type':'RevenueType',
        'wine':'Wine',
        'date':'Date',
        'day':'Day',
        'ord_day':'OrdDay',
        'revenue':'Revenue',
    },
    'covers':{
        'site_name':'SiteName',
        'location_name':'LocationName',
        'generic_location':'GenericLocation',
        'session':'Session',
        'date':'Date',
        'day':'Day',
        'ord_day':'OrdDay',
        'covers':'Covers',
    },
    ,
    'reviews': {
        'source': 'source',
        'restaurant': 'restaurant',
        'title': 'title',
        'date': 'date',
        'visit_date': 'visit_date',
        'score': 'score',
        'food': 'food',
        'service': 'service',
        'value': 'value',
        'ambience': 'ambience',
        'review': 'review',
        'link': 'link'
    }
}