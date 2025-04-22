from flask import Blueprint, render_template, redirect, url_for, request
from models import db, Route
from forms import RouteForm

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/routes')
def list_routes():
    routes = Route.query.all()
    return render_template('admin/routes.html', routes=routes)

@admin_bp.route('/routes/add', methods=['GET', 'POST'])
def add_route():
    form = RouteForm()
    if form.validate_on_submit():
        new_route = Route(name=form.name.data, description=form.description.data)
        db.session.add(new_route)
        db.session.commit()
        return redirect(url_for('admin.list_routes'))
    return render_template('admin/add_route.html', form=form)

@admin_bp.route('/routes/edit/<int:id>', methods=['GET', 'POST'])
def edit_route(id):
    route = Route.query.get_or_404(id)
    form = RouteForm(obj=route)
    if form.validate_on_submit():
        route.name = form.name.data
        route.description = form.description.data
        db.session.commit()
        return redirect(url_for('admin.list_routes'))
    return render_template('admin/edit_route.html', form=form, route=route)

@admin_bp.route('/routes/delete/<int:id>', methods=['POST'])
def delete_route(id):
    route = Route.query.get_or_404(id)
    db.session.delete(route)
    db.session.commit()
    return redirect(url_for('admin.list_routes'))
