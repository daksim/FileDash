# FileDash

**FileDash** is a lightweight web application for browsing and downloading files from a specified directory. 

## Getting Started

### Prerequisites

- Python 3.7 or above

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/FileDash.git
   cd FileDash
   ```

1. Install required dependencies:

   ```bash
   pip install flask
   ```

2. Prepare your file directory:

   - Place your files inside the `some_files/` directory (or any directory you define in the `BASE_DIR` variable in `server.py`).

### Running the Application

1. Start the server:

   ```bash
   python server.py
   ```

2. Open your browser and navigate to:

   ```arduino
   http://127.0.0.1:5000
   ```

3. For external access, use your server's IP address and ensure port `5000` is open:

   ```arduino
   http://<your-server-ip>:5000
   ```

### Directory Structure

```
csharpCopy codeproject/
├── server.py           # Main application script
├── templates/          # HTML templates
│   ├── index.html      # File browser UI
│   ├── 404.html        # 404 error page
│   ├── 403.html        # 403 error page
├── static/             # Static files (e.g., CSS, images)
├── some_files/         # Directory for storing files
```