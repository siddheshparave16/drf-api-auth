### Telegram User API Project ###

**Created by Siddhesh Parave**

>>>> **Note**: This project was developed on **Windows Subsystem for Linux (WSL)**. 

## 📂 Project Structure

drf-api-auth/ # Repository root
├── api/ # Django project root
│ ├── api/ # Main project configuration
│ ├── securegate/ # Authentication & Telegram integration
│ │ ├── models.py # User models
│ │ └── views.py # Authentication logic
│ ├── teleapi/ # API endpoints
│ │ ├── serializers.py
│ │ └── urls.py
│ └── manage.py # Django CLI
├── .gitignore
├── API_DOCS.md # Postman/cURL documentation
├── poetry.lock # Dependency locks
└── pyproject.toml # Project configuration



## 🚀 Quick Setup
1. **Clone and Enter the Repository**
   ```bash

    git clone https://github.com/siddheshparave16/drf-api-auth.git
    cd drf-api-auth/api  # Note the /api subdirectory

2. Install Dependencies
    ``` bash
    poetry install  # Install all dependencies
    source .venv/bin/activate    # Activate virtual environment


## Run Services

# Terminal 1: Django
    cd api 
    python manage.py runserver

# Terminal 2: Celery
    celery -A api worker -l info

# Terminal 3: Telegram Bot
    python manage.py runbot



## Access API at: 
# http://localhost:8000/api/v1/

🔐 Authentication Flows
JWT Tokens: /api/token-jwt/

DRF Tokens: /api-token-auth/

Telegram Bot: Handled in securegate/

📚 Documentation
Interactive: Postman Collection

Endpoint details: API_DOCS.md


## 💡 Pro Tips:

1. Always run commands from /api folder after cloning
2. Use poetry add package for new dependencies
3. Check .gitignore for excluded files (like .venv)


## 🛠️ Environment Variable Setup

Create a .env file in the project root with the following contents:

# database
DB_NAME=""
DB_USER=""
DB_PASSWORD=""
DB_HOST=127.0.0.1  # Or localhost for windows , we have set this 127.0.0.1 for wsl
DB_PORT=5432

# smpt email credentials
EMAIL_HOST_USER=""
EMAIL_HOST_PASSWORD=""

# Telegram bot token
TELEGRAM_BOT_TOKEN=""


## ✨ Features of This Project

1. User Authentication:
    - User Registration, Login, and Logout functionalities.

2. Celery setup:
    - User registration tasks integrated with Redis as the broker to send emails.

3. Telegram Bot Integration:
    - On receiving the /start command, the Telegram Bot stores user data in the TelegramUser model.

4. API endpoints for TelegramUser:
    - RESTful APIs to manage Telegram users effectively.

