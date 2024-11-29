from flask import Flask, request, render_template, redirect, url_for
import datetime
import os

app = Flask(__name__)

# Configure upload folder if it does not already exist 
UPLOAD_FOLDER = 'flyerflask/static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Function to check file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Home route
@app.route('/')

def index():
    return render_template('index.html')

# Image upload route
@app.route('/upload', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        # Check if the POST request has the file part
        if 'file' not in request.files:
            return "No file part", 400
        file = request.files['file']
        # If user does not select a file
        if file.filename == '':
            return "No selected file", 400
        if file and allowed_file(file.filename):
            # Save file to the upload folder
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            return f"File uploaded successfully: {file_path}"
    return render_template('upload.html')


#Allow user to 
@app.route('/view_uploads')
def view_uploads():
    # List all files in the upload folder
    uploaded_files = os.listdir(app.config['UPLOAD_FOLDER'])
    uploaded_images = [file for file in uploaded_files if allowed_file(file)]  # Filter valid image files
    return render_template('view_uploads.html', images=uploaded_images)


#Calendar route. finds todays date, and populates the next 4 weeks accordingly
@app.route('/calendar')
def calendar():
    # Get today's date
    today = datetime.date.today()

    # Find the start of the current week (Sunday)
    start_of_week = today - datetime.timedelta(days=today.weekday() + 1)  # Sunday of the current week

    # Create a list of dates for the next 4 weeks
    dates = []
    for week in range(4):  # We want 4 weeks worth of dates
        week_dates = []
        for day in range(7):  # 7 days in a week (Sun-Sat)
            date = start_of_week + datetime.timedelta(days=week * 7 + day)
            week_dates.append(date)
        dates.append(week_dates)

    # Pass the dates to the template
    return render_template('calendar.html', dates=dates)


if __name__ == '__main__':
    app.run(debug=True)
