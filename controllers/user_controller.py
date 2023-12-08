# controllers/user_controller.py
from itsdangerous import URLSafeTimedSerializer
from flask import render_template, flash, redirect, url_for, session, jsonify, request
import models.user as user_model
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import config

MAIL_USERNAME = config.MAIL_USERNAME
MAIL_PASSWORD = config.MAIL_PASSWORD

serializer = URLSafeTimedSerializer(config.SECRET_KEY)


def home():
    return render_template('home.html')


def profile():
    user_name = session.get('user_name')
    email = session.get('email')
    if user_name and email:
        return render_template('user.html', user=user_name)
    else:
        flash("You need to log in first.", 'warning')
        return redirect(url_for('form_bp.home'))


def forgot_password():
    if request.method == 'POST':
        data = request.json
        email = data.get('email')

        user = user_model.find_user_by_email(email)
        if user:
            expiration_time = datetime.utcnow() + timedelta(minutes=1)
            token_data = {'email': email, 'exp': expiration_time.timestamp()}
            token = serializer.dumps(token_data, salt='forgot-password')

            subject = 'Password Reset Request'
            reset_link = url_for('form_bp.reset_password', token=token, _external=True)
            body = f'Click the following link to reset your password: {reset_link}'

            # Create the MIMEText object for the email body
            msg = MIMEMultipart()
            msg.attach(MIMEText(body, 'plain'))

            # Set the email subject and recipients
            msg['Subject'] = subject
            msg['From'] = MAIL_USERNAME
            msg['To'] = email

            # Use your SMTP server to send the email
            try:
                server = smtplib.SMTP(config.smtp_domain, config.smtp_port)
                server.starttls()
                server.login(MAIL_USERNAME, MAIL_PASSWORD)  # Replace with your email and password

                server.sendmail(MAIL_USERNAME, email, msg.as_string())
                server.quit()

                flash('Password reset link sent to your email. Please check your inbox.', 'success')
            except Exception as e:
                print(e)
                flash('Failed to send the reset email. Please try again later.', 'danger')
            message = "Password reset link sent to your email."
            return success_response(True,message)
        else:
            flash('Email not found.', 'danger')
            message = 'Email not found. Try again'
            return success_response(False, message)

    return render_template('home.html')


def reset_password(token):
    try:
        token_data = serializer.loads(token, salt='forgot-password', max_age=3600)
        email = token_data.get('email')
        expiration_time = datetime.fromtimestamp(token_data.get('exp'))

        if datetime.utcnow() > expiration_time:
            flash('The password reset link has expired. Please request a new one.', 'danger')
            return redirect(url_for('form_bp.home'))

    except Exception as e:
        print(e)
        flash('Invalid or expired token. Please try again.', 'danger')
        return redirect(url_for('form_bp.home'))

    if request.method == 'GET':
        return render_template('reset_password.html',user_email=email)


def update_reset_password():
    if request.method == 'POST':
        data = request.json
        email = data.get('email')

        user = user_model.find_user_by_email(email)

        if user:
            password = data.get('password')
            user_model.update_user_password(email, password)

            flash('Password updated successfully')
            message = 'Password updated successfully'
            return success_response(True, message)
        else:
            flash('Password not updated')
            message = 'Password not updated'
            return success_response(False, message)


def logout():
    session.pop('user_name', None)
    session.pop('email', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('form_bp.home'))


def login():
    if request.method == 'POST':
        data = request.json

        user = user_model.login(data)
        if user:
            session['user_name'] = user['name']
            session['email'] = user['email']

            message = 'Login successfully.'
            resp = success_response(True, message)
            # Set the user information in cookies
            resp.set_cookie('user_name', user['name'])
            resp.set_cookie('user_email', user['email'])
            return resp
        else:
            message = 'Invalid email or password.'
            return success_response(False, message)
    else:
        return redirect(url_for('form_bp.home'))


def register():
    if request.method == 'POST':
        data = request.json
        name = data.get('name')
        email = data.get('email')

        try:
            user_model.insert_into_users(data)

            # Set session variables
            session['user_name'] = name
            session['email'] = email

            message = 'Created successfully.'
            resp = success_response(True, message)
            # Set the user information in cookies
            resp.set_cookie('user_name', name)
            resp.set_cookie('user_email', email)
            return resp
        except Exception as e:
            return success_response(False, str(e))
    else:
        return redirect(url_for('form_bp.home'))


def get_all_data():
    if request.method == 'GET':
        all_users = user_model.all_users()

        # response = {
        #     'success': True,
        #     'message': 'User data retrieved successfully',
        #     'users_data': all_users
        # }
        message = 'User data retrieved successfully'
        return success_response(True, message,all_users)


def get_one_data():
    if request.method == 'POST':
        id = request.json.get('id')
        user = user_model.find_user_by_id(id)

        # response = {
        #     'success': True,
        #     'message': 'User data retrieved successfully',
        #     'users_data': user
        # }
        message = 'User data retrieved successfully'
        return success_response(True, message, user)


def update_user():
    if request.method == 'POST':
        data = request.json
        id = data.get('id')
        try:
            user_model.update_user(data,id)
            message = 'Updated successfully.'
            return success_response(False, message)
        except Exception as e:
            return success_response(False, str(e))
    else:
        return redirect(url_for('form_bp.home'))


def page_not_found(error):
    return render_template("error_404.html")


def server_error(error):
    return render_template("error_500.html")


def success_response(success, message, data=None):
    response = {
        'success': success,
        'message': message,
    }

    if data is not None:
        response['resp_data'] = data

    return jsonify(response)