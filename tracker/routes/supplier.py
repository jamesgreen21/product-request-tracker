from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from datetime import datetime
import os

from tracker.extensions import db
from tracker.models import Suppliers

supplier = Blueprint('supplier', __name__)

@supplier.route('/suppliers', methods=['GET', 'POST'])
def suppliers():
    suppliers = Suppliers.query.all()
    return render_template('suppliers.html', suppliers=suppliers)


@supplier.route('/suppliers/new', methods=['GET', 'POST'])
@login_required
def supplier_add():
    if request.method == 'POST':

        supplier = request.form.to_dict()

        supplier = Suppliers(**supplier)
        db.session.add(supplier)
        db.session.commit()

        flash('New Supplier added.', 'success')
        return redirect(url_for('supplier.suppliers'))

    return render_template('supplier_add.html')


@supplier.route('/suppliers/edit/<int:supplier_id>', methods=['GET', 'POST'])
@login_required
def supplier_edit(supplier_id):
    supplier = Suppliers.query.get_or_404(supplier_id)
    if request.method == 'POST':

        supplier.supplier_name = request.form['supplier_name']
        db.session.commit()

        flash('Supplier updated.', 'success')
        return redirect(url_for('supplier.suppliers'))

    return render_template('supplier_edit.html', supplier=supplier)


@supplier.route('/suppliers/<int:supplier_id>')
@login_required
def supplier_display(supplier_id):

    supplier = Suppliers.query.get_or_404(supplier_id)
    if supplier.display:
        supplier.display = False
    else:
        supplier.display = True

    db.session.commit()

    flash('Supplier updated.', 'success')
    return redirect(url_for('supplier.suppliers'))
