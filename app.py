import pathlib
import os
import json 
import calendar
import locale
from platform import architecture

from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import url_for
from flask import flash
from datetime import datetime
from datetime import timedelta
from cryptography.fernet import Fernet

app = Flask(__name__)


file = pathlib.Path('keys.key')
if file.exists():
    with open('keys.key') as linea:
       app.secret_key = linea.read()
else:
    app.secret_key = Fernet.generate_key()
    archkey = open('keys.key', 'w')
    archkey.writelines(str(app.secret_key))
    archkey.close()

# Users
with open('./static/jsons/users.json', encoding="utf8") as file:
    datos = json.load(file)

# Diccionario de que Contiene parametros Globales de la App
data={
    'title':'Sample Flask Calendar with Bootstrap and SQLAlchemy',
    'message': '',
    'messagealternative':'',
    'errbd': False,
}

users = datos['users']
str_date = ''
day_of_week = []
month_of_year = {}
day_of_week_full = []
locale.setlocale(locale.LC_ALL, locale.getlocale()[0])
for item in range(7):
    day_of_week_full.append(calendar.day_name[item].capitalize().replace('.',''))
for item in range(7):
    day_of_week.append(calendar.day_abbr[item].capitalize().replace('.',''))
for item in range(1,13):
    month_of_year[calendar.month_abbr[item].capitalize().replace('.','')] = calendar.month_name[item].capitalize()

def page_not_found(error):
    return render_template('404.html'), 404

def calc_calender(date):
    year = date.year
    yearInfo = dict()
    for month in range(1, 13):
        days = calendar.monthcalendar(year, month)
        month_abbr = calendar.month_abbr[month].capitalize().replace('.','')
        yearInfo[month_abbr] = days
    return yearInfo


@app.route('/')
@app.route('/home')
def index():
    data['message'] = 'Bienvenidos al Sitio'
    data['messagealternative'] = 'Ingreso al sistema'
    if 'username' in session:
        return redirect('/calendar')
    else:
        return render_template('/index.html',data=data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)
    _user = request.form['txtUser']
    _pass = request.form['txtPassword']
    print(_user, _pass)
    usuario = [{'username': user["username"],
                 'pass': user["pass"], 
                 'name': user["name"], 
                 'dni': user["dni"], 
                 'isadmin': user["isadmin"], 
                 'superuser': user["superuser"]} 
                for user in users 
                if user["username"] == _user]
    usuario = usuario[0]
    if request.method == 'POST':
        if usuario['pass'] == _pass and usuario['username'] == _user:
            session['username'] = _user
            session['name'] = usuario['name']
            session['dni'] = usuario['dni']
            session['isadmin'] = usuario['isadmin']
            session['superuser'] = usuario['superuser']
            return redirect('/calendar')
        else:
            flash('Datos de Usuario y/o Contraseña INVALIDOS !!!')
            return redirect('/')
    else:
        return redirect('/')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('name', None)
    session.pop('dni', None)
    session.pop('isadmin', None)
    session.pop('superuser', None)
    session.clear()
    return redirect('/')


@app.route('/calendar', methods=["GET", "POST"])
@app.route('/calendar/<this_month>', methods=["GET", "POST"])
def calendar_py(this_month=None):
    data['message'] = 'Calendario Dinamico'
    date = datetime.today()
    actual_month = calendar.month_abbr[date.month].capitalize().replace('.','')
    if not this_month:
        this_month = calendar.month_abbr[date.month].capitalize().replace('.','')
    if this_month in month_of_year:
        return render_template('calendar.html',actual_month=actual_month, day_of_week=day_of_week, month_of_year=month_of_year, this_month=this_month, date=date, content=calc_calender(date), data=data)
    else:
        return render_template('404.html')

@app.route('/validate', methods=["GET", "POST"])
def validate():
    data['message'] = 'Informa y Valida Fecha'
    if request.method == "POST":
        day = request.form['day']
        month = request.form['month']
        year = request.form['year']
        try:
            date = datetime(int(year), int(month), int(day)).date()
        except:
            flash('Fecha Invalida !!!')
            return redirect('/validate')
    elif request.method == "GET":
        date = datetime.today()
    str_date = day_of_week_full[datetime(int(date.year), int(date.month), int(date.day)).weekday()]
    return render_template('validate.html', str_date=str_date, data=data, date=date)

# Captura del Error 404, se puede hacer con los otros Errores
app.register_error_handler(404,page_not_found)
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

if __name__ == '__main__':
    app.run(port=5000, debug=True)