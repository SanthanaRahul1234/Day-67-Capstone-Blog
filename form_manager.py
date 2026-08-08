from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField # Import this specific field


class Add_Post(FlaskForm):
    new_title = StringField('Name of Post', validators=[DataRequired()] )
    new_subtitle = StringField('Subtitle')
    new_author_name = StringField("Author's Name")
    new_url = StringField("URL")
    # Use CKEditorField for your main text body
    new_body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField('Submit')
