from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv
import os
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
app.config['SECRET_KEY'] =os.environ.get('FLASK_KEY')
Bootstrap5(app)


class LibForm(FlaskForm):
    lib = StringField('Library name', validators=[DataRequired()])
    location = StringField("Library Location on Google Maps (URL)", validators=[DataRequired(), URL()])
    open = StringField("Opening Time e.g. 8AM", validators=[DataRequired()])
    close = StringField("Closing Time e.g. 5:30PM", validators=[DataRequired()])
    wifi_rating = SelectField("Wi-Fi Strength Rating", choices=["✘", "📶️", "📶📶", "📶📶📶", "📶📶📶📶", "📶📶📶📶📶"], validators=[DataRequired()])
    noise_level = SelectField("Noise levl Rating", choices=["✘", "🔊", "🔊🔊", "🔊🔊🔊", "🔊🔊🔊🔊", "🔊🔊🔊🔊🔊"], validators=[DataRequired()])
    seating_comfort = SelectField("Seating comfort rating", choices=[ "🪑", "🪑🪑", "🪑🪑🪑", "🪑🪑🪑🪑", "🪑🪑🪑🪑🪑"], validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_lib():
    form = LibForm()
    if form.validate_on_submit():
        with open("lib-data.csv", mode="a", encoding='utf-8') as csv_file:
            csv_file.write(f"\n{form.lib.data},"
                           f"{form.location.data},"
                           f"{form.open.data},"
                           f"{form.close.data},"
                           f"{form.wifi_rating.data},"
                           f"{form.noise_level.data},"
                           f"{form.seating_comfort.data}")
        return redirect(url_for('libbs'))
    return render_template('add.html', form=form)


@app.route('/library')
def libbs():
    with open('lib-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('libs.html', libs=list_of_rows)


if __name__ == '__main__':
    app.run(debug=False, port=5002)
