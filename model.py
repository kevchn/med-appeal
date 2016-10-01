from wtforms import Form, IntegerField, TextAreaField, validators

class InputForm(Form):
    mirna_list = TextAreaField(
        label='Input',
        default="",
        validators=[validators.InputRequired()])
