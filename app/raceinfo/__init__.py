from flask import Blueprint

raceinfo = Blueprint('raceinfo', __name__)

from . import views
from ..models import *
