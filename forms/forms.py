from wtforms import Form, TextAreaField, SelectField, IntegerField, BooleanField, StringField, PasswordField, validators, DateTimeField, DateField, TimeField
from utils.utils import get_datetime, presences

class DoodleForm(Form):
    id = IntegerField("ID")
    date = DateField('Date')

    def populate_obj(self, obj):
        #doodle_date = get_datetime(self.date.data,self.heure.data)
        #obj.date_doodle=doodle_date
        obj.date_doodle=self.date.data
        return obj

class JoueurForm(Form):
    nom = StringField('Nom', [validators.DataRequired()])
    presence = SelectField(u'Présence', choices=[(x,x) for x in presences])

    def populate_obj(self, obj):
        obj.nom=self.nom.data
        obj.presence=self.presence.data
        return obj