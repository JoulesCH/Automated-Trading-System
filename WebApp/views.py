# Local imports
from core import app
from resources import Base

app.route('/')(Base.home)