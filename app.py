from flask import Flask, request, render_template
from model import get_prediction_label
import os
# flask: Flask is used to create the application instance, 
# request handles incoming requests, and render_template is used to render HTML templates
# model: class created where get prediction models handles the logic of generating predictions from input
# os: use operationg system functions like reading or writing file to the system
app = Flask(__name__)
# creates instance of application app = flask
@app.route('/', methods=['GET', 'POST']) #Creates route support for both methods i.e. GET and POST

def upload_file(): #new function
    if request.method == 'POST': # Checks if the request is POST, clint is submitting data to the server 
        file = request.files['file'] # retrives the file from the submitted data request.file
        if file: # checks if file was uploaded
            file_path = os.path.join('uploads', file.filename) # constrctus a file path, the 'os.path.joiun' ensures correct path seperator is used for the os
            file.save(file_path) # save the uploaded file
            with open(file_path, 'rb') as f: # opens the file, rb means binary read mode
                image_bytes = f.read() # reads the image
                prediction_label = get_prediction_label(image_bytes) # put prediction on the image
            return render_template('result.html', prediction=prediction_label) # put the results of prediction into results.html
        else:
            return render_template('index.html', error="No file uploaded")
    return render_template('index.html') # if the method is GET or no files is uploaded it renders an HTML into index.html
if __name__ == '__main__':
    app.run(debug=True)