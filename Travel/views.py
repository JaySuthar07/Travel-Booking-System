from datetime import datetime, timezone
from venv import logger
from flask import Blueprint, render_template, redirect, url_for, request, flash,session
from flask_login import current_user, login_user, logout_user,login_required
from Travel.decorator import admin_required
from Travel.forms import UserRegistrationForm, FlightBookingForm, HotelBookingForm, PackageDealForm, FlightSearchForm, HotelSearchForm, FlightBookingForm, HotelBookingForm, LoginForm, UserRegistrationForm, FlightSearchForm, HotelSearchForm
from .models import Admin, UserRegister, Flight, Hotel, PackageDeal, Booking, db

# admin = Admin(email='admin@gmail.com',password='admin')
# db.session.add(admin)
# db.session.commit() 

bp = Blueprint('travel', __name__)

@bp.route('/')
def home():
    flight_form = FlightSearchForm()
    hotel_form = HotelSearchForm()
    package_form = PackageDealForm()
    
    username = session.get('user', {}).get('username') if session.get('user_logged_in') else None

    return render_template(
        "home.html", username=username,  flight_form=flight_form, hotel_form=hotel_form, package_form=package_form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = UserRegistrationForm()  
    if form.validate_on_submit():
        new_user = UserRegister(
            username=form.username.data,
            email=form.email.data,
        )
        new_user.set_password(form.password.data)  # Hash the password before storing
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('travel.login'))
    return render_template('register.html', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  
    if form.validate_on_submit():
        user = UserRegister.query.filter_by(email=form.email.data).first()  
        if user and user.check_password(form.password.data):  
            session['user_logged_in'] = True
            session['user_id'] = user.id  
            session['username'] = user.username  
            login_user(user)  
            flash('Login successful! Welcome, {}.'.format(user.username), 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('travel.user_dashboard'))
        else:
            flash('Login unsuccessful. Please check your email and password.', 'danger')
    return render_template('login.html', form=form)

@bp.route('/logout')
def logout():
    logout_user()  
    flash('You have been logged out.', 'info')
    return redirect(url_for('travel.login'))


@bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

   
        admin = Admin.query.filter_by(email=email).first()
        if admin and admin.check_password(password):
            session['admin_id'] = admin.id
            session['admin_email'] = admin.email
            session['admin_logged_in'] = True  # Set admin session
            flash('Admin login successful!', 'success')
            return redirect(url_for('travel.admin_dashboard'))  
        else:
            flash('Login unsuccessful. Please check your email and password.', 'danger')

    return render_template('admin_login.html')

@bp.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)  # Remove admin session
    flash('You have been logged out.', 'info')
    return redirect(url_for('travel.admin_login'))


@bp.route('/admin/dashboard')
# @admin_required
def admin_dashboard():
    if not session.get('admin_logged_in'):
        flash('Please log in as admin to access the dashboard.', 'warning')
        return redirect(url_for('travel.admin_login'))
    
    users = UserRegister.query.all()  # Get all users
    total_users = UserRegister.query.count()  # Get total registered users
    total_bookings = Booking.query.count()  # Get total bookings made

    return render_template('admin_dashboard.html', users=users, total_users=total_users, total_bookings=total_bookings)

@bp.route('/user/dashboard')
@login_required
def user_dashboard():
    user = current_user 
    username = session.get('username')  # Fetch the username from the session
    
   
    bookings = Booking.query.filter_by(user_id=user.id).all()
    
    return render_template('user_dashboard.html', user=user, username=username, bookings=bookings)

@bp.route('/flights', methods=['GET'])
def flights():
    flights = Flight.query.all()
    return render_template('flight_avail.html', flights=flights)

@bp.route('/hotels', methods=['GET'])
def hotels():
    hotels = Hotel.query.all()
    return render_template('hotel_avail.html', hotels=hotels)


