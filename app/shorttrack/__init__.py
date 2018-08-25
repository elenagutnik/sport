from flask import Blueprint

shorttrack = Blueprint('shorttrack', __name__)

from .. import db
from . import views
from . import models
