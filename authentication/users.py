def first_restaurant(restaurant_list, restaurant_string):
    l = restaurant_list.copy()
    l.insert(0, restaurant_list.pop(restaurant_list.index(restaurant_string)))
    return l
    

sales_restaurants = [
#     '100 Wardour Street',
#     '14 Hills',
    '20 Stories', 
#     'Aster', 
#     'Avenue', 
    'Bluebird Chelsea', 
#     'Blueprint Café', 
    'Butlers Wharf Chophouse', 
    'Cantina', 
    "Coq d'Argent", 
    'East 59th', 
    'Fiume', 
    'German Gymnasium', 
    'Issho',
    'Klosterhaus',
#     'Launceston Place', 
    'Le Pont de la Tour', 
    'Madison', 
    'New Street Warehouse', 
    'Orrery', 
    'Paternoster Chophouse', 
    'Plateau', 
#     'Quaglinos', 
    'Radici', 
#     'Sartoria', 
    'Skylon', 
#     'South Place Hotel', 
    'Trinity', 
    'White City',
#     'The Modern Pantry',
]

bookings_restaurants = [
#     '100 Wardour St',
#     '14 Hills',
    '20 Stories',
    'Angelica',
#     'Angler',
#     'Aster',
#     'Avenue',
    'Bluebird Chelsea',
    'Bluebird White City',
    'Butlers Wharf Chophouse',
    'Cantina del Ponte',
    "Coq d'Argent",
#     'Crafthouse',
    'East 59th',
    'Fish Market',
    'Fiume',
    'German Gymnasium',
    'Issho',
    'Klosterhaus',
#     'Launceston Place',
    'Madison',
    'New Street Grill',
    'Orrery',
    'Paternoster Chophouse',
    'Plateau',
    'Pont de la Tour',
#     "Quaglino's",
    'Radici',
#     'Sartoria',
    'Skylon',
#     'South Place Chop House',
#     'The Modern Pantry',
]

sales_to_bookings_restaurants_dict = {
    '100 Wardour Street': '100 Wardour St',
    '14 Hills': '14 Hills',
    '20 Stories': '20 Stories',
    'Aster': 'Aster',
    'Avenue': 'Avenue',
    'Bluebird Chelsea': 'Bluebird Chelsea Restaurant',
    'Blueprint Café': 'Blueprint Café',
    'Butlers Wharf Chophouse': 'Butlers Wharf Chophouse Restaurant',
    'Cantina': 'Cantina del Ponte',
    "Coq d'Argent": "Coq d'Argent",
    'East 59th': 'East 59th',
    'Fiume': 'Fiume',
    'German Gymnasium': 'German Gymnasium',
    'Issho': 'Issho Restaurant',
    'Klosterhaus': 'Klosterhaus',
    'Launceston Place': 'Launceston Place',
    'Le Pont de la Tour': 'Pont de la Tour',
    'Madison': 'Madison Restaurant',
    'New Street Warehouse': ['New Street Grill', 'Fish Market'],
    'Orrery': 'Orrery',
    'Paternoster Chophouse': 'Paternoster Chophouse',
    'Plateau': 'Plateau',
    'Quaglinos': "Quaglino's Restaurant",
    'Radici': 'Radici',
    'Sartoria': 'Sartoria',
    'Skylon': 'Skylon',
    'South Place Hotel': ['South Place Chop House','Angler Restaurant'],
    'Trinity': ['Angelica','Crafthouse'],
    'White City': 'Bluebird White City',
    'The Modern Pantry':'The Modern Pantry',
}

bookings_to_sales_restaurants_dict = {
    '100 Wardour St': '100 Wardour Street',
    '14 Hills': '14 Hills',
    '20 Stories': '20 Stories',
    'Angelica': 'Angelica',
    'Angler': 'South Place Hotel',
    'Aster': 'Aster',
    'Avenue': 'Avenue',
    'Bluebird Chelsea': 'Bluebird Chelsea',
    'Bluebird White City': 'White City',
    'Butlers Wharf Chophouse': 'Butlers Wharf Chophouse',
    'Cantina del Ponte': 'Cantina',
    "Coq d'Argent": "Coq d'Argent",
    'Crafthouse': 'Trinity',
    'East 59th': 'East 59th',
    'Fish Market': 'New Street Warehouse',
    'Fiume': 'Fiume',
    'German Gymnasium': 'German Gymnasium',
    'Issho': 'Issho',
    'Klosterhaus': 'Klosterhaus',
    'Launceston Place': 'Launceston Place',
    'Madison': 'Madison',
    'New Street Grill': 'New Street Warehouse',
    'Orrery': 'Orrery',
    'Paternoster Chophouse': 'Paternoster Chophouse',
    'Plateau': 'Plateau',
    'Pont de la Tour': 'Le Pont de la Tour',
    "Quaglino's": "Quaglinos",
    'Radici': 'Radici',
    'Sartoria': 'Sartoria',
    'Skylon': 'Skylon',
    'South Place Chop House': 'South Place Hotel',
    'The Modern Pantry': 'The Modern Pantry'
}

