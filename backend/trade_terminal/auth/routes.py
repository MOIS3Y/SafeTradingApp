from flask import jsonify, request, url_for
from flask_praetorian import auth_required, roles_required, current_user
from trade_terminal import db, guard
from trade_terminal.auth import bp, User, blacklist


# ! Authentication routes

@bp.route('/user/login', methods=['POST'])
def login():
    """
    Creates a temporary token for a registered user.
    To create a token, you need to send a json request
    containing the user name and password. To access all protected routes,
    (@auth_required) you need to add the received token in the header.
    Token lifetime is configured in the config.py
    (JWT_ACCESS_LIFESPAN = {'minutes': 20})

    A simple request example:
    --The user must be in the database and the is _active flag must be True--
    curl
    -i
    -X POST
    -H "Content-Type: application/json"
    -d '{"username":"User", "password":"pass"}'
    http://localhost:5000/api/auth/login
    """
    # * Get request to create a token
    request_user = request.get_json(force=True)
    username = request_user.get('username', None)
    password = request_user.get('password', None)
    # * Check request user fields
    user = guard.authenticate(username, password)
    # * Create user token
    user_token = guard.encode_jwt_token(user)

    return jsonify(
        {
            'status_code': 202,
            'error': '',
            'access_token': user_token
        }), 202


@bp.route('/token/refresh', methods=['GET'])
def refresh():
    """
    Refreshes an existing JWT by creating a new one that is a copy of the old
    except that it has a refreshed access expiration.

    A simple request example:
    curl
    -i
    -X GET
    -H "Content-Type: application/json"
    -H "Authorization: Bearer <your_token>"
    http://localhost:5000/api/auth/refresh
    """
    # * Get token from header
    old_token = guard.read_token_from_header()
    # * Make response
    new_token = guard.refresh_jwt_token(old_token)
    return jsonify(
        {
            'status_code': 202,
            'error': '',
            'access_token': new_token
        }), 200


# ! Registration routes

@bp.route('/user/registration', methods=['POST'])
def register():
    """
    Registers a new user by parsing a POST request containing new user info and
    dispatching an email with a registration token

    A simple request example:
    curl
    -i
    -X POST
    -H "Content-Type: application/json"
    -d '{"username":"User", "password":"Pass", "email":"example@mail.domain"}'
    http://localhost:5000/api/auth/registration
    """
    # * Get request for register new user
    request_registration = request.get_json(force=True)
    username = request_registration.get('username', None)
    password = request_registration.get('password', None)
    email = request_registration.get('email', None)
    # * Check the correctness of the request
    if not username or not password or not email:
        return jsonify(
            {
                'status_code': 400,
                'error': 'MissingRequiredFields',
                'message': 'Check for required fields'
            }), 400
    check_user = User.query.filter_by(username=username).first()
    check_email = User.query.filter_by(email=email).first()
    if check_user or check_email:
        return jsonify(
            {
                'status_code': 409,
                'error': 'ConflictUsers',
                'message': 'Username or Email used by another accounts'
            }), 409
    # * Create new user in db
    new_user = User(
        username=username,
        password=guard.hash_password(password),
        email=email,
        roles='user',
        is_active=False)
    db.session.add(new_user)
    db.session.commit()
    # * Send registration email to new user
    # ? You need use Flask-Mail in your app
    guard.send_registration_email(
        email,
        user=new_user,
        # ? In prodaction use frontend app uri from os.environ in config.py
        confirmation_uri=url_for('auth.finalize', _external=True))

    return jsonify(
        {
            'status_code': 201,
            'error': '',
            'message': 'Successfully sent registration email to {}'.format(
                new_user.username)
        }), 201


@bp.route('/user/finalize', methods=['GET'])
def finalize():
    """
    Finalizes a user registration with the token that they were issued in their
    registration email

    A simple request example:

    Click to "submit button" in the input message
    """

    # TODO: Check security hole to blocked user

    # * Get request args with registration token
    registration_token = request.args.get('token', None)
    # * Check registration token
    user = guard.get_user_from_registration_token(registration_token)
    # * Enable new user
    user.is_active = True
    db.session.commit()
    # * Create user token
    user_token = guard.encode_jwt_token(user)

    return jsonify(
        {
            'status_code': 202,
            'error': '',
            'access_token': user_token
        }), 202


# ! Admin routes


@bp.route('/token/blacklist', methods=['POST'])
@auth_required
@roles_required('admin')
def blacklist_token():
    """
    Blacklists an existing JWT by registering its jti claim in the blacklist.

    A simple request example:
    curl
    -i
    -X POST
    -H "Content-Type: application/json"
    -d '{"token":"<your_token>"}'
    http://localhost:5000/api/auth/token/blacklist
    """
    lockable_token = request.get_json(force=True)
    token_data = guard.extract_jwt_token(lockable_token['token'])
    blacklist.add(token_data['jti'])

    return jsonify(
        {
            'status_code': 202,
            'error': '',
            'message': 'token blacklisted ({})'.format(lockable_token['token'])
        }), 202


# ! Test routes

@bp.route('/ping', methods=['GET'])
def ping():
    """
    Simple test route for testing work api-auth routes:
    curl
    -i
    -X GET
    http://localhost:5000/api/auth/ping
    """
    return jsonify({'response': 'pong!'})


@bp.route('/protected', methods=['GET'])
@auth_required
def protected():
    """
    A protected endpoint. The auth_required decorator will require a header
    containing a valid JWT

    A simple request example:
    curl
    -i
    -X GET
    -H "Content-Type: application/json"
    -H "Authorization: Bearer <your_token>"
    http://localhost:5000/api/auth/protected
    """
    return jsonify(message='protected endpoint (allowed user {})'.format(
        current_user().username,))
