from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Length

# Create Deck Form ==================================================
class CreateDeckForm(FlaskForm):
    name = StringField('Deck Name', validators=[DataRequired(), Length(min=1, max=64)])
    description = TextAreaField('Description', validators=[Length(min=0, max=140)])
    submit = SubmitField('Create')

# Edit Deck Form ====================================================
class EditDeckForm(FlaskForm):
    name = StringField('Deck Name', validators=[DataRequired(), Length(min=1, max=64)])
    description = TextAreaField('Description', validators=[Length(min=0, max=140)])
    submit = SubmitField('Update')

# Create Card Form ==================================================
class CreateCardForm(FlaskForm):
    front = TextAreaField('Card Front', validators=[DataRequired(), Length(min=1, max=64)])
    back = TextAreaField('Card Back', validators=[DataRequired(), Length(min=1, max=64)])
    submit = SubmitField('Create')

# Edit Card Form ====================================================
class EditCardForm(FlaskForm):
    front = TextAreaField('Card Front', validators=[DataRequired(), Length(min=1, max=64)])
    back = TextAreaField('Card Back', validators=[DataRequired(), Length(min=1, max=64)])
    submit = SubmitField('Update')

# Edit User Form ====================================================
class EditUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=6, max=64)])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')
