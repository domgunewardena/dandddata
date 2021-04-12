from authentication import dash_auth
from app import app

from authentication.users import user_restaurants
import os

app_password = os.environ['GENERAL_PASSWORD']

password_pairs = {user:app_password for user in user_restaurants.keys()}

auth = dash_auth.BasicAuth(app,password_pairs)
