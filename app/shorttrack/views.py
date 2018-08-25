from flask import render_template, redirect, request, url_for, flash
from flask_login import login_required, current_user
from . import shorttrack
from ..decorators import admin_required
from flask_babel import gettext
import json
from .models import *


@shorttrack.route('/', methods=['GET', 'POST'])
@login_required
@admin_required
def index():
    return render_template('shorttrack/index.html')