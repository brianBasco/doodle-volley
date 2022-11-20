from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required

db = SQLAlchemy()

# Define models
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

class Doodle(db.Model):
    __tablename__ = 'doodles'
    id = db.Column(db.Integer(), primary_key=True)
    date_doodle = db.Column(db.DateTime(), nullable=False)
    joueurs = db.relationship('Joueur', backref='doodles', lazy=True)

    def __repr__(self):
        return "Doodle n° {} du {}".format(self.id, self.date_doodle.strftime("%d/%m/%Y"))

class Presence(db.Model):
    __tablename__ = 'presences'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String, nullable=False)

    def __repr__(self):
        return self.nom

class Joueur(db.Model):
    __tablename__ = 'joueurs'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String, nullable=False)
    presence = db.Column(db.String, nullable=False)
    doodle = db.Column(db.Integer, db.ForeignKey('doodles.id'),
        nullable=False)

    def __repr__(self):
        #return '<User %r>' % self.nom
        return 'Joueur ' + self.nom