user_restaurants = {
    'des@danddlondon.com':{
        'sales' : sales_restaurants,
        'bookings' : bookings_restaurants,
    },
    'davidloewi@danddlondon.com':{
        'sales' : sales_restaurants,
        'bookings' : bookings_restaurants,
    },
    'annabels@danddlondon.com':{
        'sales' : sales_restaurants,
        'bookings' : bookings_restaurants,
    },
    'marki@danddlondon.com':{
        'sales' : sales_restaurants,
        'bookings' : bookings_restaurants,
    },
    'lisaf@danddlondon.com':{
        'sales' : sales_restaurants,
        'bookings' : bookings_restaurants,
    },
    'benc@danddlondon.com':{
        'sales' : sales_restaurants,
        'bookings' : bookings_restaurants,
    },
    'jaspreetr@danddlondon.com':{
        'sales' : sales_restaurants,
        'bookings' : bookings_restaurants,
    },
    'carolc@danddlondon.com':{
        'sales' : sales_restaurants,
        'bookings' : bookings_restaurants,
    },
    'michaelf@danddlondon.com':{
        'sales':[
#             '100 Wardour Street',
#             '14 Hills',
#             'Avenue',
            'Bluebird Chelsea',
            'Madison', 
#             'Quaglinos', 
            'Skylon', 
            'White City'
        ],
        'bookings':[
#             '100 Wardour St',
#             '14 Hills',
#             'Avenue',
            'Bluebird Chelsea',
            'Bluebird White City',
            'Madison',
#             "Quaglino's",
            'Skylon'
        ],
    },
    'jb@danddlondon.com':{
        'sales':[
            '20 Stories', 
#             'Aster', 
            "Coq d'Argent", 
            'East 59th', 
            'German Gymnasium', 
            'Issho',
            'New Street Warehouse',
            'Paternoster Chophouse', 
            'Plateau', 
            'Trinity'
        ],
        'bookings':[
            '20 Stories',
            'Angelica',
#             'Aster',
            "Coq d'Argent",
#             'Crafthouse',
            'East 59th',
            'Fish Market',
            'German Gymnasium',
            'Issho',
            'Klosterhaus',
            'New Street Grill',
            'Orrery',
            'Paternoster Chophouse',
            'Plateau'
        ],
    },
    'sharonw@danddlondon.com':{
        'sales':[
            'Butlers Wharf Chophouse', 
            'Cantina', 
            'Fiume',
#             'Launceston Place',
            'Le Pont de la Tour', 
            'Orrery', 
            'Radici',
#             'Sartoria',
#             'The Modern Pantry',
        ],
        'bookings':[
            'Butlers Wharf Chophouse',
            'Cantina del Ponte',
            'Fiume',
#             'Launceston Place',
            'Orrery',
            'Pont de la Tour',
            'Radici',
#             'Sartoria',
#             'The Modern Pantry',
        ],
    },
    'kimst@danddlondon.com':{
#         'sales':first_restaurant(sales_restaurants,'100 Wardour Street'),
#         'bookings':first_restaurant(bookings_restaurants,'100 Wardour St'),
        'sales':sales_restaurants,
        'bookings':bookings_restaurants
    },
    'massimilianod@danddlondon.com':{
#         'sales':first_restaurant(sales_restaurants,'14 Hills'),
#         'bookings':first_restaurant(bookings_restaurants,'14 Hills'),
        'sales':sales_restaurants,
        'bookings':bookings_restaurants
    },
    'philipu@danddlondon.com':{
        'sales':first_restaurant(sales_restaurants,'20 Stories'),
        'bookings':first_restaurant(bookings_restaurants,'20 Stories'),
    },
    'radk@danddlondon.com':{
#         'sales':first_restaurant(sales_restaurants,'Aster'),
#         'bookings':first_restaurant(bookings_restaurants,'Aster'),
        'sales':sales_restaurants,
        'bookings':bookings_restaurants
    },
    'joseu@danddlondon.com':{
#         'sales':first_restaurant(sales_restaurants,'Avenue'),
#         'bookings':first_restaurant(bookings_restaurants,'Avenue'),
        'sales':sales_restaurants,
        'bookings':bookings_restaurants
    },
    'matthewm@danddlondon.com':{
        'sales':first_restaurant(sales_restaurants,'Bluebird Chelsea'),
        'bookings':first_restaurant(bookings_restaurants,'Bluebird Chelsea'),
    },
    'mattheol@danddlondon.com':{
        'sales':first_restaurant(sales_restaurants,'White City'),
        'bookings':first_restaurant(bookings_restaurants,'Bluebird White City'),
    },
    'imantsz@danddlondon.com':{
        'sales':first_restaurant(sales_restaurants,'Butlers Wharf Chophouse'),
        'bookings':first_restaurant(bookings_restaurants,'Butlers Wharf Chophouse'),
    },
    'ornetsf@danddlondon.com':{
        'sales':first_restaurant(sales_restaurants,'Cantina'),
        'bookings':first_restaurant(bookings_restaurants,'Cantina del Ponte'),
    },
    'seang@danddlondon.com':{
        'sales':first_restaurant(sales_restaurants,"Coq d'Argent"),
        'bookings':first_restaurant(bookings_restaurants,"Coq d'Argent"),
    },
    'jonathanpf@danddlondon.com':{
        'sales':first_restaurant(sales_restaurants,'East 59th'),
        'bookings':first_restaurant(bookings_restaurants,'East 59th'),
    },
    'micharb@danddlondon.com':{
        'sales':first_restaurant(sales_restaurants,'Fiume'),
        'bookings':first_restaurant(bookings_restaurants,'Fiume'),
    },
    'samb@danddlondon.com':{
        'sales':first_restaurant(sales_restaurants,'German Gymnasium'),
        'bookings':first_restaurant(bookings_restaurants,'German Gymnasium'),
    },
    'williamg@danddlondon.com':{
        'sales':first_restaurant(sales_restaurants,'Issho'),
        'bookings':first_restaurant(bookings_restaurants,'Issho'),
    },
    'tiagop@danddlondon.com':{
        'sales':first_restaurant(sales_restaurants,'Klosterhaus'),
        'bookings':first_restaurant(bookings_restaurants,'Klosterhaus'),
    },
    'carlos@danddlondon.com':{
#         'sales':first_restaurant(sales_restaurants,'Launceston Place'),
#         'bookings':first_restaurant(bookings_restaurants,'Launceston Place'),
        'sales':sales_restaurants,
        'bookings':bookings_restaurants
    },
    'medr@danddlondon.com':{
        'sales':first_restaurant(sales_restaurants,'Madison'),
        'bookings':first_restaurant(bookings_restaurants,'Madison'),
    },
    'fadiln@danddlondon.com':{
        'sales':first_restaurant(sales_restaurants,'Orrery'),
        'bookings':first_restaurant(bookings_restaurants,'Orrery'),
    },
    'hannahn@danddlondon.com':{
        'sales':first_restaurant(sales_restaurants,'Paternoster Chophouse'),
        'bookings':first_restaurant(bookings_restaurants,'Paternoster Chophouse'),
    },
    'alfonsoc@danddlondon.com':{
        'sales':first_restaurant(sales_restaurants,'Plateau'),
        'bookings':first_restaurant(bookings_restaurants,'Plateau'),
    },
    'olgag@danddlondon.com':{
        'sales':first_restaurant(sales_restaurants,'Le Pont de la Tour'),
        'bookings':first_restaurant(bookings_restaurants,'Pont de la Tour'),
    },
    'vidmantasg@danddlondon.com':{
#         'sales':first_restaurant(sales_restaurants,"Quaglino's"),
#         'bookings':first_restaurant(bookings_restaurants,"Quaglino's"),
        'sales':sales_restaurants,
        'bookings':bookings_restaurants
    },
    'vitoc@danddlondon.com':{
        'sales':first_restaurant(sales_restaurants,'Radici'),
        'bookings':first_restaurant(bookings_restaurants,'Radici'),
    },
    'encirobf@danddlondon.com':{
#         'sales':first_restaurant(sales_restaurants,'Sartoria'),
#         'bookings':first_restaurant(bookings_restaurants,'Sartoria'),
        'sales':sales_restaurants,
        'bookings':bookings_restaurants
    },
    'dainiusk@danddlondon.com':{
        'sales':first_restaurant(sales_restaurants,'Skylon'),
        'bookings':first_restaurant(bookings_restaurants,'Skylon'),
    },
    'nono@danddlondon.com':{
#         'sales':first_restaurant(sales_restaurants,'South Place Chop House'),
#         'bookings':first_restaurant(bookings_restaurants,'South Place Hotel'),
        'sales':sales_restaurants,
        'bookings':bookings_restaurants
    },
    'annap@danddlondon.com':{
#         'sales':first_restaurant(sales_restaurants,'The Modern Pantry'),
#         'bookings':first_restaurant(bookings_restaurants,'The Modern Pantry'),
        'sales':sales_restaurants,
        'bookings':bookings_restaurants
    },
}
