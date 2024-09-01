from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from gridfs import GridFS
import os
from secrets import token_hex
from PIL import Image
import pytesseract
from bson import ObjectId
from datetime import datetime
import io
from pdf2image import convert_from_bytes
import config

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

client = MongoClient('mongodb+srv://sohamnsharma:rdcv4c75@sih.cgxnw.mongodb.net/?retryWrites=true&w=majority&appName=sih')
db = client['sih']
users = db['users']
documents = db['documents']
fs = GridFS(db)

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def perform_ocr(file_data, file_extension):
    try:
        if file_extension == 'pdf':
            # Convert PDF to images
            images = convert_from_bytes(file_data)
            text = ""
            for image in images:
                text += pytesseract.image_to_string(image)
        else:
            # For image files
            image = Image.open(io.BytesIO(file_data))
            text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print(f"OCR Error: {str(e)}")
        return ""

@app.route('/')
def index():
    if 'username' in session:
        user_documents = list(documents.find({"owner": session['username']}))
        return render_template('dashboard.html', documents=user_documents)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.find_one({"username": username})
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            return redirect(url_for('index'))
        return 'Invalid username or password'
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        if users.find_one({"username": username}):
            return 'Username already exists'
        users.insert_one({"username": username, "password": password})
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/upload', methods=['POST'])
def upload_document():
    if 'username' not in session:
        return redirect(url_for('login'))

    document_type = request.form['document_type']
    if document_type == 'other':
        document_type = request.form['other_type']
    
    document_file = request.files['document']
    
    if document_file and allowed_file(document_file.filename):
        file_extension = document_file.filename.rsplit('.', 1)[1].lower()
        file_data = document_file.read()
        
        # Store file in GridFS
        file_id = fs.put(file_data, filename=document_file.filename)
        
        # Perform OCR
        ocr_text = perform_ocr(file_data, file_extension)
        
        # Store document information in MongoDB
        document_id = documents.insert_one({
            'type': document_type,
            'status': 'Pending',
            'date_uploaded': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'file_id': file_id,
            'owner': session['username'],
            'ocr_text': ocr_text,
            'filename': document_file.filename
        }).inserted_id
        
        return redirect(url_for('index'))
    
    return 'Invalid file type', 400

@app.route('/view/<file_id>')
def view_document(file_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    document = documents.find_one({"file_id": ObjectId(file_id), "owner": session['username']})
    if document:
        return render_template('view_document.html', document=document)
    return 'Document not found', 404

@app.route('/download/<file_id>')
def download_document(file_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    document = documents.find_one({"file_id": ObjectId(file_id), "owner": session['username']})
    if document:
        file_data = fs.get(ObjectId(file_id))
        return send_file(
            io.BytesIO(file_data.read()),
            mimetype='application/octet-stream',
            as_attachment=True,
            download_name=document['filename']
        )
    return 'Document not found', 404

@app.route('/api/documents')
def get_documents():
    if 'username' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 5))
    
    skip = (page - 1) * per_page
    
    user_documents = list(documents.find({"owner": session['username']}).skip(skip).limit(per_page))
    
    # Convert ObjectId to string for JSON serialization
    for doc in user_documents:
        doc['_id'] = str(doc['_id'])
        doc['file_id'] = str(doc['file_id'])
    
    total_documents = documents.count_documents({"owner": session['username']})
    total_pages = (total_documents + per_page - 1) // per_page
    
    return jsonify({
        "documents": user_documents,
        "total_pages": total_pages,
        "current_page": page
    })

@app.route('/update_ocr/<file_id>', methods=['POST'])
def update_ocr(file_id):
    if 'username' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    document = documents.find_one({"file_id": ObjectId(file_id), "owner": session['username']})
    if document:
        file_data = fs.get(ObjectId(file_id)).read()
        file_extension = document['filename'].rsplit('.', 1)[1].lower()
        
        # Perform OCR
        ocr_text = perform_ocr(file_data, file_extension)
        
        # Update OCR text in the database
        documents.update_one(
            {"_id": document['_id']},
            {"$set": {"ocr_text": ocr_text}}
        )
        
        return jsonify({"message": "OCR updated successfully"}), 200
    
    return jsonify({"error": "Document not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)