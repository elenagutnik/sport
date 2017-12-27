from flask import Blueprint

raceinfo = Blueprint('raceinfo', __name__)

from . import views
from ..models import *
from . import events
from . import testdata
from . import jsonencoder