@bp.route('/add_flight', methods=['GET', 'POST'])
@admin_required
def add_flight():
    if not session.get('user_logged_in') and not session.get('admin_logged_in'):
        flash("Please log in to access your dashboard.", "warning")
        return redirect(url_for('travel.login'))
    flight_id = request.args.get('id')  # Retrieve flight ID from query parameters
    flight = Flight.query.get(flight_id) if flight_id else None 

    form = FlightBookingForm(obj=flight) if flight else FlightBookingForm()

    if form.validate_on_submit():
        if flight:  # Editing an existing flight
            flight.Flight_Name = form.Flight_Name.data
            flight.From = form.From.data
            flight.To = form.To.data
            flight.Departure = form.Departure.data
            flight.Return = form.Return.data or None  
            flight.service_id = form.service_id.data
            flight.availability_count = form.availability_count.data
            flight.price = form.price.data
            flash('Flight updated successfully!', 'success')
        else:  # Creating a new flight
            flight = Flight(
                Flight_Name=form.Flight_Name.data,
                From=form.From.data,
                To=form.To.data,
                Departure=form.Departure.data,
                Return=form.Return.data or None,
                service_id=form.service_id.data,
                availability_count=form.availability_count.data,
                price=form.price.data,
            )
            db.session.add(flight)
            flash('Flight added successfully!', 'success')


        try:
            db.session.commit()
            return redirect(url_for('travel.flights'))  # Redirect to the flight list page
        except Exception as e:
            db.session.rollback()  # Roll back the session if there's an error
            flash('Error occurred while saving the flight: ' + str(e), 'danger')
    else:
        print(form.errors)  # Debugging line to check validation errors

    return render_template('add_flight.html', form=form, flight=flight)


@bp.route('/edit/flight/<int:id>', methods=['GET', 'POST'])
def edit_flight(id):
    flight = Flight.query.or_404(id)  # Retrieve the flight or return 404 if not found

    if not session.get('user_logged_in') and not session.get('admin_logged_in'):
        flash("Please log in to access your dashboard.", "warning")
        return redirect(url_for('travel.login'))

    form = FlightBookingForm(obj=flight)

    if form.validate_on_submit():
        flight.Flight_Name = form.Flight_Name.data
        flight.From = form.From.data
        flight.To = form.To.data
        flight.Departure = form.Departure.data
        flight.Return = form.Return.data or None
        flight.price = form.price.data
        flight.availability_count = form.availability_count.data

        try:
            db.session.commit()
            flash("Flight updated successfully!", 'success')
            return redirect(url_for('travel.flights'))
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred while editing the flight: {e}", "danger")

    return render_template('add_flight.html', form=form, flight=flight)


@bp.route('/book_flight/<int:flight_id>', methods=['GET', 'POST'])
@login_required
def book_flight(flight_id):
    flight = Flight.query.get_or_404(flight_id)
    form = FlightBookingForm(obj=flight)  # Prepopulate form fields with flight data
    flight_availability_count = flight.availability_count
    
    
    if form.validate_on_submit():
        print("Form is valid. Proceeding to save booking.")  
        try:
            booking = Booking(
                user_id=current_user.id,
                flight_id=flight.id,
                booking_date=datetime.now(timezone.utc),
                status='Pending'
            )
            db.session.add(booking)
            flight.availability_count = int(flight_availability_count) - 1 
            db.session.commit()
            flash('Flight booked successfully!', 'success')
            return redirect(url_for('travel.user_bookings'))
        except Exception as e:
            db.session.rollback()  # Rollback in case of errors
            print(f"Error saving booking: {e}") 
            flash('An error occurred while booking the flight.', 'danger')
    else:
        print(form.errors)  # Debugging form errors

    return render_template('book_flight.html', form=form, flight=flight)



@bp.route('/search/flight', methods=['GET', 'POST'])
@login_required
def search_flight():
    form = FlightSearchForm()
    if form.validate_on_submit():
        From = form.from_location.data
        To = form.to_location.data
        flights = Flight.query.filter_by(From=From, To=To).all()
        return render_template('user_flight_avail.html', flights=flights)
    return render_template('flight_search.html', form=form)


@bp.route('/delete/flight/<int:id>', methods=['POST'])
@admin_required
def delete_flight(id):
    try:
        
        flight = Flight.query.get_or_404(id)

        PackageDeal.query.filter_by(flight_id=id).delete()

        db.session.delete(flight)
        db.session.commit()

        flash("Flight and associated package deals have been successfully deleted.", 'success')
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred: {str(e)}", 'danger')

    return redirect(url_for('travel.flights'))

