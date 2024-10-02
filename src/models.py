from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorites = db.relationship('Favorites', backref='client', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    url = db.Column(db.String(150), unique=False, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url
        }
    

class Vehicles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    url = db.Column(db.String(150), unique=False, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url
        }


class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    url = db.Column(db.String(150), unique=False, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url
        }

class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'), nullable=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'),nullable=True)


    # client = db.relationship('User', backref='favorites')
    vehicle = db.relationship('Vehicles', backref='favorites')
    character = db.relationship('Characters', backref='favorites')
    planet = db.relationship('Planets', backref='favorites')

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id
        }
