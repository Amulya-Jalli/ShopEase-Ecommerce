# 🛍️ ShopEase – E-Commerce Web Application

ShopEase is a full-stack e-commerce web application developed using Python, FastAPI, MySQL, HTML, and CSS. It allows users to browse products, search and filter items, manage their shopping cart, and place orders through a simple and responsive interface.

## 🚀 Features

- Display products with images, prices, and descriptions.
- Search products by name.
- Filter products by category.
- Sort products.
- View individual product details.
- Add products to the shopping cart.
- Increase or decrease product quantities.
- Remove products from the cart.
- Checkout and place orders.
- Store products, cart items, and orders in MySQL.
- Responsive user interface.
- Custom 404 error page.

## 🛠️ Technologies Used

- **Backend:** Python, FastAPI
- **Frontend:** HTML, CSS
- **Database:** MySQL
- **Template Engine:** Jinja2
- **Database Connectivity:** PyMySQL
- **Server:** Uvicorn

## 📁 Project Structure

```text
Ecommerce_Project/
│
├── main.py
├── database.py
├── data.py
├── seed.py
├── requirements.txt
├── .gitignore
├── .env
│
├── templates/
│   ├── products.html
│   ├── product_details.html
│   ├── cart.html
│   ├── checkout.html
│   ├── order_success.html
│   └── 404.html
│
└── static/
    └── style.css
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Amulya-Jalli/ShopEase-Ecommerce.git
```

### 2. Navigate to the project folder

```bash
cd ShopEase-Ecommerce
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

Windows:

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure environment variables

Create a `.env` file in the project root:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=shopease_db
```

Replace the password placeholder with your own MySQL password.

### 7. Create the MySQL database

Open MySQL Workbench and execute:

```sql
CREATE DATABASE shopease_db;
```

Run the project's database initialization and seed scripts as required to create and populate the tables.

### 8. Start the FastAPI server

```bash
python -m uvicorn main:app --reload
```

### 9. Open the application

Visit:

```text
http://127.0.0.1:8000
```

## 🎯 Project Objective

The main objective of ShopEase is to develop a simple and user-friendly online shopping application that demonstrates backend development, database integration, server-side rendering, and responsive frontend design.

## 👩‍💻 Developer

**Jalli Amulya**

- GitHub: https://github.com/Amulya-Jalli

---

⭐ If you find this project useful, feel free to explore the repository!