from flask import Flask, render_template, request, session, redirect, url_for
from datetime import datetime
import calendar
import locale

app = Flask(__name__)

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

@app.route('/', methods=["GET", "POST"])
@app.route('/<this_month>', methods=["GET", "POST"])
@app.route('/home', methods=["GET", "POST"])
@app.route('/home/<this_month>', methods=["GET", "POST"])
def index(this_month=None):
    print(request.method)
    if request.method == "POST":
        day = request.form['day']
        month = request.form['month']
        year = request.form['year']
        date = datetime(int(year), int(month), int(day)).date()
    else:
        date = datetime.today()
    str_date = day_of_week_full[datetime(int(date.year), int(date.month), int(date.day)).weekday()]
    actual_month = calendar.month_abbr[date.month].capitalize().replace('.','')
    if not this_month:
        this_month = calendar.month_abbr[date.month].capitalize().replace('.','')
    if this_month in month_of_year:
        return render_template('index.html',actual_month=actual_month, day_of_week=day_of_week, month_of_year=month_of_year, this_month=this_month, date=date, content=calc_calender(date), str_date=str_date)
    else:
        return render_template('404.html')

app.register_error_handler(404,page_not_found)
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

if __name__ == '__main__':
    app.run(port=5000, debug=True)