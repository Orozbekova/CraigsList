```markdown
# CraigsList – Django Practice Project

A multi-app Django project created while learning Python and backend web development.

---
This project was built to explore how a real Django application is structured and how different parts of a web application work together.

### Goals of this project:

- Organizing a Django project into separate apps
- Working with models, views, and serializers
- Building a basic REST API with Django REST Framework
- Understanding authentication and overall project structure
- Practicing background tasks with Celery + Redis

---

## Apps

| App              | Description                        |
|------------------|------------------------------------|
| `board`          | Main listings / board functionality |
| `cart`           | Cart-related logic                 |
| `chat_app`       | Chat feature practice              |
| `normal_account` | User account handling              |

---

## Tech Stack

- **Python**
- **Django**
- **Django REST Framework**
- **PostgreSQL** (via `psycopg2`)
- **JWT Authentication** (`djangorestframework-simplejwt`)
- **Celery + Redis** (background tasks practice)
- Additional: `django-allauth`, `Pillow`, `django-filter`, `drf-yasg`

---

## Project Structure

CraigsList/

├── applications/

│   ├── board/

│   ├── cart/

│   ├── chat_app/

│   └── normal_account/

├── main/

├── manage.py

└── requirements.txttext


---

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver



