from flask import Flask, jsonify, request, Blueprint, g, redirect, url_for, session
from models.user_model import User
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from functools import wraps
from app import db

bp = Blueprint('user', __name__, url_prefix='/user')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('UserLoggedIn'):
            # Redirect to the login route or return an authentication error
            return jsonify(error='Not authenticated'), 401
        return f(*args, **kwargs)
    return decorated_function

def validate_email(email):
    """
    Validates the emails based on the specified policy.

    Parameters:
    - email (str): The email to be validated.

    Returns:
    - True if the email meets the basic email requirements, False otherwise.
    """
    import re
    email_regex = re.compile(r'^[\w\-\.]+@([\w-]+\.)+[\w-]{2,4}$')
    return re.match(email_regex, email) is not None

def validate_password(password):
    """
    Validates the password based on the specified policy.

    Parameters:
    - password (str): The password to be validated.

    Returns:
    - True if the password meets the policy requirements, False otherwise.
    """
    # Password policy regular expression
    import re
    password_regex = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{14,}$'

    return re.match(password_regex, password) is not None

@bp.route("/login", methods=['POST'])
def login():
    """
    Authenticate a user based on their email and password.

    This route allows users to log in by providing their email and password
    in the request JSON. It fetches the user's information from the database
    using the provided email and checks if the password provided in the request
    matches the stored password hash for that user.

    Args:
        None

    Returns:
        If authentication is successful, returns a success message with a status code 200.
        If the provided email or password is invalid, returns an error message with a
        status code 401 (Unauthorized).

    Raises:
        None
    """
    email = request.json.get('email')
    passwort = request.json.get('passwort')

    # Fetch the user from the database based on the email
    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.passwort, passwort):
        # Password matches, user is authenticated
        session['user_id'] = user.id
        session['UserLoggedIn'] = True 
        session['UserLastname'] = user.lastName
        session['UserFirstname'] = user.firstName
        session['UserEmail'] = user.email
        return 'Logged in successfully', 200
    else:
        # Invalid email or passwort
        return 'Invalid email or passwort', 401

@bp.route("/logout", methods=['POST'])
def logout():
    if 'user_id' in session:
        session.clear()

        return 'Logged out successfully', 200
    else:
        return 'No user is logged in', 401


@bp.route("/session_data", methods=['GET'])
def get_user_data():
    user_id = session.get('user_id')
    user_logged_in = session.get('UserLoggedIn')
    user_lastname = session.get('UserLastname')
    user_firstname = session.get('UserFirstname')
    user_email = session.get('UserEmail')

    if user_id:
        return jsonify({
            'user_id': user_id,
            'UserLoggedIn': user_logged_in,
            'UserLastname': user_lastname,
            'UserFirstname': user_firstname,
            'UserEmail': user_email
        }), 200
    else:
        return 'No user is logged in', 401

@bp.route("/", methods=['POST'])
@login_required
def add_user():
    """
    Adds a new user to the database.

    Parameters:
    - None
    - If the user is added successfully, returns a JSON success message with a 200 status code.
    """

    # Password validation
    password = request.json.get('passwort')
    if not validate_password(password):
        return jsonify(error='Invalid password. Please follow the password policy.'), 400

    email_valid = request.json.get('email')
    if not validate_email(email_valid):
        return jsonify(error='Invalid email. Please give valid email.'), 400
    

    # Insert the user data into the database
    else:
        user_data = User(
            firstName = request.json.get('firstName'),
            lastName = request.json.get('lastName'),
            email = request.json.get('email'),
            passwort = generate_password_hash(request.json.get('passwort'),
                method='pbkdf2:sha256', salt_length=8),
        )

        db.session.add(user_data)
        db.session.commit() 

        return jsonify(message='Example data seeded successfully'), 201

@bp.route("/", methods=['GET'])
@login_required
def get_all_user():
    """
    Retrieves all users and correspoding email and returns their data in JSON format.
    Returns:
        A JSON response containing the data of all users.
            - If successful, returns a 200 status code.
            - If an error occurs, returns a 500 status code with an error message.
    """
    try:
        users = User.query.all()
        users_data = [
            {
                'id': user.id,
                'firstName': user.firstName,
                'lastName': user.lastName,
                'email': user.email
            }
            for user in users
        ]
        return jsonify(users_data), 200

    except Exception as e:
        return jsonify(error=f'Error retrieving user roles: {str(e)}'), 500
    

@bp.route("/<int:user_id>", methods=['GET'])
@login_required
def get_user(user_id):
    """
    Retrieves a specific user by their ID.
    Parameters:
        user_id (int): The ID of the user to retrieve.
    Returns:
        tuple: A JSON response containing the user data and a status code. The user data
            includes the following fields:
            - id (int): The ID of the user.
            - firstName (str): The first name of the user's username.
            - lastName (str): The last name of the user's username.
    Raises:
        Exception: If an error occurs while retrieving the user.
    """
    try:
        user_id = request.view_args.get('user_id')
        user = User.query.get_or_404(user_id)
        user_data = {
                'id': user.id,
                'firstName': user.firstName,
                'lastName': user.lastName,
                'email': user.email
            }
        return jsonify(user_data), 200

    except Exception as e:
            db.session.rollback()
            return jsonify(error=f'Error deleting user role: {str(e)}'), 500
    

@bp.route("/<int:user_id>", methods=['PUT'])
@login_required
def update_user(user_id):
    try:
        user_id = request.view_args.get('user_id')
        user = User.query.get_or_404(user_id)
        
        user.firstName = request.json.get('firstName')
        user.lastName = request.json.get('lastName')

        db.session.commit()

        return jsonify(message='User updated successfully'), 200

    except Exception as e:
        db.session.rollback()
        return jsonify(error=f'Error updating user: {str(e)}'), 500

@bp.route("/<int:user_id>", methods=['DELETE'])
@login_required
def delete_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
            
        db.session.delete(user)
        db.session.commit()

        return jsonify(message='User deleted successfully'), 200

    except Exception as e:
        db.session.rollback()
        return jsonify(error=f'Error deleting user: {str(e)}'), 500