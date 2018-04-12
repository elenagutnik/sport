from flask import Blueprint

raceinfo = Blueprint('raceinfo', __name__)

from . import views
from . import results
from ..models import *
from . import events
from . import testdata
from . import competitors
from . import jsonencoder


