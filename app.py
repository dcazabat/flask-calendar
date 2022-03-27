from flask import Flask, render_template, request, session, redirect, url_for
from datetime import datetime
import calendar
import locale

#calendar.setfirstweekday(firstweekday=6)
app = Flask(__name__)

def calc_calender(date):
    year = date.year
    yearInfo = dict()
    for month in range(1, 13):
        days = calendar.monthcalendar(year, month)
        # if len(days) != 6:
        #     days.append([0 for _ in range(7)])
        month_abbr = calendar.month_abbr[month].capitalize().replace('.','')
        yearInfo[month_abbr] = days
    return yearInfo

def page_not_found(error):
    return render_template('404.html'), 404

@app.route('/', methods=["GET", "POST"])
@app.route('/<this_month>', methods=["GET", "POST"])
@app.route('/home', methods=["GET", "POST"])
@app.route('/home/<this_month>', methods=["GET", "POST"])
def index(this_month=None):
    if request.method == "GET":
        locale.setlocale(locale.LC_ALL, locale.getlocale()[0])
        day_of_week = []
        month_of_year = {}
        for item in range(7):
            day_of_week.append(calendar.day_abbr[item].capitalize().replace('.',''))
        for item in range(1,13):
            month_of_year[calendar.month_abbr[item].capitalize().replace('.','')] = calendar.month_name[item].capitalize()
        date = datetime.today()
        actual_month = calendar.month_abbr[date.month].capitalize().replace('.','')
        if not this_month:
            this_month = calendar.month_abbr[date.month].capitalize().replace('.','')
        if this_month in month_of_year:
            return render_template('index.html',actual_month=actual_month, day_of_week=day_of_week, month_of_year=month_of_year, this_month=this_month, date=date, content=calc_calender(date))
        else:
            return render_template('404.html')

app.register_error_handler(404,page_not_found)
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

if __name__ == '__main__':
    app.run(port=6000, debug=True)