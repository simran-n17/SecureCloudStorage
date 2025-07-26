from flask_login import LoginManager
from flask import Flask, render_template, redirect, request, flash, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from cryptography.fernet import Fernet
from io import BytesIO
import boto3
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key\\'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# Fernet key management
KEY_FILE = 'fernet.key'
if os.path.exists(KEY_FILE):
    with open(KEY_FILE, 'rb') as f:
        key = f.read()
else:
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as f:
        f.write(key)

cipher_suite = Fernet(key)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# AWS setup
s3 = boto3.client('s3')
S3_BUCKET = 'hybrid-secure-storage'  # Replace with your actual bucket name

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Upload Route
@app.route('/upload', methods=['POST'])
@login_required
def upload():
    file = request.files.get('file')

    if not file or not allowed_file(file.filename):
        flash('Invalid file type. Only PDF, DOCX, and TXT allowed.')
        return redirect(url_for('home'))

    filename = secure_filename(file.filename)

    try:
        # Ensure temp folder exists
        os.makedirs('temp', exist_ok=True)

        # Save uploaded file locally
        local_path = os.path.join('temp', filename)
        file.save(local_path)

        # Read and encrypt the file
        with open(local_path, 'rb') as f:
            data = f.read()
        encrypted_data = cipher_suite.encrypt(data)

        # Save encrypted file
        encrypted_path = os.path.join('temp', filename + '.enc')
        with open(encrypted_path, 'wb') as f:
            f.write(encrypted_data)

        # Upload to S3
        s3_key = f'encrypted/{filename}.enc'
        s3.upload_file(encrypted_path, S3_BUCKET, s3_key)
        flash('File encrypted and uploaded successfully!')

    except Exception as e:
        flash(f'Upload failed: {e}')

    finally:
        # Clean up files
        if os.path.exists(local_path):
            os.remove(local_path)
        if os.path.exists(encrypted_path):
            os.remove(encrypted_path)

    return redirect(url_for('home'))

# Downloads Route (merged and fixed)
@app.route('/downloads', methods=['GET', 'POST'])
@login_required
def downloads():
    if request.method == 'GET':
        try:
            response = s3.list_objects_v2(Bucket=S3_BUCKET, Prefix='encrypted/')
            encrypted_files = [
                obj['Key'].replace('encrypted/', '').replace('.enc', '')
                for obj in response.get('Contents', [])
                if obj['Key'].endswith('.enc')
            ]
        except Exception as e:
            encrypted_files = []
            flash(f"Error fetching file list: {str(e)}")
        return render_template('downloads.html', encrypted_files=encrypted_files)

    elif request.method == 'POST':
        filename = request.form['filename']
        s3_key = f'encrypted/{filename}.enc'

        try:
            response = s3.get_object(Bucket=S3_BUCKET, Key=s3_key)
            encrypted_data = response['Body'].read()
            decrypted_data = cipher_suite.decrypt(encrypted_data)

            return send_file(
                BytesIO(decrypted_data),
                download_name=filename,
                as_attachment=True
            )
        except Exception as e:
            flash(f"Download or decryption failed: {str(e)}")
            return redirect(url_for('downloads'))

# User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash('Username already exists!')
            return redirect(url_for('register'))

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))

    return render_template('register.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.password == request.form['password']:
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials')
            return redirect(url_for('login'))

    return render_template('login.html')

# Index/Home
@app.route('/')
@login_required
def index():
    encrypted_files = []

    try:
        response = s3.list_objects_v2(Bucket=S3_BUCKET, Prefix='encrypted/')
        if 'Contents' in response:
            seen = set()
            for obj in response['Contents']:
                key = obj['Key']
                if key.endswith('.enc'):
                    filename = os.path.basename(key).replace('.enc', '')
                    if filename not in seen:
                        encrypted_files.append(filename)
                        seen.add(filename)
    except Exception as e:
        flash(f"Failed to load encrypted files: {str(e)}")

    return render_template('index.html', encrypted_files=encrypted_files)

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.')
    return redirect(url_for('login'))

@app.route('/home')
@login_required
def home():
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=8000, debug=True)
