from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from Travel import db, login_manager
from datetime import datetime, timezone
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return UserRegister.query.get(user_id)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    
    def check_password(self, password):
        return self.password == password 

class UserRegister(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.username}>'


class TravelService(db.Model):
    __abstract__ = True  
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, nullable=False)  
    availability_count = db.Column(db.Integer, default=0)  
    price = db.Column(db.Numeric(10, 2), nullable=False) 

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.service_id}>'

class Flight(TravelService):
    __tablename__ = 'flights'
    
    Flight_Name = db.Column(db.String(80), nullable=False)
    From = db.Column(db.String(80), nullable=False)
    To = db.Column(db.String(80), nullable=False)
    Departure = db.Column(db.DateTime, nullable=False)
    Return = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), default='Pending') 

    def calculate_cost(self):
        return self.price

    def __repr__(self):
        return f'<Flight {self.Flight_Name}, ID: {self.service_id}>'

class Hotel(TravelService):
    __tablename__ = 'hotels'
    
    Destination = db.Column(db.String(80), nullable=False)
    Hotel_Name = db.Column(db.String(80), nullable=False)
    Check_In = db.Column(db.DateTime, nullable=False)
    Check_Out = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='Pending') 

    def calculate_cost(self):
        return self.price

    def __repr__(self):
        return f'<Hotel {self.Hotel_Name}>'

class PackageDeal(db.Model):
    __tablename__ = 'package_deals'

    
    package_id = db.Column(db.Integer, primary_key=True)
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.id'), nullable=False)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotels.id'), nullable=False)
    total_price = db.Column(db.Float, nullable=False)

    flight = db.relationship('Flight', backref='package_deals', lazy=True)
    hotel = db.relationship('Hotel', backref='package_deals', lazy=True)

    def calculate_and_update_price(self):
        """Calculates and updates the total price for the package deal."""
        flight_price = self.flight.price if self.flight and self.flight.price is not None else 0
        hotel_price = self.hotel.price if self.hotel and self.hotel.price is not None else 0
        self.total_price = flight_price + hotel_price
        return self.total_price


    def __repr__(self):
        return f'<PackageDeal {self.package_id} - Flight ID {self.flight_id} - Hotel ID {self.hotel_id}>'


class Booking(db.Model):
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.id'), nullable=True)  
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotels.id'), nullable=True)    
    package_id = db.Column(db.Integer, db.ForeignKey('package_deals.package_id'), nullable=True)  
    booking_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))  
    status = db.Column(db.String(20), default='Pending') 

    user = db.relationship('UserRegister', backref='bookings', lazy=True)
    flight = db.relationship('Flight', backref='flight_bookings', lazy=True)
    hotel = db.relationship('Hotel', backref='hotel_bookings', lazy=True)
    package = db.relationship('PackageDeal', backref='package_bookings', lazy=True)

    def __repr__(self):
        return f'<Booking {self.id} - User {self.user_id}>'

    
db.create_all()
