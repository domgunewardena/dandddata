from authentication import dash_auth
from app import app

import os
app_password = os.environ['GENERAL_PASSWORD']

password_pairs = {
  'dandd':app_password,
  'michaelf':app_password,
  'sharon':app_password,
  'jb':app_password,
}

auth = dash_auth.BasicAuth(app,password_pairs)
