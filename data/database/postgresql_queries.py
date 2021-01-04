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
}

select = {
    'tracker':'SELECT * FROM tracker',
    'pickup':'SELECT * FROM pickup',
    'trends':'SELECT * FROM booking_trends',
    'future':'SELECT * FROM future',
    'revenue':'SELECT * FROM revenue',
    'covers':'SELECT * FROM covers'
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
    ]
}
