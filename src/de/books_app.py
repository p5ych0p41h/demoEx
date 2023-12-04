from flask import Flask, render_template
from flask_wtf import FlaskForm, Form
from wtforms import StringField, SubmitField, FieldList, FormField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'apple pie'

DAT = {"tit1": "name1", "tit2": "name2"}


class BookForm(FlaskForm):
    book = StringField()


class LibraryForm(FlaskForm):
    library = StringField()
    books = FieldList()
    submit = SubmitField('Submit')


@app.route('/book', methods=['GET', 'POST'])
def book():
    form = LibraryForm()
    datas = ['cdsvr', 'trsdvck', 'vsdv', "djykfs"]
    labels = ['car', 'truck', 'van', "dsfs"]
    for veh in labels:
        form.books.append_entry()
        # form.books.entries[-1].name = "rgrgyj"
        form.books.entries[-1].label.text = veh
        print(veh)
    if form.validate_on_submit():
        return {form.library.data: form.data}
    # for i in range(4):
    #     form.books.append_entry()

    return render_template('books.html', form=form)


app.run()
