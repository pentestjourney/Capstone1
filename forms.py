"""Forms for hardware listings app."""

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, TextAreaField, BooleanField, FloatField, PasswordField
from wtforms.validators import InputRequired, Length, NumberRange, URL, Optional


class UserForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])


class AddHardwareForm(FlaskForm):
    """Form for adding hardware listings."""

    name = StringField(
        "Hardware",
        validators=[InputRequired()],
    )

    condition = SelectField(
        "Condition",
        choices=[("new", "New"), ("used", "Used")],
    )

    photo_url = StringField(
        "Photo URL",
        validators=[Optional(), URL()],
    )

    price = FloatField(
        "Price",
        validators=[Optional(), NumberRange(min=0, max=10000)],
    )

    notes = TextAreaField(
        "Description",
        validators=[Optional(), Length(min=10)],
    )


class EditHardwareForm(FlaskForm):
    """Form for editing an existing listing."""

    photo_url = StringField(
        "Photo URL",
        validators=[Optional(), URL()],
    )

    notes = TextAreaField(
        "Description",
        validators=[Optional(), Length(min=10)],
    )
