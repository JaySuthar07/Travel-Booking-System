from flask_wtf import FlaskForm
from wtforms import DateField, DecimalField, PasswordField, StringField, IntegerField, DateTimeField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Optional, EqualTo


class UserRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')]) 
    submit = SubmitField('Register')

    
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class FlightBookingForm(FlaskForm):
    Flight_Name = StringField('Flight Name', validators=[DataRequired()])
    From = StringField('From', validators=[DataRequired()])
    To = StringField('To', validators=[DataRequired()])
    Departure = DateField('Departure Date', format='%Y-%m-%d', validators=[DataRequired()])
    Return = DateField('Return Date', format='%Y-%m-%d', validators=[Optional()])
    availability_count = IntegerField('Availability Count', validators=[DataRequired()])
    service_id = IntegerField('Service ID', validators=[DataRequired()])
    price = DecimalField('Price', places=2, validators=[DataRequired()])
    submit = SubmitField('Add Flight')


class FlightSearchForm(FlaskForm):
    from_location = StringField('From Location', validators=[DataRequired(), Length(max=100)])
    to_location = StringField('To Location', validators=[DataRequired(), Length(max=100)])
    departure_date = DateField('Departure Date', format='%Y-%m-%d', validators=[Optional()])
    return_date = DateField('Return Date', format='%Y-%m-%d', validators=[Optional()])
    submit = SubmitField('Search Flights')


class HotelBookingForm(FlaskForm):
    Hotel_Name = StringField('Hotel Name', validators=[DataRequired()])
    Destination = StringField('Destination', validators=[DataRequired()])
    Check_In = DateField('Check-In Date', format='%Y-%m-%d', validators=[DataRequired()])
    Check_Out = DateField('Check-Out Date', format='%Y-%m-%d', validators=[DataRequired()])
    price = DecimalField('Price', places=2, validators=[DataRequired()])
    availability_count = IntegerField('Availability Count', validators=[DataRequired()])  # New field added
    service_id = IntegerField('Service ID', validators=[DataRequired()])  # New field added
    submit = SubmitField('Book Hotel') 


class HotelSearchForm(FlaskForm):
    destination = StringField('Destination', validators=[DataRequired(), Length(max=100)])
    check_in = DateTimeField('Check-In', format='%Y-%m-%d', validators=[Optional()])
    check_out = DateTimeField('Check-Out', format='%Y-%m-%d', validators=[Optional()])
    submit = SubmitField('Search Hotels')


class PackageDealForm(FlaskForm):
    flight_id = SelectField('Select Flight', coerce=int, validators=[DataRequired()])
    hotel_id = SelectField('Select Hotel', coerce=int, validators=[DataRequired()])

    submit = SubmitField('Book Package')