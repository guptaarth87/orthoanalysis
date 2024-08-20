from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from PIL import Image
import io
import base64
from bson import ObjectId
from flask import jsonify

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS

# MongoDB client setup
client = MongoClient('mongodb+srv://arth1234samepass:arth1234@cluster0.pdgx6ns.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')  # Update with your MongoDB URI if needed
db = client['Xray']  # Database name
users_collection = db['User']  # Collection for user authentication
xraydata_collection = db['xraydata']  # Collection for storing images

# Helper function to process images (replace this with your actual image processing code)
def process_image(input_image):
    # Convert image to grayscale as an example of processing
    output_image = input_image.convert("L")
    return output_image

@app.route('/', methods=['GET'])
def index():
    return jsonify({'status': 'success', 'message': 'app running successfully'}), 201

@app.route('/getusers', methods=['GET'])
def getuser():
    try:
        users = users_collection.find()
        user_list = []
        
        for user in users:
            user['_id'] = str(user['_id'])  # Convert ObjectId to string
            user_list.append(user)
        
        return jsonify({'status': 'success', 'data': user_list}), 200
    except Exception as e:
        return jsonify({'status': 'fail', 'message': str(e)}), 500
    
# Signup route
@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.json
        name_ = data['name_']
        phoneNo = data['phoneNo']
        email = data['email']
        password = data['password']

        # Check if user already exists
        if users_collection.find_one({'email': email}):
            print(users_collection.find_one({'email': email}))
            return jsonify({'status': 'fail', 'message': 'User already exists'}), 400

        # Hash the password and store the user
        hashed_password = generate_password_hash(password, method='sha256')
        users_collection.insert_one({'name_':name_ ,'phoneNo':phoneNo , 'email': email, 'password': hashed_password})
        return jsonify({'status': 'success', 'message': 'User created successfully'}), 201

    except Exception as e:
        return jsonify({'status': 'fail', 'message': str(e)}), 500

# Signin route

@app.route('/signin', methods=['POST'])
def signin():
    try:
        data = request.json
        email = data['email']
        password = data['password']
        print(email)
        print(password)
        user = users_collection.find_one({'email': email})
        if user and check_password_hash(user['password'], password):
            return jsonify({'status': 'success', 'message': 'Logged in successfully'}), 200
        else:
            return jsonify({'status': 'fail', 'message': 'Invalid email or password'}), 401

    except Exception as e:
        return jsonify({'status': 'fail', 'message': str(e)}), 500

# Image processing route
def process_image(input_image):
    # Convert image to grayscale
    output_image = input_image.convert("L")
    return output_image

@app.route('/process-image', methods=['POST'])
def process_image_route():
    
    try:
        # Extract email and image from the request
        email = request.form['email']
        input_image_file = request.files['image']
        print(email)
        # Load the input image using PIL
        input_image = Image.open(input_image_file)

        # Process the image using the process_image function
        output_image = process_image(input_image)

        # Save input and output images as bytes in memory
        input_image_bytes = io.BytesIO()
        output_image_bytes = io.BytesIO()
        input_image.save(input_image_bytes, format='PNG')
        output_image.save(output_image_bytes, format='PNG')

        # Encode images to base64 strings
        input_image_str = base64.b64encode(input_image_bytes.getvalue()).decode('utf-8')
        output_image_str = base64.b64encode(output_image_bytes.getvalue()).decode('utf-8')

        # Store the images and email in MongoDB
        xraydata_collection.insert_one({
            'email': email,
            'input_image': input_image_str,
            'output_image': output_image_str
        })

        # Prepare additional data (if any)
        dataArray = {}

        # Return the processed image and status
        return jsonify({'status': 'success', 'output_image': output_image_str, 'data': dataArray}), 200

    except Exception as e:
        return jsonify({'status': 'fail', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
