from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from app.models import Offer
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import (
    DataRequired,
    Length,
    ValidationError,
)


class NewOfferForm(FlaskForm):
    title = StringField("Offer Name", validators=[
                        DataRequired(), Length(max=50)])
    description = TextAreaField(
        "Offer Description", validators=[DataRequired(), Length(max=150)]
    )
    icon = FileField("Icon", validators=[
                     DataRequired(), FileAllowed(["jpg", "png"])])
    price = StringField("Price", validators=[DataRequired(), Length(max=9)])
    submit = SubmitField("Create")

    def validate_title(self, title):
        offer = Offer.query.filter_by(title=title.data).first()
        if offer:
            raise ValidationError(
                "Offer name already exists! Please choose a different one"
            )
