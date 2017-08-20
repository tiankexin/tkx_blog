from flask import render_template
from . import main
from app.utils.permission import permission_required, admin_required
from app.common.constant import Permission
from app.models.user import User, UserProfile
from flask import abort


@main.route('/admin')
@admin_required
def for_admins_only():
    return "For Admins"


@main.route('/everyone')
@permission_required(Permission.READ_ARTICLES)
def for_everyone():
    return "Welcome Everyone!"


@main.route('/test1')
def test1():
    return render_template('test/test1.html')


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/user/<user_id>')
def show_user_info(user_id):
    user = User.query_one(User.id == user_id)
    if user is None:
        abort(404)
    profile = UserProfile.query_one(UserProfile.user_id == user_id)
    return render_template('user/info.html', user=user, profile=profile)


