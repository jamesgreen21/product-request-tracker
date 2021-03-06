from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from datetime import datetime

from tracker.extensions import db
from tracker.models import User, Posts, Suppliers, Actions


main = Blueprint('main', __name__)


@main.route('/')
def index():
    """
    The Home page of the Application with all live Posts
    """
    posts = Posts.query.filter(Posts.complete == False).order_by(Posts.date_posted.desc()).all()
    context = {'posts': posts}
    if not posts:
        flash('There are no outstanding Requests!', 'information')

    return render_template('index.html', **context)


@main.route('/archives')
def archives():
    """
    Access the Archives containing archived Posts
    """
    posts = Posts.query.filter(Posts.complete
                               == True).order_by(Posts.date_posted.desc()).all()

    context = {'posts': posts}
    if not posts:
        flash('There are no archived Requests!', 'information')

    return render_template('archives.html', **context)


@main.route('/new', methods=['GET', 'POST'])
@login_required
def add_request():
    """
    Add a new request to the Posts table
    """
    if request.method == 'POST':

        new_request = request.form.to_dict()
        new_request['user_id'] = current_user.id
        product_type = request.form['product_type']
        new_request['product_type'] = \
            'media/img/{}.jpg'.format(product_type)

        # check new product checkbox
        try:
            new = new_request['new_product']
            new_request['new_product'] = (True if new == 'on'
                     else False)
        except:
            new_request['new_product'] = False

        # check existing case orientation checkbox
        try:
            new = new_request['ex_case_orientation']
            new_request['ex_case_orientation'] = (True if new == 'on'
                     else False)
        except:
            new_request['ex_case_orientation'] = False

        # check new case orientation checkbox
        try:
            new = new_request['case_orientation']
            new_request['case_orientation'] = (True if new == 'on'
                     else False)
        except:
            new_request['case_orientation'] = False

        new_request = Posts(**new_request)
        db.session.add(new_request)
        db.session.commit()

        flash('New request added!', 'success')
        return redirect(url_for('main.index'))

    suppliers = Suppliers.query.filter(Suppliers.display == True).all()

    context = {'suppliers': suppliers}
    return render_template('request_add.html', **context)


@main.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_request(post_id):
    """
    Edit an existing request in the Posts table
    """
    post = Posts.query.get_or_404(post_id)
    if request.method == 'POST':

        post.title = request.form['title']
        post.content = request.form['content']
        post.supplier_id = request.form['supplier_id']
        post.contact_name = request.form['contact_name']
        post.product_number = request.form['product_number']
        post.product_name = request.form['product_name']
        product_type = request.form['product_type']
        post.product_type = 'media/img/{}.jpg'.format(product_type)

        post.product_length = request.form['product_length']
        post.product_width = request.form['product_width']
        post.product_height = request.form['product_height']
        post.product_weight = request.form['product_weight']
        post.units_per_case = request.form['units_per_case']
        post.inners_per_case = request.form['inners_per_case']

        post.ex_product_length = request.form['ex_product_length']
        post.ex_product_width = request.form['ex_product_width']
        post.ex_product_height = request.form['ex_product_height']
        post.ex_product_weight = request.form['ex_product_weight']
        post.ex_units_per_case = request.form['ex_units_per_case']
        post.ex_inners_per_case = request.form['ex_inners_per_case']

        # New Product Check Box

        try:
            new = request.form['new_product']
            post.new_product = (True if new == 'on' else False)
        except:
            post.new_product = False

        # Existing Product Orientation

        try:
            ex_case_orientation = request.form['ex_case_orientation']
            post.ex_case_orientation = (True if ex_case_orientation
                    == 'on' else False)
        except:
            post.ex_case_orientation = False

        # New Product Orientation

        try:
            case_orientation = request.form['ex_case_orientation']
            post.case_orientation = (True if case_orientation == 'on'
                     else False)
        except:
            post.case_orientation = False

        db.session.commit()

        flash('The request has been editted.', 'success')
        return redirect(url_for('main.index'))

    suppliers = Suppliers.query.filter(Suppliers.display == True).all()

    context = {'suppliers': suppliers, 'post': post}
    return render_template('request_edit.html', **context)


@main.route('/outputform/<int:post_id>', methods=['GET', 'POST'])
def output_form(post_id):
    """
    Access to the Output Form page for a chose Post ID
    """
    post = Posts.query.get_or_404(post_id)
    health_and_safety = Actions.query.filter(Actions.stage == 1,
            Actions.posts_id
            == post_id).order_by(Actions.created_on.desc()).first()
    quality = Actions.query.filter(Actions.stage == 2, Actions.posts_id
                                   == post_id).order_by(Actions.created_on.desc()).first()
    cagefill = Actions.query.filter(Actions.stage == 3,
                                    Actions.posts_id
                                    == post_id).order_by(Actions.created_on.desc()).first()
    restaurant_impact = Actions.query.filter(Actions.stage == 4,
            Actions.posts_id
            == post_id).order_by(Actions.created_on.desc()).first()

    context = {
        'post': post,
        'health_and_safety': health_and_safety,
        'quality': quality,
        'cagefill': cagefill,
        'restaurant_impact': restaurant_impact,
        }

    return render_template('output_form.html', **context)


@main.route('/complete/<int:post_id>/<status>')
@login_required
def complete_request(post_id, status):
    """
    Mark a Post as complete to finish the NPI request
    """
    post = Posts.query.get_or_404(post_id)
    if post.healthandsafety in (0, 2):
        flash('Please complete Health and Safety for {}.'.format(post.title),
              'error')
        return redirect(url_for('main.index'))
    elif post.quality in (0, 2):
        flash('Please complete Quality for {}.'.format(post.title),
              'error')
        return redirect(url_for('main.index'))
    elif post.cagefill in (0, 2):
        flash('Please complete Cage Fill for {}.'.format(post.title),
              'error')
        return redirect(url_for('main.index'))
    elif post.restaurantimpact in (0, 2):
        flash('Please complete Restaurant Impact for {}.'.format(post.title),
              'error')
        return redirect(url_for('main.index'))

    post.status = status
    db.session.commit()

    flash('Request Status updated to {}'.format(post.status), 'success')
    return redirect(url_for('main.index'))


@main.route('/archive/<int:post_id>')
@login_required
def archive_request(post_id):
    """
    Archive a Post to move it into the Archive page of the App
    """
    post = Posts.query.get_or_404(post_id)
    if post.status == None:
        flash('Please ensure the Request is complete', 'error')
        return redirect(url_for('main.index'))

    post.complete = True
    db.session.commit()

    flash('Request {} has been moved to the Archives'.format(post.title),
          'success')
    return redirect(url_for('main.index'))


@main.route('/unarchive/<int:post_id>')
@login_required
def unarchive_request(post_id):
    """
    Move an archived Post back into the live tracker (Home page)
    """
    post = Posts.query.get_or_404(post_id)
    post.complete = False
    db.session.commit()

    flash('Request {} has been moved back to the Tracker'.format(post.title),
          'success')
    return redirect(url_for('main.archives'))
