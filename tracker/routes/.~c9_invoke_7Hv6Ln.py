from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required

from tracker.extensions import db
from tracker.models import User, Posts, Suppliers, ProductType, Actions

main = Blueprint('main', __name__)

@main.route('/')
def index():
    posts = Posts.query.order_by(Posts.date_posted).all()

    context = {
        'posts': posts,
    }
    return render_template('index.html', **context)


@main.route('/new', methods=['GET', 'POST'])
@login_required
def add_request():
    if request.method == 'POST':

        new_request = request.form.to_dict()
        new_request["user_id"] = current_user.id

        new_request = Posts(**new_request)
        db.session.add(new_request)
        db.session.commit()

        flash('New request added!')
        return redirect(url_for('main.index'))

    types = ProductType.query.all()
    suppliers = Suppliers.query.all()

    context = {
        'suppliers': suppliers,
        'types': types
    }
    return render_template('new_request.html', **context)


@main.route("/action_prompt/<int:post_id>/action", methods=['GET', 'POST'])
@login_required
def action_prompt(post_id):
    post = Posts.query.get_or_404(post_id)
    if request.method == 'POST':

        new_action = request.form.to_dict()
        new_action["user_id"] = current_user.id
        new_action["posts_id"] = post.id

        new_action = Actions(**new_action)
        db.session.add(new_action)
        db.session.commit()

        flash("New action has been added for {}.".format(post.title))
        return redirect(url_for('main.index'))

    return render_template('action_prompt.html', post=post)


@main.route('/action_outstanding')
def action_outstanding():
    actions = Actions.query.filter_by(stage=int(current_user.user_type)).filter(Actions.approval == 2).all()
    return render_template('action_outstanding.html', actions=actions)


@main.route('/action/<int:action_id>')
def answer_action(action_id):
    actions = Actions.query.get_or_404(action_id)
    return render_template('answer_action.html', actions=actions)


@main.route('/users')
def users():
    return render_template('users.html')
