# Lapaulla Groceries â€” Django E-commerce Application



A Django-powered grocery shopping web application designed to simplify online grocery shopping, product management and order processing.



## Project Overview



Lapaulla Groceries is an e-commerce application that allows customers to browse grocery products, explore packaged Nigerian soup kits, manage shopping carts and place orders using a simulated wallet payment system.



The project demonstrates practical experience in Python and Django backend development, backend architecture, relational database design and e-commerce business logic.



## Features



- **User Authentication:** Customer registration, login and account management.

- **Product Catalogue:** Browse grocery products and categories.

- **Soup Kits:** Packaged soup kits with related ingredient records.

- **Shopping Cart:** Add products and soup kits, update quantities and remove items.

- **Wallet Management:** Wallet balance management and simulated wallet payments.

- **Order Management:** Create and manage customer orders.

- **Inventory Management:** Product availability checks and stock deductions during checkout.

- **Admin Dashboard:** Manage products, categories, soup kits and orders through Django Admin with Jazzmin.

- **Automated Testing:** Tests covering cart operations and wallet checkout scenarios.



## Technology Stack



- Python 3

- Django 5.2

- SQLite

- Django ORM

- HTML5

- CSS3

- Jazzmin Admin



## Backend Architecture



The application follows Django's Model-View-Template (MVT) architecture.



The main application components include:



1. **Presentation Layer:** HTML templates and CSS for the customer-facing storefront.

2. **Routing Layer:** Django URL configurations connecting requests to application views.

3. **Business Logic Layer:** Views responsible for authentication, cart operations, checkout, wallet transactions and inventory validation.

4. **Data Layer:** Django models and ORM managing products, categories, carts, soup kits, wallets and orders.

5. **Database Layer:** SQLite database for local development.



## Installation and Setup



### 1. Clone the repository



```bash

git clone https://github.com/barnabz/Grocery-Store.git

cd Grocery-Store

```



### 2. Navigate to the Django application directory



```powershell

cd lapaulla_store

```



### 3. Create and activate a virtual environment



```powershell

python -m venv .venv

.venv\\Scripts\\Activate.ps1

```



### 4. Install dependencies



```powershell

python -m pip install -r requirements.txt

```



### 5. Configure environment variables



Create a `.env` file in the same directory as `manage.py` and add:



```env

DJANGO_SECRET_KEY=your-generated-secret-key

```



Generate a secure key locally:



```powershell

python -c "import secrets; print(secrets.token_urlsafe(50))"

```



Copy the generated key into your `.env` file.



Do not commit `.env` or other private configuration files to GitHub.



### 6. Apply database migrations



```powershell

python manage.py migrate

```



### 7. Create an administrator account



```powershell

python manage.py createsuperuser

```



### 8. Start the development server



```powershell

python manage.py runserver

```



Open `http://127.0.0.1:8000/` in your browser.



## Running Tests



Run the application tests:



```powershell

python manage.py test store

```



Run Django system checks:



```powershell

python manage.py check

```



## Payment Information



The wallet checkout functionality is simulated for demonstration purposes. The application does not currently integrate with a live payment gateway.



## Project Purpose



This project was developed to demonstrate practical skills in:



- Python and Django backend development.

- Backend architecture and application structure.

- Relational database modelling.

- E-commerce business logic.

- Shopping cart and order processing.

- Inventory management.

- Database operations using Django ORM.

- Automated testing and application validation.



## Future Improvements



- Integration with a live payment gateway.

- Additional production deployment configuration.

- Further application security and performance improvements.



## Author



**Dennis Barnabas Ofon**


Python / Django Backend Developer
