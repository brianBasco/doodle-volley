import os
from xmlrpc.client import DateTime

from flask import Flask, redirect, render_template, request, session, url_for, flash, abort
from sqlalchemy import false
from models.models import Joueur, db, User, Role, Doodle
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
from datetime import date, datetime, timedelta
from forms.forms import DoodleForm, JoueurForm

# Create app
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'super-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///doodle.sqlite'

# Generate a nice key using secrets.token_urlsafe()
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", 'pf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-wyJILbq_dFw')
# Bcrypt is set as default SECURITY_PASSWORD_HASH, which requires a salt
# Generate a good salt using: secrets.SystemRandom().getrandbits(128)
app.config['SECURITY_PASSWORD_SALT'] = os.environ.get("SECURITY_PASSWORD_SALT", '146585145368132386173505678016728509634')


# Create database connection object
db.init_app(app)

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Create a user to test with
"""
@app.before_first_request
def create_user():
    db.drop_all()
    db.create_all()
    user_datastore.create_user(email='matt@nobien.net', password='password')
    user_datastore.create_user(email='admin@admin.net', password='admin')
    user_datastore.create_user(email='seb@s.net', password='admin')
    db.session.add(Doodle(date_doodle=datetime.now() + timedelta(days=2)))
    #db.save(doodle)
    db.session.commit()
"""

# --------------- Views ---------------------------
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.route('/activate_connexion', methods=['POST'])
def activate_connexion():
    #session["admin"] = False
    #resultats=Doodle.query.all()
    if request.method == 'POST':
        if request.form['login'] == 'marie' and request.form['password'] == 'reinedesponeys':
            session["admin"] = "admin"
            flash("vous êtes connecté !" ,"success")
        else :
            flash("Login incorrect !" ,"danger")
        return redirect(url_for('index'))
    return abort(404)

@app.route('/close_connexion', methods=['GET'])
def close_connexion():
    session.pop("admin", None)
    return redirect(url_for('index'))

@app.route('/', methods=['GET'])
def index():
    doodles = Doodle.query.filter(Doodle.date_doodle >= (datetime.now() + timedelta(hours=-25))).order_by(Doodle.date_doodle)
    return render_template('index.html', doodles=doodles)

        # ------------------- index ----------------------------


def not_admin():
    if "admin" not in session :
        flash("Vous n'êtes pas connecté", "danger")
        return True
    return False



@app.route('/cms/doodles', methods=['GET'])
def get_doodles():
    if not_admin():
        return redirect(url_for('index'))
    doodles = Doodle.query.all()
    return render_template('cms/doodles/index.html', doodles=doodles)


@app.route('/cms/doodles/register', methods=['GET','POST'])
def register_doodle():
    if not_admin():
        return redirect(url_for('index'))
    form = DoodleForm(request.form)
    doodle = Doodle()
    if request.method == 'POST' and form.validate():
        doodle = form.populate_obj(doodle)
        db.session.add(doodle)
        db.session.commit()
        flash("doodle créé", "success")
        return redirect(url_for('index'))
    titre='Enregistrer Doodle'
    return render_template('cms/doodles/edit.html', form=form, titre=titre)

@app.route('/cms/doodles/edit/<int:id>', methods=['GET','POST'])
def edit_doodle(id):
    if not_admin():
        return redirect(url_for('index'))
    doodle = Doodle.query.filter(Doodle.id == id).first_or_404()
    obj = {'id': doodle.id, 'date':doodle.date_doodle}
    form = DoodleForm(request.form, data=obj)
    if request.method == 'POST' and form.validate():
            # update Doodle in the db :
            form.populate_obj(doodle)
            db.session.commit()
            flash("doodle édité", "success")
            return redirect(url_for('get_doodles'))
    titre='Editer Doodle'
    return render_template('cms/doodles/edit.html', form=form, titre=titre)

@app.route('/cms/doodles/delete/<int:id>', methods=['GET','POST'])
def delete_doodle(id):
    if not_admin():
        return redirect(url_for('index'))
    doodle = Doodle.query.filter(Doodle.id == id).first_or_404()
    if request.method == 'POST':
        db.session.delete(doodle)
        db.session.commit()
        flash("doodle supprimé", "success")
        return redirect(url_for('get_doodles'))
    return render_template('cms/doodles/delete.html', objet=doodle, nom='doodle')



@app.route('/ui/register_joueur/<int:doodle>', methods=['GET', 'POST'])
def ui_register_joueur(doodle):
    joueur = Joueur()
    form = JoueurForm(request.form)
    if request.method == 'POST' and form.validate() :
        joueur.nom = form.nom.data
        joueur.presence = form.presence.data
        joueur.doodle = doodle
        db.session.add(joueur)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('ui/edit_joueur.html', form=form)

@app.route('/ui/edit_joueur/<int:id>', methods=['GET', 'POST'])
def ui_edit_joueur(id):
    joueur = Joueur.query.filter(Joueur.id == id).first_or_404()
    form = JoueurForm(request.form,joueur)
    if request.method == 'POST' and form.validate() :
        form.populate_obj(joueur)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('ui/edit_joueur.html', form=form,  id=id)

@app.route('/ui/delete_joueur/<int:id>', methods=['GET'])
def ui_delete_joueur(id):
    joueur = Joueur.query.filter(Joueur.id == id).first_or_404()
    db.session.delete(joueur)
    db.session.commit()
    flash(joueur.nom + " a été supprimé", "success")
    return redirect(url_for('index'))

