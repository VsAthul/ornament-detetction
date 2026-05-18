# Ornament Detection

A simple AI-powered ornament detection project built with Python.  
The application allows users to upload an image, detect ornaments from the image, and store the detected results in a database.

## Features

- Upload image support
- Detect ornaments from uploaded images
- Store detection results in SQLite database
- Simple web interface using HTML templates
- Modular project structure

## Project Structure

```bash
ornament detection/
│── main.py
│── graph.py
│── database.py
│── schemas.py
│── detection.db
│── pyproject.toml
│── README.md
│
├── nodes/
│   ├── load_image.py
│   ├── detect_items.py
│   └── save_to_db.py
│
├── templates/
│   └── index.html
│
└── static/
```

## Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd "ornament detection"
```

### 2. Create virtual environment

```bash
python -m venv .venv
```

### 3. Activate virtual environment

#### Windows

```bash
.venv\Scripts\activate
```

#### Linux / Mac

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

## Run the Project

```bash
python main.py
```

The server will start locally.

## Image Upload Example

Example HTML form for uploading an image:

```html
<form action="/upload" method="POST" enctype="multipart/form-data">
    <input type="file" name="image" accept="image/*" required>
    <button type="submit">Upload Image</button>
</form>
```

## Technologies Used

- Python
- FastAPI / Flask
- SQLite
- HTML
- AI Image Detection

## Future Improvements

- Add real-time detection
- Improve UI design
- Add user authentication
- Support multiple image uploads

## License

This project is for educational purposes.