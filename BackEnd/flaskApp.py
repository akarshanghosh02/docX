from flask import *
from flask import Flask, request
from flask import Flask, render_template, request, redirect, url_for, current_app
from flask import session
import readCSV as readCSV
import create_bundle_sorter as createBundleSorter
import create_word_doc as createDoc
import os

df = readCSV.readCSVFiles()
app = Flask(__name__)

# Add app configurations
app.config['UPLOAD_PATH'] = 'uploads'
app.config['UPLOAD_EXTENSIONS'] = ['.xml']
app.config["CACHE_TYPE"] = "null"
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


# Shows main page of app
@app.route('/', methods=['GET', 'POST'])
def upload():
    # print(request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr))
    return render_template("index.html")


# Runs main logic
@app.route('/download', methods=['POST'])
def run_logic():
    # Checks the requested method
    if request.method == 'POST':
        f = request.files['file']
        # Check if any file uploaded
        if f.filename != '':
            file_ext = os.path.splitext(f.filename)[1]
            # Check if files extension is XML
            if file_ext not in current_app.config['UPLOAD_EXTENSIONS']:
                return redirect(url_for('upload'))
            # Save file to given path
            file = (os.path.join(app.config['UPLOAD_PATH'], f.filename))
            f.save(file)
        else:
            return redirect(url_for('upload'))
        # f.save(f.filename)
    print("before bundle sort " + f.filename)
    createBundleSorter.extractBundleData(f.filename)
    print("after bundle sort")
    createDoc.createDocument()

    session['ip'] = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    file = (os.path.join(app.config['UPLOAD_PATH'], f.filename))
    # Remove file from directory
    os.remove(file)
    return render_template("download.html")


# Show document download page
@app.route('/download')
def download_file():
    path = df.loc['outputFileName'].value
    session.pop('ip', None)
    return send_file(path, as_attachment=True, cache_timeout=0)


if __name__ == '__main__':
    app.run(threaded=True, debug=True)
