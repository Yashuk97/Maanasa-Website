from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from flask_admin.form import FileUploadField, ImageUploadField, form
from markupsafe import Markup
import os
import uuid
from datetime import datetime


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'a_very_secure_secret_key'

UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'maanasa.inquiries@gmail.com'  # <-- REPLACE THIS LINE
app.config['MAIL_PASSWORD'] = 'otgn inxt uihy gfum'     # <-- REPLACE THIS LINE
mail = Mail(app)
login_manager.login_view = 'login'

@login_manager.unauthorized_handler
def unauthorized():
    flash("Please log in to get access to this page", "warning")
    return redirect(url_for('login'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    cover_photo_url = db.Column(db.String(255), nullable=True)
    main_photo_url = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(20), nullable=False, default='Past')

    def __repr__(self):
        return f"Project('{self.name}', '{self.location}')"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

class About(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

class MyProjectView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    form_extra_fields = {
        'cover_photo_url': ImageUploadField(
            'Cover Photo (for Project List)',
            base_path=app.config['UPLOAD_FOLDER'],
            url_relative_path='uploads/',
            allow_overwrite=True
        ),
        'main_photo_url': ImageUploadField(
            'Main Project Photo (for Detail Page)',
            base_path=app.config['UPLOAD_FOLDER'],
            url_relative_path='uploads/',
            allow_overwrite=True
        )
    }

    column_list = ('name', 'location', 'description', 'cover_photo_url', 'main_photo_url', 'status')
    column_labels = dict(
        name='Project Name',
        location='Location',
        description='Description',
        cover_photo_url='Cover Photo',
        main_photo_url='Main Photo',
        status='Project Status'
    )

    def _list_thumbnail(view, context, model, name):
        if not model.photo_url:
            return ''
        return Markup(f'<img src="{url_for("static", filename="uploads/" + model.photo_url)}" width="100px">')

    column_formatters = {
        'photo_url': _list_thumbnail
    }

admin = Admin(app, name='Maanasa Admin', template_mode='bootstrap3', index_view=MyAdminIndexView())
admin.add_view(MyProjectView(Project, db.session, name='Projects'))
admin.add_view(ModelView(About, db.session, name='About Us'))


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    about_content = About.query.first()
    return render_template("about.html", about_content=about_content)

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/projects/<status_filter>")
def projects_list(status_filter):
    if status_filter not in ['Ongoing', 'Past']:
        return redirect(url_for('services'))
    projects = Project.query.filter_by(status=status_filter).all()
    return render_template("projects_list.html", projects=projects, status=status_filter)

@app.route("/project/<int:project_id>")
def project_detail(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template("project_detail.html", project=project)

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        project_id = request.form.get('project_id')
        message = request.form.get('message')
        msg = Message(
            subject=f"New Inquiry from Website: {name}",
            sender=app.config['MAIL_USERNAME'],
            recipients=[app.config['MAIL_USERNAME']],
            body=f"Name: {name}\nEmail: {email}\nPhone: {phone}\nProject ID: {project_id}\n\nMessage:\n{message}"
        )
        try:
            mail.send(msg)
            flash("Your message has been sent successfully!", "success")
        except Exception as e:
            print(f"EMAIL SENDING FAILED: {e}") 
            flash(f"There was an issue sending your message. Please try again later.", "danger")
            
        return redirect(url_for('contact'))
    
    all_projects = Project.query.all()
    return render_template("contact.html", projects=all_projects)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('admin.index'))
        else:
            flash("Invalid username or password", "danger")
    return render_template('login.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/chatbot-api", methods=['POST'])
def chatbot_api():
    message = request.json.get("message")
    if "hi" in message.lower():
        response = "Hello. Welcome to Maanasa Constructions. How can I help you today?"
    elif "contact" in message.lower():
        response = "You can contact us through the form on our contact page or drop us an E-mail."
    elif "services" in message.lower():
        response = "We specialize in building Apartments, Residential complexes, Independent Houses, Flat developments."
    elif "quote" in message.lower():
        response = "Please fill out the contact form with details about your project to get a quote."
    elif "thankyou" in message.lower():
        response = "Your Welcome! Is there anything else you would like to know more about?"
    elif "no" in message.lower():
        response = "Thank you for getting in touch with us. Have a great Day!"
    else:
        response = "Not sure about this. Drop us an email on maanasa.inquiries@gmail.com. Our team will get in touch with you soon."
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)