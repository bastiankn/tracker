from flask import session, jsonify, request, Blueprint, g
from .user_bp import login_required
from models.user_model import User
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db

bp = Blueprint('change-pw', __name__, url_prefix='/change-pw')

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

def verify_password(hashed_password, password):
    """
    Verifies if the given password matches the hashed password.

    Parameters:
    - hashed_password (str): The hashed password to compare against.
    - password (str): The password to be verified.

    Returns:
    - True if the password matches the hashed password, False otherwise.
    """
    return check_password_hash(hashed_password, password)

def get_logged_in_user():
    """
    Retrieves the logged-in user from the session.

    Returns:
    - The logged-in user object, or None if the user is not logged in.
    """
    user_id = session.get('user_id')
    if user_id is not None:
        # Retrieve the user from the database based on the user_id
        user = User.query.get(user_id)
        return user
    else:
        return None

@bp.route("/", methods=['POST'])
@login_required
def change_password():
    """
    Changes the password of the logged-in user.

    Parameters:
    - None

    Returns:
    - If the current password is incorrect, returns a JSON error message with a 400 status code.
    - If the new password does not meet the policy requirements, returns a JSON error message with a 400 status code.
    - If the password is changed successfully, returns a JSON success message with a 200 status code.
    """
    current_password = request.json.get('current_password')
    new_password = request.json.get('new_password')

    # Retrieve the logged-in user
    user = get_logged_in_user()

    if user is None:
        return jsonify(error='User not found.'), 404

    # Verify the current password
    if not verify_password(user.passwort, current_password):
        return jsonify(error='Incorrect current password.'), 400

    # Password policy check
    if not validate_password(new_password):
        return jsonify(error='Invalid new password. Please follow the password policy.'), 400

    # Update the password
    user.passwort = generate_password_hash(new_password, method='pbkdf2:sha256', salt_length=8)
    db.session.commit()

    return jsonify(message='Password changed successfully.'), 200
