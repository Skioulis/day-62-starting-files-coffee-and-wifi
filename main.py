from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TimeField, SelectField
from wtforms.validators import DataRequired, URL

import csv


'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

cafe_choices=[
    ('☕️','☕️'),
    ('☕️☕️','☕️☕️'),
    ('☕️☕️☕️','☕️☕️☕️'),
    ('☕️☕️☕️☕️','☕️☕️☕️☕️'),
    ('☕️☕️☕️☕️☕️','☕️☕️☕️☕️☕️'),
    ]

wifi_choices = [
    ('✘','✘'),
    ('💪','💪'),
    ('💪💪','💪💪'),
    ('💪💪💪','💪💪💪'),
    ('💪💪💪💪','💪💪💪💪'),
    ('💪💪💪💪💪','💪💪💪💪💪'),
]

power_choices = [
    ('✘','✘'),
    ('🔌','🔌'),
    ('🔌🔌','🔌🔌'),
    ('🔌🔌🔌','🔌🔌🔌'),
    ('🔌🔌🔌🔌','🔌🔌🔌🔌'),
    ('🔌🔌🔌🔌🔌','🔌🔌🔌🔌🔌'),
]

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[
        DataRequired(message="Please Add a name")
    ])
    location = StringField("Cafe Location", validators=[
        DataRequired(message="Enter a valid location"),
        URL(message="Not a Valid url")
    ])
    open = TimeField("Opening Time", validators=[DataRequired()])
    close = TimeField("Closing Time", validators=[DataRequired()])
    coffee = SelectField(u'Coffee Rating', choices=cafe_choices)
    wifi = SelectField(u'Wifi Coverage Rating', choices=wifi_choices)
    power = SelectField(u'Power Socket Availability', choices=power_choices)
    submit = SubmitField('Submit')

    def __str__(self):
        return (f"{self.cafe.data},{self.location.data},{self.open.data},{self.close.data},{self.coffee.data},{self.wifi.data},{self.power.data}")

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET","POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print("True")
        print(form)
        f=open("cafe-data.csv", "a", encoding="utf-8")
        f.write('\n' + form.__str__())
        f.close()

    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
        print(len(list_of_rows))
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
