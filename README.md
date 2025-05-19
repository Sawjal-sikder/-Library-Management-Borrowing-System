# Library Management System

## Project Instructions

### Prerequisites
- Python 3.x installed
- Required libraries (see `requirements.txt`)

### Setup

1. **Clone the repository:**
      ```
      git clone https://github.com/Sawjal-sikder/Library-Management-Borrowing-System.git
      ```

2. **Install dependencies:**
create environment
      ``` 
      python -m venv env
      cd dir
      ```
install all dependencies
      ```
      pip install -r requirements.txt
      ```

3. **Configure the database:**

        ```
        python manage.py makemigrations
        python manage.py migrate
        python manage.py createsuperuser
        ```

4. **Run the application:**
      ```
      python manage.py runserver
      ```