@bp.route('/add_hotel', methods=['GET', 'POST'])
@admin_required
def add_hotel():
    hotel_id = request.args.get('id')
    hotel = Hotel.query.get(hotel_id) if hotel_id else None

    form = HotelBookingForm(obj=hotel) if hotel else HotelBookingForm()

    if form.validate_on_submit():
        try:
            check_in_date = form.Check_In.data
            check_out_date = form.Check_Out.data

            if isinstance(check_in_date, str):
                check_in_date = datetime.strptime(check_in_date, '%Y-%m-%d')
            if isinstance(check_out_date, str):
                check_out_date = datetime.strptime(check_out_date, '%Y-%m-%d')

            if hotel:  # Update existing hotel
                hotel.service_id = form.service_id.data
                hotel.Destination = form.Destination.data
                hotel.Hotel_Name = form.Hotel_Name.data
                hotel.Check_In = check_in_date
                hotel.Check_Out = check_out_date
                hotel.availability_count = form.availability_count.data
                hotel.price = form.price.data
                flash('Hotel updated successfully!', 'success')
            else:  # Create new hotel
                hotel = Hotel(
                    service_id=form.service_id.data,
                    Destination=form.Destination.data,
                    Hotel_Name=form.Hotel_Name.data,
                    Check_In=check_in_date,
                    Check_Out=check_out_date,
                    availability_count=form.availability_count.data,
                    price=form.price.data,
                )
                db.session.add(hotel)
                flash('Hotel added successfully!', 'success')

            db.session.commit()
            return redirect(url_for('travel.hotels'))

        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred while saving the hotel: {e}", 'danger')

    return render_template('add_hotel.html', form=form, hotel=hotel)

@bp.route('/edit/hotel/<int:id>', methods=['GET', 'POST'])
def edit_hotel(id):
    hotel = Hotel.query.get_or_404(id)

    if not session.get('user_logged_in') and not session.get('admin_logged_in'):
        flash("Please log in to access your dashboard.", "warning")
        return redirect(url_for('travel.login'))

    form = HotelBookingForm(obj=hotel)  # Pre-fill the form with the existing hotel data

    if form.validate_on_submit():
        hotel.service_id = form.service_id.data
        hotel.Destination = form.Destination.data
        hotel.Hotel_Name = form.Hotel_Name.data
        hotel.Check_In = form.Check_In.data
        hotel.Check_Out = form.Check_Out.data
        hotel.availability_count = form.availability_count.data
        hotel.price = form.price.data

        try:
            db.session.commit()
            flash("Hotel updated successfully!", 'success')
            return redirect(url_for('travel.hotels'))  
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred while editing the hotel: {e}", "danger")

    return render_template('edit_hotel.html', form=form, hotel=hotel)


@bp.route('/book_hotel/<int:hotel_id>', methods=['GET', 'POST'])
@login_required
def book_hotel(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)
    form = HotelBookingForm(obj=hotel)
    hotel_availability_count = hotel.availability_count
    if form.validate_on_submit():
        booking = Booking(
            user_id=current_user.id,
            hotel_id=hotel_id,
        )
        db.session.add(booking)
        hotel.availability_count = int(hotel_availability_count) - 1 
        db.session.commit()
        flash('Hotel booked successfully!', 'success')
        return redirect(url_for('travel.user_dashboard'))

    form.Hotel_Name.data = hotel.Hotel_Name
    form.Destination.data = hotel.Destination
    form.price.data = hotel.price
    return render_template('book_hotel.html', form=form, hotel=hotel)

@bp.route('/search/hotel', methods=['GET', 'POST'])
@login_required
def search_hotel():
    form = HotelSearchForm()
    if form.validate_on_submit():
        try:
            destination = form.destination.data
            check_in = form.check_in.data
            check_out = form.check_out.data

            query = Hotel.query.filter(Hotel.Destination == destination)

           
            if check_in:
                query = query.filter(Hotel.Check_In >= check_in)

            if check_out:
                query = query.filter(Hotel.Check_Out <= check_out)

  

            hotels = query.all()

            return render_template('user_hotel_avail.html', hotels=hotels)

        except Exception as e:
            flash(f"An error occurred during search: {e}", 'danger')

    return render_template('hotel_search.html', form=form)



