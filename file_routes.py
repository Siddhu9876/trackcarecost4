from flask import Blueprint, request, jsonify
from file_handler import save_uploaded_file, get_uploaded_file
from user_activity import get_user_activity

file_routes = Blueprint("file_routes", __name__)  # Creating a Blueprint

@file_routes.route("/upload", methods=["POST"])
def upload_file():
    """Handles file uploads."""
    user_id = 1  # Static user_id for testing
    
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filename = save_uploaded_file(file, user_id)
    return jsonify({"message": "File uploaded successfully", "filename": filename})

@file_routes.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    """Handles file downloads."""
    user_id = 1  # Static user_id for testing
    return get_uploaded_file(filename, user_id)

@file_routes.route("/activity", methods=["GET"])
def user_activity():
    user_id = request.args.get("user_id")
    activity = get_user_activity(user_id)  # Fetch user activity

    if not activity:  # Ensure JSON response even if empty
        return jsonify({"message": "No activity found"}), 200

    return jsonify(activity)


    


