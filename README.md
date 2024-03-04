> FastAPI Core Application
### Features

- User Registration: Users can create an account.
- User Login: Users can log in to their accounts.
- Role-based Authentication: Three roles with different permission levels - regular user, user manager, admin.
- CRUD Operations: Users can create, read, update, and delete their owned records.
- User Manager: User managers can CRUD users.
- Admin: Admins can CRUD all records and users.
- Entry Information: Each entry has a date, time, text, and number of calories.
- Calories API Integration: If calories are not provided, the API connects to a Calories API provider to fetch the number of calories for the entered meal.
- User Setting: Users can set their expected number of calories per day.
- Calorie Comparison: Each entry has a boolean field indicating if the total calories for the day are less than the expected number of calories.
- JSON API: Data is returned in JSON format.
- Filtering and Pagination: Endpoints provide filter capabilities and support pagination.
- Unit and E2E Tests: Includes unit tests and end-to-end tests.
- Python Web Framework: Uses any Python web framework.
- SQLite Database: Uses SQLite as the database.

> Installation and Setup

###### Clone repository run dependencies.

```bash
    git clone https://github.com/mbrsagor/fastapiCore.git
    cd fastapiCore
    virtualenv venv --python=python3.10
    source venv/bin/activate
    pip install -r requirements.txt
```
