import json

from flask import Flask, request, jsonify
import create_bundle_sorter as createBundleSorter
import create_word_doc as createDoc
import xmltodict
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    return response

@app.route('/login', methods=['POST'])
def validateLogin():
    print(request);
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if username == 'admin' and password == 'password':
        return jsonify({'status':'1'},
            {'message': 'Login Successful'})
    else:
        return jsonify({'status':'0'},
            {'message': 'Login Unsuccessful'})

@app.route('/readBundle', methods=['POST'])
def readXMLFileContent():
    try:
        file_content = request.json.get('fileContent')
        xml_data = xmltodict.parse(file_content)
        # entities = xml_data["root"]["bundle"]["entities"]

        createBundleSorter.df = xml_data
        createBundleSorter.extractBundleData()
        component_list=createBundleSorter.list_of_component
        return {'componentList': component_list}
    except Exception as e:
        return {'message': str(e)}

@app.route('/generateDocument', methods=['POST'])
def generateDocument():
    try:
        file_content = request.json.get('fileContent')
        selected_component=request.json.get('checkedComponents')
        bundle_data = xmltodict.parse(file_content)
        #component_checked=xmltodict.parse(checked_component)
        createDoc.createDocument(bundle_data,selected_component)
        return {'message': 'Document generated successfully'}
    except Exception as e:
        return {'message': str(e)}


if __name__ == '__main__':
    app.run(debug=True)
