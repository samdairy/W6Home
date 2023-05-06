from flask import Blueprint, render_template, request, redirect, url_for, flash
from car_inventory.forms import UserLoginForm
from car_inventory.models import User, db, check_password_hash

# Imports for flask login
from flask_login import login_user, logout_user, login_required

auth = Blueprint('auth', __name__, template_folder='auth_templates')

# Two methods GET -> gets the form and POST -> allows the form to post
@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserLoginForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            # Print just to confirm it worked
            print(email, password)

            user = User(email, password = password)

            db.session.add(user)
            db.session.commit()

            flash(f'You have successfully created a user account {email}', 'user-created')

            return redirect(url_for('site.home'))

    except:
        raise Exception('Invalid Form Data: Please Check Your Form Inputs')

    return render_template('signup.html',form = form)

@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = UserLoginForm()

    try:

        if request.method == 'POST' and form.validate_on_submit():
            # if true, get the email from the form
            email = form.email.data
            password = form.password.data
            # Print just to check to make sure it's working
            print(email,password)

 
            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash('You were successfully logged in: via email/password', 'auth-success')
                return redirect(url_for('site.home'))

 
            else:
                flash('Your email/password is incorrect', 'auth-failed')
                return redirect(url_for('auth.signin'))

    except:
        raise Exception('Invalid Form Data: Please Check Your Form!')

    return render_template('signin.html', form=form)


@auth.route('/logout')
# Need to import login_required
@login_required
def logout():
    # Need to import logout_user
    logout_user()
    return redirect(url_for('site.home'))