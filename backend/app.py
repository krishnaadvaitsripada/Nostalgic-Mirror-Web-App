from flask import Flask, render_template, request, url_for, redirect, jsonify, send_file
from pymongo import MongoClient
from bson.objectid import ObjectId
import bson, pickle
import base64
from werkzeug.utils import secure_filename
import os
import io

app = Flask(__name__)

client = MongoClient('localhost', 27017)

db = client.flask_db
collection = db.images

# Set up upload folder
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    # Fetch all images from MongoDB
    images = collection.find()
    return render_template('index.html', images=images)

@app.route('/upload_album', methods=['POST'])
def upload_album():
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # file.save(file_path)

        # Convert image data to Base64
        with file.stream as image_file:
            image_data_bytes = image_file.read()
            image_data_base64 = base64.b64encode(image_data_bytes).decode('utf-8')

        # Save file info to MongoDB
        collection.insert_one({'filename': filename, 'imageData': image_data_base64})

        return redirect(url_for('index'))

        return "File uploaded successfully"

    return redirect(url_for('index'))
    return "Invalid file type"

@app.route('/images/<filename>', methods=['GET'])
def get_image(filename):
    image = collection.find_one({'filename': filename}, {'_id': 0})
    if image:
        image_data = base64.b64decode(image['imageData'])
        return send_file(io.BytesIO(image_data), mimetype='image/jpeg')  # Adjust mimetype accordingly
    else:
        return jsonify({"error": "Image not found"}), 404
    
@app.route('/images', methods=['GET'])
def get_images():
    images = collection.find({}, {'_id': 0})
    image_names = {}
    i = 1
    for image in images:
        image_names['Image Number ' + str(i)] = image['filename']
        i += 1
    return jsonify(image_names)

# @app.route('/', methods=('GET', 'POST'))
# def index():
#     if request.method=='POST':
#         content = request.form['content']
#         degree = request.form['degree']
#         todos.insert_one({'content': content, 'degree': degree})
#         return redirect(url_for('index'))

#     all_todos = todos.find()
#     return render_template('index.html', todos=all_todos)

# @app.post('/<id>/delete/')
# def delete(id):
#     todos.delete_one({"_id": ObjectId(id)})
#     return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
