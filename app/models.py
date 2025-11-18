from . import db

class Supply(db.Model):
    __tablename__ = 'supply'
    id = db.Column(db.Integer, primary_key=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'), nullable=False)
    piece_id = db.Column(db.Integer, db.ForeignKey('piece.id'), nullable=False)
    price = db.Column(db.Float, nullable=False, default=0.0)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    color = db.Column(db.String(64))
    category = db.Column(db.String(64))

    provider = db.relationship('Provider', back_populates='supplies')
    piece = db.relationship('Piece', back_populates='supplies')


class Provider(db.Model):
    __tablename__ = 'provider'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(200))
    city = db.Column(db.String(100))
    province = db.Column(db.String(100))

    supplies = db.relationship('Supply', back_populates='provider', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Provider {self.name}>'


class Piece(db.Model):
    __tablename__ = 'piece'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    supplies = db.relationship('Supply', back_populates='piece', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Piece {self.name}>'