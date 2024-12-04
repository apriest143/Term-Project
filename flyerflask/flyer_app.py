from flask import Flask, request, render_template, redirect, url_for, session, g, current_app
import datetime
import os
from main import image_upload, analyze_text_with_ai
from werkzeug.utils import secure_filename
from models import db, User, Event, Image
from functools import wraps
from dotenv import load_dotenv
import logging
from ics import Calendar, Event as ICSEvent
from flask import send_file
import io

load_dotenv()
app = Flask(__name__)
app.secret_key = os.urandom(32)

# SQLite Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the app
db.init_app(app)

# Create tables - this replaces migrations
with app.app_context():
    db.create_all()

# Configure upload folder with absolute path
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    current_app.logger.debug(f"Created upload directory: {UPLOAD_FOLDER}")

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Function to check file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Home route
@app.route('/', methods=['GET', 'POST'])
def index():
    if g.user:
        return redirect(url_for('upload_image'))
    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username=username)
            db.session.add(user)
            db.session.commit()
        session['user_id'] = user.id
        return redirect(url_for('upload_image'))
    return render_template('index.html')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@app.before_request
def load_user():
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])
    else:
        g.user = None

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_image():
    if request.method == 'POST':
        try:
            if 'file' not in request.files:
                current_app.logger.debug("No file part in request")
                return "No file part", 400
            file = request.files['file']
            if file.filename == '':
                current_app.logger.debug("No selected file")
                return "No selected file", 400
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                current_app.logger.debug(f"File saved to {file_path}")

                # Save image record with user association
                image = Image(filename=filename, user_id=g.user.id)
                db.session.add(image)
                db.session.commit()

                # Process extracted text and create event
                text = image_upload(file_path)
                event_data = analyze_text_with_ai(text)
                current_app.logger.debug(f"Event data: {event_data}")

                # Create event even if data is incomplete
                event = Event(
                    name=event_data.get('name') or 'Unnamed Event',
                    date=event_data.get('date'),
                    time=event_data.get('time'),
                    location=event_data.get('location') or 'Unknown Location',
                    description=event_data.get('description') or 'No description provided.',
                    user_id=g.user.id
                )
                db.session.add(event)
                db.session.commit()
                current_app.logger.debug(f"Event created: {event.name}")

                return redirect(url_for('events'))
            else:
                current_app.logger.debug("File type not allowed")
                return "File type not allowed", 400

        except Exception as e:
            current_app.logger.error(f"Error in upload_image: {e}")
            db.session.rollback()
            return "An error occurred during upload.", 500

    return render_template('upload.html', user=g.user)

@app.route('/events')
@login_required
def events():
    user_events = Event.query.filter_by(user_id=g.user.id).all()
    return render_template('events.html', user=g.user, events=user_events)

# Calendar route
@app.route('/calendar')
@login_required
def calendar():
    user = g.user
    today = datetime.date.today()
    first_day = today.replace(day=1)
    last_day = (first_day + datetime.timedelta(days=32)).replace(day=1) - datetime.timedelta(days=1)
    start_date = first_day - datetime.timedelta(days=first_day.weekday())

    calendar_weeks = []
    current_week = []
    current_date = start_date

    while current_date <= last_day:
        day_events = [event for event in user.events if event.date == current_date]

        day_info = {
            'date': current_date,
            'events': day_events,
            'is_current_month': current_date.month == today.month
        }
        current_week.append(day_info)

        if len(current_week) == 7:
            calendar_weeks.append(current_week)
            current_week = []
        current_date += datetime.timedelta(days=1)

    if current_week:
        calendar_weeks.append(current_week)

    month_name = today.strftime('%B %Y')
    return render_template('calendar.html',
                           user=user,
                           weeks=calendar_weeks,
                           month_name=month_name,
                           today=today)

@app.route('/view_uploads')
@login_required
def view_uploads():
    user_images = Image.query.filter_by(user_id=g.user.id).all()
    return render_template('view_uploads.html', user=g.user, images=user_images)


@app.route('/export_ics')
@login_required
def export_ics():
    user_events = Event.query.filter_by(user_id=g.user.id).all()
    c = Calendar()
    
    for event in user_events:
        e = ICSEvent()
        e.name = event.name or 'Unnamed Event'
        
        # Handle date and time
        if event.date and event.time:
            dt = datetime.datetime.combine(event.date, event.time)
            e.begin = dt
            e.end = dt + datetime.timedelta(hours=1)  # Default 1 hour duration
        elif event.date:
            e.begin = event.date
            e.end = event.date + datetime.timedelta(hours=24)  # All day event
            
        e.location = event.location or 'No location specified'
        e.description = event.description or 'No description available'
        c.events.add(e)
    
    # Create ICS file in memory
    calendar_str = str(c)
    
    # Return as downloadable file
    return send_file(
        io.BytesIO(calendar_str.encode()),
        mimetype='text/calendar',
        as_attachment=True,
        download_name=f'{g.user.username}_events.ics'
    )

if __name__ == '__main__':
    app.run(debug=True)
