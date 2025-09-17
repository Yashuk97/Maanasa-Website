from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message

app = Flask(__name__)

# Configure database connection and security
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'a_very_secure_secret_key'

# Initialize database, bcrypt, and login manager
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'maanasa.inquiries@gmail.com'  # REPLACE WITH YOUR EMAIL
app.config['MAIL_PASSWORD'] = 'ksid epsv ezfs fznm'     # REPLACE WITH YOUR APP PASSWORD
mail = Mail(app)

# This handles the redirection to the login page
@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Define database models before using them
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Project('{self.name}', '{self.location}')"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

# Custom Admin views to secure the dashboard
class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))

class MyProjectView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))
    
    column_list = ('name', 'location', 'description')
    column_labels = dict(name='Project Name', location='Location', description='Description')

# Initialize Flask-Admin after all the models and views are defined
admin = Admin(app, name='Maanasa Admin', template_mode='bootstrap3', index_view=MyAdminIndexView())
admin.add_view(MyProjectView(Project, db.session, name='Projects'))

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/services")
def services():
    all_projects = Project.query.all()
    return render_template("services.html", projects=all_projects)

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Get data from the form
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

        # Send the email and handle any errors
        try:
            mail.send(msg)
            flash("Your message has been sent successfully!", "success")
        except Exception as e:
            flash(f"There was an issue sending your message. Error: {e}", "danger")
            
        
        # Redirect the user back to the contact page
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

if __name__ == "__main__":
    app.run(debug=True)