from flask import Blueprint

shorttrack = Blueprint('shorttrack', __name__)

from .. import db_shorttrack as db
from . import views
from . import models
from . import RunList
from . import events
from . import Race
from . import deviceDataHandler