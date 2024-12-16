# Expense Management API

This is a **RESTful API** for managing expenses, built with **Django REST Framework (DRF)**.  
It allows users to **create, retrieve, update, and delete** expenses, as well as apply additional filtering and summarization.

---

## **Features**
- Full **CRUD** functionality for managing expenses.
- **Filter expenses** by date range.
- **Summarize expenses** by category for a specific month and year.
- Interactive **API documentation** with Swagger and ReDoc.

---

## **Technologies Used**
- **Backend**: Django, Django REST Framework
- **Documentation**: drf-yasg (Swagger, ReDoc)
- **Database**: SQLite3 
- **Testing**: Django TestCase, DRF APITestCase

---

## **API Endpoints**

### **Expense CRUD**
| Method | Endpoint                | Description             |
|--------|-------------------------|-------------------------|
| `GET`  | `/expenses/`            | List all expenses       |
| `POST` | `/expenses/`            | Create a new expense    |
| `GET`  | `/expenses/{id}/`       | Retrieve a specific expense |
| `PUT`  | `/expenses/{id}/`       | Update an existing expense  |
| `DELETE` | `/expenses/{id}/`     | Delete an expense       |

### **Custom Endpoints**
| Method | Endpoint                                | Description                                 |
|--------|-----------------------------------------|---------------------------------------------|
| `GET`  | `/expenses/filter_by_date/?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD` | Filter expenses by date range |
| `GET`  | `/expenses/summary_by_category/?year=YYYY&month=MM`                   | Summarize expenses by category for a given month |

---

## **Setup Instructions**

### **1. Clone the Repository**
```bash
git clone https://github.com/<your_username>/pageloot_test.git
cd pageloot_test
```

### **2. Create a Virtual Environment**
```bash
python3 -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Apply Migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

### **5. Create a Superuser**
```bash
python manage.py createsuperuser
```

### **6. Run the Server**
```bash
python manage.py runserver
Access the API at: http://127.0.0.1:8000/
```

## **Interactive API Documentation**
Swagger: http://127.0.0.1:8000/swagger/
ReDoc: http://127.0.0.1:8000/redoc/

## **Testing**
Run unit tests using the Django testing framework:
```bash
python manage.py test expenses
```

