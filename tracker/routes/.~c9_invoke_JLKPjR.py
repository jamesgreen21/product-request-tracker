from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from datetime import datetime
import os
from werkzeug.utils import secure_filename

from tracker.extensions import db
from tracker.models import User, Posts, Suppliers, ProductType, Actions

action = Blueprint('action', __name__)
IMAGE_UPLOADS = '/home/ubuntu/environment/tracker/static/uploads/img'
ALLOWED_IMAGE_EXTENSIONS = ['PNG', 'JPG', 'JEPG']


def allowed_image(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in ALLOWED_IMAGE_EXTENSIONS:
        return True
    else:
        return False


@action.route("/action/add/<int:post_id>", methods=['GET', 'POST'])
@login_required
def action_add(post_id):
    post = Posts.query.get_or_404(post_id)
    if request.method == 'POST':

        new_action = request.form.to_dict()
        if request.files['image_file']:

            image_file = request.files['image_file']

            if image_file.filename == "":
                flash("Please ensure the image has a filename!")
                return redirect(url_for('action.action_add', post_id=post.id))

            if allowed_image(image_file.filename):
                filename = secure_filename(image_file.filename)
                image_file.save(os.path.join(IMAGE_UPLOADS, filename))
                new_action["image"] = "uploads/img/" + filename

            else:
                flash("That image extension is not allowed!")
                return redirect(url_for('action.action_add', post_id=post.id))

        new_action["created_by"] = current_user.id
        new_action["posts_id"] = post.id

        new_action = Actions(**new_action)
        db.session.add(new_action)
        db.session.commit()

        flash("New action has been added for {}.".format(post.title))
        return redirect(url_for('main.index'))

    return render_template('action_add.html', post=post)


@action.route("/action/edit/<int:post_id>", methods=['GET', 'POST'])
@login_required
def action_prompt(action_id):
    action = Actions.query.get_or_404(action_id)
    if request.method == 'POST':

        updated_action = request.form.to_dict()
        if request.files['image_file']:

            image_file = request.files['image_file']

            if image_file.filename == "":
                flash("Please ensure the image has a filename!")
                return redirect(url_for('action.edit_action_prompt', action_id=action.id))

            if allowed_image(image_file.filename):
                filename = secure_filename(image_file.filename)
                image_file.save(os.path.join(IMAGE_UPLOADS, filename))
                action["image"] = "uploads/img/" + filename

            else:
                flash("That image extension is not allowed!")
                return redirect(url_for('action.action_add', action_id=action.id))

        action = Actions(**action)
        db.session.add(action)
        db.session.commit()

        flash("New action has been added for {}.".format(action.action_post.title))
        return redirect(url_for('main.index'))

    return render_template('action_add.html', action=action)


@action.route('/action/outstanding')
@login_required
def action_outstanding():
    if current_user.user_type == 0:
        actions = \
            Actions.query.filter(Actions.approval
                == None).order_by(Actions.created_on.desc()).all()
    else:
        actions = \
            Actions.query.filter_by(stage=int(current_user.user_type)).filter(Actions.approval
                == None).order_by(Actions.created_on.desc()).all()
    if not actions:
        flash("There are no outstanding actions")

    return render_template('action_outstanding.html', actions=actions)


@action.route('/action/answer/<int:action_id>', methods=['GET', 'POST'])
@login_required
def action_answer(action_id):
    action = Actions.query.get_or_404(action_id)

    if request.method == 'POST':

        action.feedback = request.form["feedback"]
        action.approval = request.form["approval"]
        action.approved_by = current_user.id
        action.approved_on = datetime.utcnow()

        post = Posts.query.get_or_404(action.posts_id)
        if action.stage == 1:
            post.healthandsafety = action.approval
        elif action.stage == 2:
            post.quality = action.approval
        elif action.stage == 3:
            post.cagefill = action.approval
        elif action.stage == 4:
            post.restaurantimpact = action.approval
        
        db.session.commit()
        flash("Outstanding Action for {} complete.".format(action.action_post.title))
        return redirect(url_for('action.action_outstanding'))

    return render_template('action_answer.html', action=action)
