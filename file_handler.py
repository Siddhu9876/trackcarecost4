import os

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def save_uploaded_file(file, user_id):
    """Save the uploaded file with user ID for tracking."""
    filename = f"{user_id}_{file.filename}"
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    
    with open(file_path, "wb") as f:
        f.write(file.read())

    return filename

def get_uploaded_file(filename, user_id):
    """Retrieve a file (for downloading)."""
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        return file_path
    else:
        return None
