# Energy System planning
The Energy System Planning project is a full-stack web application designed to educate students on
energy distribution, resource management, and optimization through an interactive simulation.
Developed from scratch using Django (backend) and Vue.js (frontend), this web-based platform
enables students to modify energy production from various sources, observe real-time system
efficiency changes, and analyze impacts using graph-based visualizations, matrices, and cost
analysis charts

This guide walks you through setting up the project with **Django** as the backend and **Vue.js** as the frontend. 

## Prerequisites

Before starting, ensure you have the following installed:
- Python 3.12.7
- Node.js and npm
- Git

## Setup Instructions

### Step 1: Clone the Repository

```bash
git clone <repository_url>
cd <path to cloned repo>
```

### Step 2: Set Up the Backend (Django)

1. **Create and Activate the Virtual Environment**
    ```bash
    #Create a virtual environment
    python -m venv venv 

    # Activate venv on macOS/Linux
    source venv/bin/activate

    # Activate venv on Windows
    venv\Scripts\activate
    ```

2. **Install Python Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3. **Apply Migrations**
    ```bash
    python manage.py migrate
    ```

4. **Run the Django Development Server**
    ```bash
    python manage.py runserver
    ```
### You can confirm that the backend is running locally at the link generated (http://127.0.0.1:8000/)

### Step 3: Set Up the Frontend (Vue.js)

1. **Navigate to the Frontend Directory**
    ```bash
    cd frontend
    ```

2. **Install Frontend Dependencies**
    ```bash
    npm install
    ```

3. **Run the Vue.js Development Server**
    ```bash
    npm run dev
    ```

### Now the frontend application can be accesed at the local link generated (http://localhost:5173/)