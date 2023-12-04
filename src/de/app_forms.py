"""
Flask WTForms and generating fields with for loop
https://stackoverflow.com/questions/63122912/flask-wtforms-and-generating-fields-with-for-loop
Flask and WTForms for creating multi-part forms
https://copyprogramming.com/howto/multi-part-form-using-flask-wtforms

https://copyprogramming.com/howto/flask-wtform-from-list-of-field-labels
"""

# import yaml
import os

from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import (SelectField, StringField, FormField, FieldList, RadioField, SubmitField
                     # TextAreaField, IntegerField, BooleanField,
                     )
# from wtforms.validators import DataRequired, EqualTo, Length

from data import DCT


app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


def recu(FlaskForm, heads, dat, lev=1):
    """Recursive function for doing everything alright"""
    if isinstance(dat, dict):
        for key, val in dat.items():
            if isinstance(val, dict):
                # heads.append(f"<h{lev}>{key[0]}. {key[1]}, ({key[2]} баллов)</h{lev}>")
                recu(FlaskForm, heads, val, lev=lev+1)
            elif isinstance(val, list):
                return RadioField(f"<h{lev}>{key[0]}. {key[1]}, ({key[2]} баллов)</h{lev}>", choices=val)


class BasedForm(FlaskForm):
    """Рекурсия!"""
    caption = StringField('Caption')
    radio = RadioField('Привет', choices=[(4, 'Да'), (0, 'Нет')])
    # frequency = SelectField(choices=[('monthly', 'Monthly'), ('weekly', 'Weekly')])
    # credit = StringField('Credit')


class TestForm(FlaskForm):
    # forms = FieldList(FormField(BasedForm), min_entries=1)
    forms = FieldList()
    submit = SubmitField('Submit')

DAT = {
    (
      "1.1",
      "Наличие базовых элементов и соответствие техническим требованиям",
      24,
    ): {
      ("3", "Наличие лайфа", 4): [("да", 4), ("нет", 0)],
      ("4", "Наличие стендапа", 4): [("да", 4), ("нет", 0)],
    }
}

@app.route('/', methods=['POST', 'GET'])
def index():
    baseform = BasedForm()
    tf = TestForm()
    data = DAT
    fields = []
    for nam, dat in data.items():
        for _k, _v in dat.items():
            tf.forms.append_entry()
            form.books.entries[-1].name = "rgrgyj"


    #     text_entry = TextForm()
    #     text_entry.text.label = name
    #     text_entry.text.name = name
    #     fields.append(text_entry)
    # form = TextListForm()
    # form.entries = fields
    # if form.is_submitted():
    #     print(request.form)
    return render_template('index.html', form=tf)


    if form.validate_on_submit():
        return {form.library.data: form.data}
    return render_template('index.html', base=baseform, testForm=TestForm())
    # return render_template('index.html', testForm=TestForm(), base=baseform)


# SAVEDATA = False
# if SAVEDATA:
#     YAML_FILENAME = "forms_data.yaml"
#     with open(YAML_FILENAME, 'w') as file:
#         documents = yaml.dump(DCT, file, allow_unicode=True)


app.run()
