#!/usr/bin/python3
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from database.mmm import create_connection, execute_query, execute_read_query, iscore, get_user_data_helper

app = Flask(__name__)
CORS(app)

@app.route('/get_iscore', methods=['GET'])
def get_iscore():

    user = request.args.get('user')
    if user is None:
        return jsonify({"error": "User parameter is required"}), 400
    return jsonify(iscore(user))

@app.route("/get_user_data", methods=["GET"])
def get_user_data():
    user = request.args.get('user')
    if user is None:
        return jsonify({"error": "User parameter is required"}), 400

    data = get_user_data_helper(user)
    return jsonify(data)

if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    app.run(host='0.0.0.0', port=port, debug=False)