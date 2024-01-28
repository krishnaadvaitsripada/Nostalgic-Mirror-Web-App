from flask import Flask, render_template, request, url_for, redirect, jsonify, send_file
from pymongo import MongoClient
from bson.objectid import ObjectId
import bson, pickle
import base64
from werkzeug.utils import secure_filename
import os
import io
from PIL import Image

app = Flask(__name__)

client = MongoClient('localhost', 27017)

album_db = client.album
album_collection = album_db.images

selfies_db = client.selfies
selfies_collection = selfies_db.images

users_db = client.users
users_collection = users_db.names

# Set up upload folder
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    # Fetch all images from MongoDB
    images = album_collection.find()
    return render_template('index.html', images=images)


def is_username_exist(username):
    # Check if the username exists in both collections
    user = users_collection.find_one({'username': username})
    return user is not None

def add_username(username):
    # Add the username to the users collection
    users_collection.insert_one({'username': username})

@app.route('/login', methods=['POST'])
def check_username():
    data = request.get_json()
    username = data.get('username')

    if is_username_exist(username):
        return jsonify({'message': 'Username exists'}), 200
    else:
        return jsonify({'message': 'Username does not exist'}), 409
    
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')

    if not username:
        return jsonify({'error': 'Username is required'}), 400

    if is_username_exist(username):
        return jsonify({'error': 'Username already exists'}), 409
    else:
        add_username(username)
        return jsonify({'message': 'Signup successful'}), 200

@app.route('/upload_album', methods=['POST'])
def upload_album(
    # file, username
    ):
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    username = request.form.get('username')

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
        album_collection.insert_one({'username': username, 'filename': filename, 'imageData': image_data_base64})

        return redirect(url_for('index'))

        return "File uploaded successfully"

    return redirect(url_for('index'))
    return "Invalid file type"

@app.route('/upload_selfie', methods=['POST'])
def upload_selfie(
    # file, username
    ):
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    username = request.form.get('username')

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
        selfies_collection.insert_one({'username': username, 'filename': filename, 'imageData': image_data_base64})

        return redirect(url_for('index'))

        return "File uploaded successfully"

    return redirect(url_for('index'))
    return "Invalid file type"

@app.route('/albums/<username>/images/<filename>', methods=['GET'])
def get_image_from_album(username, filename):
    image = album_collection.find_one({'username': username, 'filename': filename}, {'_id': 0})
    if image:
        image_data = base64.b64decode(image['imageData'])
        return send_file(io.BytesIO(image_data), mimetype='image/jpeg')  # Adjust mimetype accordingly
    else:
        return jsonify({"error": "Image not found"}), 404
    
@app.route('/albums/<username>/images', methods=['GET'])
def get_images_from_album(username):
    images = album_collection.find({'username': username}, {'_id': 0})
    image_names = {}
    i = 1
    for image in images:
        # image_names['Image Number ' + str(i)] = image['filename']

        # Assuming the image file is sent as binary data
        image_data = base64.b64decode(image['imageData'])

        # Open the image using Pillow
        image = Image.open(io.BytesIO(image_data))

        # Extract metadata
        metadata = {
            'format': image.format,
            'mode': image.mode,
            'size': image.size,
        }

        # Additional metadata if available
        if hasattr(image, '_getexif'):
            exif_data = image._getexif()
            if exif_data:
                metadata['exif'] = exif_data

        image_names['metadata' + str(i)] = metadata
        i += 1
    return jsonify(image_names)

@app.route('/selfies/<username>/images/<filename>', methods=['GET'])
def get_image_from_selfies(username, filename):
    image = selfies_collection.find_one({'username': username, 'filename': filename}, {'_id': 0})
    if image:
        image_data = base64.b64decode(image['imageData'])
        return send_file(io.BytesIO(image_data), mimetype='image/jpeg')  # Adjust mimetype accordingly
    else:
        return jsonify({"error": "Image not found"}), 404
    
@app.route('/selfies/<username>/images', methods=['GET'])
def get_images_from_selfies(username):
    images = selfies_collection.find({'username': username}, {'_id': 0})
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