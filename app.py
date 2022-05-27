from flask import Flask, render_template, url_for, redirect, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from datetime import datetime
import base64

from face_recognize import FaceRecognize

app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'
faceRec = FaceRecognize()

# def data_uri_to_cv2_img(uri):
#     encoded_data = uri.split(',')[1]
#     nparr = np.fromstring(encoded_data.decode('base64'), np.uint8)
#     img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
#     return img
#
# img = data_uri_to_cv2_img(data_uri)
# cv2.imshow(img)

'''
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
'''
def markAttendance(names):
    now = datetime.now()
    dateString = now.strftime('%H:%M:%S')
    for name in names:
        new_user = User(username=name, date=dateString)
        db.session.add(new_user)
        db.session.commit()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    date = db.Column(db.String(80), nullable=False)


class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    submit = SubmitField('Register')


'''
    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')
'''

class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    submit = SubmitField('Check Attendance')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/check_attendance', methods=['GET', 'POST'])
def check_attendance():
    print("check attendance")
    form = LoginForm()
    if form.is_submitted():
        print("form submitted")
        users = User.query.filter_by(username=form.username.data).all()
        print(users)
        marked_time_list = []
        for user in users:
            if user:
                if user.date:
                    print(user.date)
                    marked_time_list.append(user.date)
            else:
                return "user doesnt exist"
        return jsonify(marked_time_list)
    else:
        print("not submitted")
    return render_template('check_attendance.html', form=form)

''' 
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

'''
@ app.route('/mark_attendance', methods=['GET', 'POST'])
def mark_attendance():
    form = RegisterForm()
    if form.validate_on_submit():
        # hashed_password = bcrypt.generate_password_hash(form.password.data)
        markAttendance([form.username.data])
        return redirect(url_for('check_attendance'))
    return render_template('mark_attendance.html', form=form)

@app.route('/attendance', methods=['GET','POST'])
def attendance():
    if request.method == 'POST':
        imgdata = base64.b64decode(request.form['file'].split(',')[1])
        filename = 'img.jpg'
        with open(filename,"wb") as f:
            f.write(imgdata)

        names = faceRec.findName("img.jpg")
        markAttendance(names)
        print(names)
        # return jsonify(request.form['userID'], request.form['file'])
        return(jsonify(names))
    return render_template('attendance.html')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", ssl_context="adhoc")
