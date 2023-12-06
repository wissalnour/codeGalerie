from flask import Flask, render_template, request, redirect, url_for
from azure.storage.blob import BlobServiceClient
import os
from datetime import datetime
import logging


app = Flask(_name_)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Replace 'YOUR_AZURE_STORAGE_CONNECTION_STRING' with your actual Azure Storage connection string
app.config['AZURE_STORAGE_CONNECTION_STRING'] = 'DefaultEndpointsProtocol=https;AccountName=stockgalerie;AccountKey=j+aL4fpCCjaug1yngJcqXibkLQyU+oNe/NbV2j/PQH/ENHwghJCPSo9RIRgfBmdjNAtxHuGYpEQx+ASt7dod+g==;EndpointSuffix=core.windows.net'

# Replace 'uploads' with the name of the container you created in Azure Storage
app.config['CONTAINER_NAME'] = 'conteneur'

def upload_to_blob(file):
    blob_service_client = BlobServiceClient.from_connection_string(app.config['AZURE_STORAGE_CONNECTION_STRING'])
    container_client = blob_service_client.get_container_client(app.config['CONTAINER_NAME'])

    with open(file, 'rb') as data:
        container_client.upload_blob(name=os.path.basename(file), data=data)

@app.route('/')
@app.route('/')
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Add your authentication logic here
        # Example: Check if the username and password are correct
        if username == 'your_username' and password == 'your_password':
            # Successful login, you might want to redirect to the dashboard
            logging.info('Successful login for user: %s', username)
            return redirect(url_for('dashboard'))
        else:
            # Failed login, you might want to display an error message
            error_message = 'Invalid credentials. Please try again.'
            logging.warning('Failed login attempt for user: %s', username)
            return render_template('login.html', error_message=error_message)
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    blob_service_client = BlobServiceClient.from_connection_string(app.config['AZURE_STORAGE_CONNECTION_STRING'])
    container_client = blob_service_client.get_container_client(app.config['CONTAINER_NAME'])
    blobs = container_client.list_blobs()

    images = [{'filename': blob.name, 'upload_date': blob.creation_time} for blob in blobs]
    return render_template('dashboard.html', images=images)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(url_for('dashboard'))
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('dashboard'))
   
    if file:
        # Local storage (optional, depending on your needs)
        local_filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(local_filename)

        # Upload to Azure Blob Storage
        upload_to_blob(local_filename)

        return redirect(url_for('dashboard'))

if _name_ == '_main_':
    app.run(debug=True)