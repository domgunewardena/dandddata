import dash_auth
from app import app

VALID_USERNAME_PASSWORD_PAIRS = {
    'dandd':'london123',
    'michaelf':'london123',
    'sharon':'london123',
    'jb':'london123'
}

auth = dash_auth.BasicAuth(app,VALID_USERNAME_PASSWORD_PAIRS)
