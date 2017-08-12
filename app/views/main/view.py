from flask import render_template
from . import main
from app.utils.permission import permission_required, admin_required
from app.common.constant import Permission


@main.route('/admin')
@admin_required
def for_admins_only():
    return "For Admins"


@main.route('/everyone')
@permission_required(Permission.READ_ARTICLES)
def for_everyone():
    return "Welcome Everyone!"


@main.route('/')
def index():
    return render_template('index.html')

