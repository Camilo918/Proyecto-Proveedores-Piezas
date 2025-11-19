from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from . import models

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return redirect(url_for('main.list_providers'))



@bp.route('/providers')
def list_providers():
    providers = models.get_all_providers()
    return render_template('providers.html', providers=providers)


@bp.route('/providers/new', methods=['GET', 'POST'])
def new_provider():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form.get('address')
        city = request.form.get('city')
        province = request.form.get('province')

        models.create_provider(name, address, city, province)
        flash("Proveedor creado.")
        return redirect(url_for('main.list_providers'))

    return render_template('provider_form.html', provider=None)


@bp.route('/providers/<int:pid>/edit', methods=['GET', 'POST'])
def edit_provider(pid):
    provider = models.get_provider(pid)
    if not provider:
        abort(404)

    if request.method == 'POST':
        name = request.form['name']
        address = request.form.get('address')
        city = request.form.get('city')
        province = request.form.get('province')

        models.update_provider(pid, name, address, city, province)
        flash("Proveedor actualizado.")
        return redirect(url_for('main.list_providers'))

    return render_template('provider_form.html', provider=provider)


@bp.route('/providers/<int:pid>/delete', methods=['POST'])
def delete_provider(pid):
    provider = models.get_provider(pid)
    if not provider:
        abort(404)

    models.delete_provider(pid)
    flash("Proveedor eliminado.")
    return redirect(url_for('main.list_providers'))



@bp.route('/providers/<int:pid>', methods=['GET', 'POST'])
def provider_detail(pid):
    provider = models.get_provider(pid)
    if not provider:
        abort(404)

    pieces = models.get_all_pieces()

    if request.method == 'POST':
        piece_id = int(request.form['piece_id'])
        price = float(request.form.get('price') or 0)
        quantity = int(request.form.get('quantity') or 0)
        color = request.form.get('color')
        category = request.form.get('category')

        models.upsert_supply(pid, piece_id, price, quantity, color, category)
        flash("Pieza asociada/actualizada.")
        return redirect(url_for('main.provider_detail', pid=pid))

    supplies = models.get_supplies_by_provider(pid)
    return render_template('provider_detail.html', provider=provider, pieces=pieces, supplies=supplies)



@bp.route('/pieces')
def list_pieces():
    pieces = models.get_all_pieces()
    return render_template('pieces.html', pieces=pieces)


@bp.route('/pieces/new', methods=['GET', 'POST'])
def new_piece():
    if request.method == 'POST':
        name = request.form['name']
        models.create_piece(name)
        flash("Pieza creada.")
        return redirect(url_for('main.list_pieces'))

    return render_template('piece_form.html', piece=None)


@bp.route('/pieces/<int:pid>/edit', methods=['GET', 'POST'])
def edit_piece(pid):
    piece = models.get_piece(pid)
    if not piece:
        abort(404)

    if request.method == 'POST':
        name = request.form['name']
        models.update_piece(pid, name)
        flash("Pieza actualizada.")
        return redirect(url_for('main.list_pieces'))

    return render_template('piece_form.html', piece=piece)


@bp.route('/pieces/<int:pid>/delete', methods=['POST'])
def delete_piece(pid):
    piece = models.get_piece(pid)
    if not piece:
        abort(404)

    models.delete_piece(pid)
    flash("Pieza eliminada.")
    return redirect(url_for('main.list_pieces'))



@bp.route('/supplies/<int:sid>/delete', methods=['POST'])
def delete_supply(sid):
    supply = models.get_supply_by_id(sid)
    if not supply:
        abort(404)

    models.delete_supply_by_id(sid)
    flash("Asociación eliminada.")
    return redirect(url_for('main.provider_detail', pid=supply['provider_id']))
