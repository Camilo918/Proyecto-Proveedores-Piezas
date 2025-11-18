from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import db
from .models import Provider, Piece, Supply

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return redirect(url_for('main.list_providers'))


@bp.route('/providers')
def list_providers():
    providers = Provider.query.all()
    return render_template('providers.html', providers=providers)

@bp.route('/providers/new', methods=['GET', 'POST'])
def new_provider():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form.get('address')
        city = request.form.get('city')
        province = request.form.get('province')
        p = Provider(name=name, address=address, city=city, province=province)
        db.session.add(p)
        db.session.commit()
        flash('Proveedor creado.')
        return redirect(url_for('main.list_providers'))
    return render_template('provider_form.html', provider=None)

@bp.route('/providers/<int:pid>/edit', methods=['GET', 'POST'])
def edit_provider(pid):
    p = Provider.query.get_or_404(pid)
    if request.method == 'POST':
        p.name = request.form['name']
        p.address = request.form.get('address')
        p.city = request.form.get('city')
        p.province = request.form.get('province')
        db.session.commit()
        flash('Proveedor actualizado.')
        return redirect(url_for('main.list_providers'))
    return render_template('provider_form.html', provider=p)

@bp.route('/providers/<int:pid>/delete', methods=['POST'])
def delete_provider(pid):
    p = Provider.query.get_or_404(pid)
    db.session.delete(p)
    db.session.commit()
    flash('Proveedor eliminado.')
    return redirect(url_for('main.list_providers'))

@bp.route('/providers/<int:pid>', methods=['GET', 'POST'])
def provider_detail(pid):
    p = Provider.query.get_or_404(pid)
    pieces = Piece.query.all()
    if request.method == 'POST':

        piece_id = int(request.form['piece_id'])
        price = float(request.form.get('price') or 0)
        quantity = int(request.form.get('quantity') or 0)
        color = request.form.get('color')
        category = request.form.get('category')

        supply = Supply.query.filter_by(provider_id=pid, piece_id=piece_id).first()
        if supply:
            supply.price = price
            supply.quantity = quantity
            supply.color = color
            supply.category = category
        else:
            supply = Supply(provider_id=pid, piece_id=piece_id, price=price, quantity=quantity, color=color, category=category)
            db.session.add(supply)
        db.session.commit()
        flash('Pieza asociada/actualizada para el proveedor.')
        return redirect(url_for('main.provider_detail', pid=pid))
    return render_template('provider_detail.html', provider=p, pieces=pieces)



@bp.route('/pieces')
def list_pieces():
    pieces = Piece.query.all()
    return render_template('pieces.html', pieces=pieces)

@bp.route('/pieces/new', methods=['GET', 'POST'])
def new_piece():
    if request.method == 'POST':
        name = request.form['name']
        piece = Piece(name=name)
        db.session.add(piece)
        db.session.commit()
        flash('Pieza creada.')
        return redirect(url_for('main.list_pieces'))
    return render_template('piece_form.html', piece=None)

@bp.route('/pieces/<int:pid>/edit', methods=['GET', 'POST'])
def edit_piece(pid):
    piece = Piece.query.get_or_404(pid)
    if request.method == 'POST':
        piece.name = request.form['name']
        db.session.commit()
        flash('Pieza actualizada.')
        return redirect(url_for('main.list_pieces'))
    return render_template('piece_form.html', piece=piece)

@bp.route('/pieces/<int:pid>/delete', methods=['POST'])
def delete_piece(pid):
    piece = Piece.query.get_or_404(pid)
    db.session.delete(piece)
    db.session.commit()
    flash('Pieza eliminada.')
    return redirect(url_for('main.list_pieces'))

@bp.route('/supplies/<int:sid>/delete', methods=['POST'])
def delete_supply(sid):
    s = Supply.query.get_or_404(sid)
    provider_id = s.provider_id
    db.session.delete(s)
    db.session.commit()
    flash('Asociación eliminada.')
    return redirect(url_for('main.provider_detail', pid=provider_id))