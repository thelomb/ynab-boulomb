from flask import (render_template,
                   request,
                   current_app)
from application import db
from application.reports import bp
from flask_login import current_user, login_required
from application.models import (Budget,
                                Account,
                                Transaction,
                                Category)
from datetime import date, datetime
from wtforms import TextField, SelectField
from application.ynab_api import Client as ynab


@bp.route('/')
def index():
    d = ynab(current_app.config['YNAB_API_KEY'])
    budget_id = '5694aece-d160-48f4-a041-42fad626098f'
    budget_id = None
    # accounts = object['budget']['accounts']
    budget = d.get_budget()

    budgetname = budget['budget']['name']
    accounts = budget['budget']['accounts']
    return render_template('index.html',
                           budget=budgetname,
                           object=accounts)