@bp.route('/delete/hotel/<int:id>', methods=['POST'])
@admin_required
def delete_hotel(id):
    try:
        hotel = Hotel.query.get_or_404(id)
        
        PackageDeal.query.filter_by(hotel_id=id).delete()
        
        db.session.delete(hotel)
        db.session.commit()
        flash("Hotel has been successfully deleted.", 'success')
        return redirect(url_for('travel.hotels'))
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred: {str(e)}", "danger")

    return redirect(url_for('travel.hotels') if not session.get('admin_logged_in') else url_for('travel.admin_dashboard')) 

@bp.route('/add/package_deal', methods=['GET', 'POST'])
@admin_required
def add_package_deal():
    form = PackageDealForm()

    flights = Flight.query.all()
    hotels = Hotel.query.all()


    form.flight_id.choices = [(flight.id, f"{flight.Flight_Name} | From: {flight.From} To: {flight.To} - Price: ${flight.price}") for flight in flights]
    form.hotel_id.choices = [(hotel.id, f"{hotel.Hotel_Name} | Destination: {hotel.Destination} - Price: ${hotel.price}") for hotel in hotels]

    if form.validate_on_submit():
        flight_id = form.flight_id.data
        hotel_id = form.hotel_id.data

        # Debugging: Print the selected flight and hotel IDs
        print(f"Selected Flight ID: {flight_id}, Selected Hotel ID: {hotel_id}")

        # Fetch the selected flight and hotel
        selected_flight = Flight.query.get(flight_id)
        selected_hotel = Hotel.query.get(hotel_id)

   
        if not selected_flight or not selected_hotel:
            return render_template("add_package_deal.html", error="Selected flight or hotel not found.", form=form)

        # Calculate total price
        total_price = selected_flight.price + selected_hotel.price  # Assuming both have a price attribute

        # Create new package deal
        new_package_deal = PackageDeal(flight_id=flight_id, hotel_id=hotel_id, total_price=total_price)

        # Debugging: Print the new package deal to be added
        print(f"New Package Deal: {new_package_deal}")

        try:
            db.session.add(new_package_deal)
            db.session.commit()
            print("Package Deal added successfully.")
            return redirect(url_for('travel.show_package'))
        except Exception as e:
            print(f"Error adding Package Deal: {e}")
            db.session.rollback()  

    else:
        print(form.errors)  

    return render_template("add_package_deal.html", form=form)

@bp.route('/edit/package_deal/<int:package_id>', methods=['GET', 'POST'])
@admin_required
def edit_package_deal(package_id):
    # Fetch the existing package deal
    package_deal = PackageDeal.query.get_or_404(package_id)

    # Load available flights and hotels
    flights = Flight.query.all()
    hotels = Hotel.query.all()

    if request.method == 'POST':
        flight_id = request.form.get('flight_id')
        hotel_id = request.form.get('hotel_id')

        # Fetch the selected flight and hotel
        selected_flight = Flight.query.get(flight_id)
        selected_hotel = Hotel.query.get(hotel_id)

        # Ensure selected flight and hotel exist
        if not selected_flight or not selected_hotel:
            flash("Selected flight or hotel not found.", "danger")
            return redirect(url_for('travel.edit_package_deal', package_id=package_id))

        # Calculate total price
        total_price = selected_flight.price + selected_hotel.price

        # Update the package deal
        package_deal.flight_id = flight_id
        package_deal.hotel_id = hotel_id
        package_deal.total_price = total_price

        try:
            db.session.commit()
            flash('Package Deal updated successfully!', 'success')
            return redirect(url_for('travel.show_package')) 
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating Package Deal: {e}', 'danger')

    return render_template("edit_package_deal.html", form=PackageDealForm(), package_deal=package_deal, flights=flights, hotels=hotels)

    
