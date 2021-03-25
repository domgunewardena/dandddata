sales_restaurants = [
    '100 Wardour Street',
    '14 Hills',
    '20 Stories', 
    'Aster', 
    'Avenue', 
    'Bluebird Chelsea', 
    'Blueprint Café', 
    'Butlers Wharf Chophouse', 
    'Cantina', 
    "Coq d'Argent", 
    'East 59th', 
    'Fiume', 
    'German Gymnasium', 
    'Issho',
    'Klosterhaus',
    'Launceston Place', 
    'Le Pont de la Tour', 
    'Madison', 
    'New Street Warehouse', 
    'Orrery', 
    'Paternoster Chophouse', 
    'Plateau', 
    'Quaglinos', 
    'Radici', 
    'Sartoria', 
    'Skylon', 
    'South Place Hotel', 
    'Trinity', 
    'White City',
    'The Modern Pantry',
]

bookings_restaurants = [
    '100 Wardour St',
    '14 Hills',
    '20 Stories',
    'Angelica',
    'Angler',
    'Aster',
    'Avenue',
    'Bluebird Chelsea',
    'Bluebird White City',
    'Butlers Wharf Chophouse',
    'Cantina del Ponte',
    "Coq d'Argent",
    'Crafthouse',
    'East 59th',
    'Fish Market',
    'Fiume',
    'German Gymnasium',
    'Issho',
    'Klosterhaus',
    'Launceston Place',
    'Madison',
    'New Street Grill',
    'Orrery',
    'Paternoster Chophouse',
    'Plateau',
    'Pont de la Tour',
    "Quaglino's",
    'Radici',
    'Sartoria',
    'Skylon',
    'South Place Chop House',
    'The Modern Pantry',
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
    'New Street Grill': 'New Street Grill',
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
    'dandd':{
        'sales' : sales_restaurants,
        'bookings' : bookings_restaurants,
    },
    'michaelf':{
        'sales':[
            '100 Wardour Street',
            'Avenue',
            'Bluebird Chelsea',
            'Madison', 
            'Quaglinos', 
            'Skylon', 
            'White City'
        ],
        'bookings':[
            '100 Wardour St',
            '14 Hills',
            'Avenue',
            'Bluebird Chelsea',
            'Bluebird White City',
            'Madison',
            "Quaglino's",
            'Skylon Restaurant'
        ],
    },
    'jb':{
        'sales':[
            '20 Stories', 
            'Aster', 
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
            'Angler',
            'Aster',
            "Coq d'Argent",
            'Crafthouse',
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
    'sharon':{
        'sales':[
            'Butlers Wharf Chophouse', 
            'Cantina', 
            'Fiume',
            'Launceston Place',
            'Le Pont de la Tour', 
            'Orrery', 
            'Radici',
            'Sartoria',
            'The Modern Pantry',
        ],
        'bookings':[
            'Butlers Wharf Chophouse',
            'Cantina del Ponte',
            'Fiume',
            'Launceston Place',
            'Orrery',
            'Pont de la Tour',
            'Radici',
            'Sartoria',
            'The Modern Pantry',
        ],
    },
}
        
            
    
            
            

sales_user_restaurants = {
    'dandd':[
        '100 Wardour Street', 
        '20 Stories', 
        'Aster', 
        'Avenue', 
        'Bluebird Chelsea', 
        'Blueprint Café', 
        'Butlers Wharf Chophouse', 
        'Cantina', 
        "Coq d'Argent", 
        'East 59th', 
        'Fiume', 
        'German Gymnasium', 
        'Issho', 
        'Launceston Place', 
        'Le Pont de la Tour', 
        'Madison', 
        'New Street Warehouse', 
        'Orrery', 
        'Paternoster Chophouse', 
        'Plateau', 
        'Quaglinos', 
        'Radici', 
        'Sartoria', 
        'Skylon', 
        'South Place Hotel', 
        'Trinity', 
        'White City'],
    'michaelf':[
        '100 Wardour Street',
        'Avenue',
        'Bluebird Chelsea',
        'Madison', 
        'Quaglinos', 
        'Skylon', 
        'White City'],
    'jb':[
        '20 Stories', 
        'Aster', 
        "Coq d'Argent", 
        'East 59th', 
        'German Gymnasium', 
        'Issho',
        'New Street Warehouse',
        'Paternoster Chophouse', 
        'Plateau', 
        'Trinity'],
    'sharon':[
        'Butlers Wharf Chophouse', 
        'Cantina', 
        'Fiume',
        'Launceston Place',
        'Le Pont de la Tour', 
        'Orrery', 
        'Radici',
        'Sartoria']
}

bookings_user_restaurants = {
    'dandd':[
        '100 Wardour St',
        '14 Hills',
        '20 Stories',
        'Angelica',
        'Angler Restaurant',
        'Aster',
        'Avenue',
        'Bluebird Chelsea Restaurant',
        'Bluebird White City',
        'Butlers Wharf Chophouse Restaurant',
        'Cantina del Ponte',
        "Coq d'Argent",
        'Crafthouse',
        'East 59th',
        'Fish Market',
        'Fiume',
        'German Gymnasium',
        'Issho Restaurant',
        'Klosterhaus',
        'Launceston Place',
        'Madison Restaurant',
        'New Street Grill',
        'Orrery',
        'Paternoster Chophouse',
        'Plateau',
        'Pont de la Tour',
        "Quaglino's Restaurant",
        'Radici',
        'Sartoria',
        'Skylon Restaurant',
        'South Place Chop House',
        'The Modern Pantry'
    ],
    'michaelf':[
        '100 Wardour St',
         '14 Hills',
         'Avenue',
         'Bluebird Chelsea Restaurant',
         'Bluebird White City',
         'Madison Restaurant',
         "Quaglino's Restaurant",
         'Skylon Restaurant'
    ],
    'sharon':[
         'Butlers Wharf Chophouse Restaurant',
         'Cantina del Ponte',
         'Fiume',
         'Launceston Place',
         'Orrery',
         'Pont de la Tour',
         'Radici',
         'Sartoria',
         'The Modern Pantry'
    ],
    'jb':[
        '20 Stories',
         'Angelica',
         'Angler Restaurant',
         'Aster',
         "Coq d'Argent",
         'Crafthouse',
         'East 59th',
         'Fish Market',
         'German Gymnasium',
         'Issho Restaurant',
         'Klosterhaus',
         'New Street Grill',
         'Orrery',
         'Paternoster Chophouse',
         'Plateau'
    ]
}
