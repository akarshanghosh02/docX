import readCSV
import create_bundle_sorter as createBundleSorter
import create_word_doc as createDoc
import main as login
from flask import Flask, request, jsonify
import os

# get list from readCSVFiles() function
df = readCSV.readCSVFiles()
app = Flask(__name__)
def background_task():
    with app.app_context():
        # Now use request, session, etc. safely
        print(request.url) #example usage, adjust to your code.
# Main program execution starts here where first call goes to bundle sorter and second to crate word document
# if __name__ == '__main__':
#     login.validateLogin()
#     createBundleSorter.extractBundleData()
#     createDoc.createDocument()

    # os.system("start " + df.loc['outputFileName'].value)