@bp.route('/show_package')
def show_package():
    packages = PackageDeal.query.all()
    package_prices = [(package, package.calculate_and_update_price()) for package in packages]
    return render_template('show_package.html', package_prices=package_prices)  

@bp.route('/book/package', methods=['GET', 'POST'])
@login_required
def book_package():
    form = PackageDealForm()
    packages = PackageDeal.query.all()

    if request.method == 'POST':
        package_id = request.form.get('package_id')
        selected_package = PackageDeal.query.get_or_404(package_id)

        new_booking = Booking(user_id=current_user.id, package_id=selected_package.package_id)
        try:
            db.session.add(new_booking)
            db.session.commit()
            flash('Package booked successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error occurred during package booking: {e}', 'danger')

        return redirect(url_for('travel.user_dashboard'))

    return render_template('book_package.html', packages=packages, form=form)


@bp.route('/delete/package/<int:package_id>', methods=['POST'])
@admin_required
def delete_package(package_id):
    package = PackageDeal.query.get_or_404(package_id)
    try:
        db.session.delete(package)
        db.session.commit()
        flash('Package deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error occurred while deleting package: {e}', 'danger')

    return redirect(url_for('travel.show_package'))

@bp.route('/search/package_deals', methods=['GET', 'POST'])
@login_required
def search_package_deals():
    package_form = PackageDealForm()


    package_form.flight_id.choices = [
        (flight.id, f"{flight.Flight_Name} | From: {flight.From} To: {flight.To} | Departure: {flight.Departure.strftime('%Y-%m-%d %H:%M')}")
        for flight in Flight.query.all()
    ]
    
    package_form.hotel_id.choices = [
        (hotel.id, f"{hotel.Hotel_Name} | Destination: {hotel.Destination} | Check-In: {hotel.Check_In.strftime('%Y-%m-%d')}")
        for hotel in Hotel.query.all()
    ]

    if package_form.validate_on_submit():
        flight_id = package_form.flight_id.data
        hotel_id = package_form.hotel_id.data

        selected_flight = Flight.query.get(flight_id)
        selected_hotel = Hotel.query.get(hotel_id)

        if not selected_flight or not selected_hotel:
            return render_template("package_deals.html", error="Selected flight or hotel not found.", package_form=package_form)

        package_deals = PackageDeal.query.filter_by(flight_id=flight_id, hotel_id=hotel_id).all()

        if not package_deals:
            return render_template("package_deals.html", error="No package deals available for the selected flight and hotel.", package_form=package_form)

    
        return render_template("package_deals.html", package_deals=package_deals, package_form=package_form, selected_flight=selected_flight, selected_hotel=selected_hotel)

    return render_template("package_deals.html", package_form=package_form)


@bp.route('/user_bookings',methods=['POST','GET'])
@login_required
def user_bookings():

    all_bookings = Booking.query.filter_by(user_id=current_user.id).all()

    has_bookings = bool(all_bookings)

    flight_bookings = [booking for booking in all_bookings if booking.flight_id is not None]
    hotel_bookings = [booking for booking in all_bookings if booking.hotel_id is not None]
    package_bookings = [booking for booking in all_bookings if booking.package_id is not None]

    return render_template('user_bookings.html', flight_bookings=flight_bookings or None, hotel_bookings=hotel_bookings or None, package_bookings=package_bookings or None, has_bookings=has_bookings)


@bp.route('/cancel/booking/<int:booking_id>', methods=['POST'])
@login_required
def cancel_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)  # Get the booking or return 404
    
    # Check if the booking is already cancelled
    if booking.status == 'Cancelled':
        flash('This booking is already cancelled.', 'warning')
        return redirect(url_for('travel.user_bookings'))

    # Update the booking status to 'Cancelled'
    booking.status = 'Cancelled'
    
    # Determine booking type based on fields:

    # 1. If `package_id` is present, it's a package deal (cancel both flight and hotel)
    if booking.package_id:
        if booking.flight_id:
            flight = Flight.query.get_or_404(booking.flight_id)
            flight.availability_count = int(flight.availability_count) + 1
        if booking.hotel_id:
            hotel = Hotel.query.get_or_404(booking.hotel_id)
            hotel.availability_count = int(hotel.availability_count) + 1

    # 2. If `flight_id` is present, it's a flight booking, so increment flight availability
    elif booking.flight_id:
        flight = Flight.query.get_or_404(booking.flight_id)
        flight.availability_count = int(flight.availability_count) + 1

    # 3. If `hotel_id` is present, it's a hotel booking, so increment hotel availability
    elif booking.hotel_id:
        hotel = Hotel.query.get_or_404(booking.hotel_id)
        hotel.availability_count = int(hotel.availability_count) + 1

    # Commit changes to the database
    try:
        db.session.commit()
        flash('Booking has been cancelled successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error cancelling the booking: {e}', 'danger')

    return redirect(url_for('travel.user_bookings'))


