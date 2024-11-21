from flask import Flask, render_template, send_from_directory, request, abort, Response
import os

app = Flask(__name__)

# Root directory for files
BASE_DIR = os.path.abspath("some_files")
# Allowed file extensions
ALLOWED_EXTENSIONS = {'.txt', '.pdf', '.jpg', '.png', '.docx', '.xlsx', '.pptx', '.zip', '.tar', '.gz', '.rar', '.7z'}


# Verify the safety of the path
def is_safe_path(base_path, target_path):
    base_path = os.path.realpath(base_path)
    target_path = os.path.realpath(target_path)
    return os.path.commonpath([base_path, target_path]) == base_path


# Check if the file extension is allowed
def is_allowed_file(filename):
    _, ext = os.path.splitext(filename)
    return ext.lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    # Get the requested path, default to the base directory
    requested_path = request.args.get('path', BASE_DIR)
    # Normalize and construct the full path
    current_path = os.path.realpath(os.path.join(BASE_DIR, requested_path.strip('/')))

    # Validate the path for security
    if not is_safe_path(BASE_DIR, current_path):
        abort(403)

    # List the files in the directory
    try:
        files = os.listdir(current_path)
    except FileNotFoundError:
        abort(404)

    # Sort the files by directories and then by name
    file_list = sorted(
        [{"name": f, "is_dir": os.path.isdir(os.path.join(current_path, f))} for f in files],
        key=lambda x: (not x["is_dir"], x["name"].lower())
    )

    # Get the relative path for the current directory
    relative_path = os.path.relpath(current_path, BASE_DIR) if current_path != BASE_DIR else '/'
    return render_template('index.html', files=file_list, current_path=relative_path, base_dir=BASE_DIR)



@app.route('/download')
def download_file():
    requested_path = request.args.get('path')

    # Check if the path is provided
    if not requested_path:
        abort(404)

    # Normalize and construct the full path
    full_path = os.path.realpath(os.path.join(BASE_DIR, requested_path.strip('/')))

    # Validate the path for security
    if not is_safe_path(BASE_DIR, full_path):
        abort(403)

    # Check if the file exists and is allowed
    if not os.path.isfile(full_path):
        abort(404)
    if not is_allowed_file(full_path):
        abort(403)

    # Stream the file to the client
    def generate_file(file_path):
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                yield chunk

    response = Response(generate_file(full_path), mimetype='application/octet-stream')
    response.headers['Content-Disposition'] = f'attachment; filename={os.path.basename(full_path)}'
    return response



@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403


if __name__ == '__main__':
    # Run the app on
    app.run(host="0.0.0.0", port=5000, debug=False)
