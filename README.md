# FastAPI Application Setup

This repository contains a simple FastAPI application. Follow these instructions to set up and run the application.

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Create a Virtual Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
# Install using requirements.txt
pip install -r requirements.txt
```

### 4. Create a .env File (Optional)

Create a `.env` file in the root directory with the following variables:

```
APP_NAME="Your FastAPI App"
DEBUG_MODE=True
DATABASE_URL="sqlite:///./test.db"
API_KEY="your-secret-api-key"
```

## Running the Application

```bash
python main.py
```

Or you can use uvicorn directly:

```bash
uvicorn main:app --reload
```

The application will be available at http://localhost:8000

## API Documentation

Once the application is running, you can access:
- Swagger UI documentation: http://localhost:8000/docs
- ReDoc documentation: http://localhost:8000/redoc

## API Endpoints

- `GET /`: Welcome message
- `GET /items`: List all items
- `GET /items/{item_id}`: Get a specific item
- `POST /items`: Create a new item
- `PUT /items/{item_id}`: Update an existing item
- `DELETE /items/{item_id}`: Delete an item 