@bp.route('/user_reservations')
def user_reservations():
    reservations = (
        Booking.query
        .join(UserRegister, Booking.user_id == UserRegister.id)
        .outerjoin(Flight, Booking.flight_id == Flight.id)
        .outerjoin(Hotel, Booking.hotel_id == Hotel.id)
        .outerjoin(PackageDeal, Booking.package_id == PackageDeal.package_id)
        .add_columns(
            Booking.id.label("booking_id"),
            UserRegister.username,
            UserRegister.email,
            PackageDeal.package_id,
            Flight.id.label("flight_id"),
            Hotel.id.label("hotel_id"),
            Booking.status  
        ).all()
    )

    reservation_details = []  
    for res in reservations:
        # Query the PackageDeal object if applicable
        package = PackageDeal.query.get(res.package_id) if res.package_id else None
        
        # Start calculating the total price
        total_price = 0
        if package:
            total_price += package.total_price  # Add package price if available
        
        if res.flight_id:
            flight = Flight.query.get(res.flight_id)
            total_price += flight.price if flight else 0  # Add flight price if available
            
        if res.hotel_id:
            hotel = Hotel.query.get(res.hotel_id)
            total_price += hotel.price if hotel else 0  # Add hotel price if available
        
        # Debug log to ensure values are being fetched correctly
        print(f"Reservation ID: {res.booking_id}, Package ID: {res.package_id}, Flight ID: {res.flight_id}, Hotel ID: {res.hotel_id}, Total Price: {total_price}")
        
        reservation_details.append({
            'booking_id': res.booking_id,
            'username': res.username,
            'email': res.email,
            'package_id': res.package_id,
            'flight_id': res.flight_id,
            'hotel_id': res.hotel_id,
            'total_price': total_price,  # Pass the total price
            'status': res.status  # Pass the booking status
        })

    return render_template('user_reservations.html', reservations=reservation_details)

@bp.route('/edit_user_reservation/<int:reservation_id>', methods=['GET', 'POST'])
def edit_user_reservations(reservation_id):
    form = PackageDealForm()
    booking = Booking.query.get_or_404(reservation_id)
    
    if request.method == 'POST':
        try:
            booking.user_id = request.form['user_id']
            booking.flight_id = request.form.get('flight_id')
            booking.hotel_id = request.form.get('hotel_id')
            booking.package_id = request.form.get('package_id')
            booking.status = request.form['status']
            
            db.session.commit()
            flash('Booking updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()  
            flash(f'An error occurred: {str(e)}', 'danger') 
            
        return redirect(url_for('travel.user_reservations'))
    
    return render_template('edit_reservation.html', booking=booking, form=form)


@bp.route('/delete_user_reservation/<int:reservation_id>', methods=['POST','GET'])
def delete_user_reservations(reservation_id):
    booking = Booking.query.get_or_404(reservation_id)
    
    try:
        db.session.delete(booking)
        db.session.commit()
        flash('Booking deleted successfully!', 'success')
    except:
        db.session.rollback()
        flash('Error occurred while trying to delete the booking.', 'danger')
    
    return redirect(url_for('travel.user_reservations'))


@bp.route('/change_status/<int:reservation_id>', methods=['POST'])
def change_status(reservation_id):
    booking = Booking.query.get_or_404(reservation_id)
    booking.status = request.form['status']
    
    db.session.commit()
    flash('Booking status updated!', 'success')
    return redirect(url_for('travel.user_reservations'))

