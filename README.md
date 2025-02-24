# Django Chat app

## Overview
This project is realization of a simple chat task
## Features
- RESTful APIs for managing thread and messages.
---

## Getting Started

### Prerequisites
Ensure you have Python 3.10+ installed on your system.

### Installation

Follow these steps to install and run the application on Windows and macOS.

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Nazar04u/SimpleChatDjango
   cd SimpleChatDjango
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   
   #MacOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` File**
   Create a `.env` file in the project root and add your `SECRET_KEY`:
   ```plaintext
   SECRET_KEY=<secret_key>
   ```

5. **Apply Migrations**
   Apply the generated migration to create the database:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
6. **Load Test Data**
   ```bash
   python manage.py loaddata dump.json
   ```
7. **Run the Application**
   ```bash
   python manage.py runserver
   ```

8. **Access API Documentation**
   Open your browser and navigate to [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger) to explore the API endpoints.

---

### Notes

- Ensure you have `Python 3.10` or newer installed on your system.
- If you encounter any issues with permissions, try running commands with `sudo` (macOS) or as Administrator (Windows).
- To stop the application, press `Ctrl+C` in the terminal where the server is running.


## Usage

### 1. Authorization
First of all, authorize user with credentials(for example, username-user1, password - 111). Then copy your access token 
and go to Authorize button at the top and enter ```Bearer access_token```. it is needed for jwt authentication.

### 2. Now be free to test it
