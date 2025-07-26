<h1 align="center">🔐 Secure Cloud Storage</h1>
<p align="center">
  A Flask-based web application for secure, encrypted file storage and retrieval.<br>
  <em>Protect your files with encryption. Store and retrieve them with confidence.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10-blue.svg" />
  <img src="https://img.shields.io/badge/Flask-2.x-orange.svg" />
  <img src="https://img.shields.io/badge/Status-Active-brightgreen.svg" />
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" />
</p>

---

## 📽️ Demo

<p align="center">
  <a href="demo/SecureCloudDemo.mp4">
    <img src="demo/secureCloudDemo.mp4" alt="Watch Demo" width="200"/>
  </a>
</p>

> 🔹 Click the play button above to watch the screen recording demo.
---

## 🧩 Overview

**Secure Cloud Storage** is a secure file management platform that lets users:

- 🔒 Upload and encrypt files
- ⬇️ Download encrypted files securely
- 🧹 Delete unwanted files
- 🔐 Register and login securely
- 📦 View and manage stored files via a simple dashboard

All operations happen locally unless hosted externally.

---

## 🌐 Technologies Used

| Layer         | Technology              |
|---------------|--------------------------|
| 👨‍💻 Frontend     | HTML5, CSS3, JavaScript      |
| ⚙️ Backend      | Python 3, Flask            |
| 🗃️ Database     | SQLite (via SQLAlchemy)     |
| 🔐 Encryption   | Fernet (Cryptography lib)   |
| 🎥 Demo Format | `.mp4` Screen Recording     |

---

## 🛠️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/secure-cloud-storage.git
cd secure-cloud-storage
````

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate      # For Linux/macOS
venv\Scripts\activate         # For Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the App

```bash
python app.py
```

Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

## 📁 Project Structure

```
secure-cloud-storage/
│
├── app.py                 # Main Flask application
├── templates/             # HTML templates (Jinja2)
├── static/                # CSS and JavaScript
├── uploads/               # Encrypted user file storage
├── demo/                  # Screen recording demo (mp4)
├── requirements.txt       # Required Python packages
└── README.md              # This file
```

---

## 🔐 Security Features

* **User Authentication**: Secure login & session management
* **File Encryption**: Uses Fernet symmetric encryption
* **Access Control**: User-specific file handling
* **Safe Storage**: Files saved in encrypted format only

---

## 💡 Future Improvements

* 🗂️ Folder-wise uploads
* ⛅ Cloud Integration (Google Drive, AWS S3, etc.)
* 🔍 Search functionality
* 🔑 Two-Factor Authentication

---

<p align="center"><em>“Your data, your control.”</em></p>
```

---
