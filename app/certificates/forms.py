from flask_wtf import FlaskForm
from wtforms import FileField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

class CertificateGenerationForm(FlaskForm):
    file = FileField("Excel or CSV File", validators=[DataRequired()])
    title = StringField("Certificate Title", validators=[DataRequired(), Length(min=2, max=255)])
    description = TextAreaField("Description", validators=[DataRequired(), Length(min=5, max=5000)])
    submit = SubmitField("Generate Certificates")