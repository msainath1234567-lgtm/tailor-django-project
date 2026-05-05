# Smart Tailors - Django + MySQL Project

## Included Modules

### Customer Website Pages
- Home page
- Customer register
- Customer login/logout
- Customer dashboard
- Customer profile update
- My orders
- Order details
- My measurements
- Add men measurement
- Add ladies measurement
- Services page
- Gallery page
- Contact enquiry page

### Admin Panel Pages
- Admin login
- Dashboard
- Customer Management
- Order Management
- Measurement Management
- Service Management
- Price Management
- Gallery Management
- Contact Enquiry Management
- Reports
- Site Settings

## Setup Commands

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create MySQL database:

```sql
CREATE DATABASE tailor_admin_db;
```

Copy `.env.example` to `.env` and update MySQL username/password.

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## URLs

Customer website:

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/register/
http://127.0.0.1:8000/login/
```

Admin panel:

```text
http://127.0.0.1:8000/admin-panel/
```

Django default admin:

```text
http://127.0.0.1:8000/django-admin/
```

## Notes
- Admin creates customer orders from admin panel.
- Customers can register, login, view orders, view order details, and add measurements.
- Database is MySQL configured from `.env`.
