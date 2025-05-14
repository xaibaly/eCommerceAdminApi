E-commerce Admin API
This project is a backend API designed to power an e-commerce admin dashboard. The API is built using FastAPI and SQLAlchemy and provides endpoints for managing product sales, revenue analysis, inventory status, and more.

Features
Sales Data: Get sales data filtered by date range, product, or category.

Revenue Analysis: Calculate revenue for daily, weekly, monthly, and annual periods and compare across different timeframes and categories.

Inventory Management: View current inventory status, including low-stock alerts, and update stock levels.

Product Registration: Add new products to the database with a name, category, and price.

Dependencies:
fastapi: Web framework for building APIs.

uvicorn: ASGI server to run FastAPI apps.

sqlalchemy: ORM for working with databases.

mysql-connector-python: MySQL database connector for Python.

pydantic: Data validation and parsing used by FastAPI.

databases: Used to interact with relational databases asynchronously (if needed).

python-dotenv: To load environment variables from a .env file (if you need one for database credentials, etc.).


Setup Instructions
Prerequisites
You'll need the following installed:

Python 3.8+

MySQL or SQLite for the database (MySQL is recommended for production)

Steps to Get It Running
Clone the repo:

bash
Copy
Edit
git clone https://github.com/yourusername/ecommerce-api.git
cd ecommerce-api
Set up a virtual environment (optional but recommended):

bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install the dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Set up your database (MySQL or SQLite):

For MySQL:

bash
Copy
Edit
mysql -u username -p
CREATE DATABASE ecommerce;
For SQLite, it will automatically create a .db file in the project directory.

Create the database schema:
The application will automatically create the necessary tables when you start it.

Run the app:

bash
Copy
Edit
uvicorn main:app --reload
The API should now be accessible at http://localhost:8000.

API Endpoints
1. Register Product
POST /products/register

Use this endpoint to register a new product.

Request Body:

json
Copy
Edit
{
    "name": "Product Name",
    "category": "Category",
    "price": 100.0
}
Response:

json
Copy
Edit
{
    "message": "Product registered successfully",
    "product_id": 1
}
2. Get Sales Data
GET /sales

Fetch sales data with optional filters for date range, product, or category.

Query Parameters:

start_date: (optional) Start date in the format YYYY-MM-DD

end_date: (optional) End date in the format YYYY-MM-DD

product_id: (optional) Filter by product ID

category: (optional) Filter by product category

Response:

json
Copy
Edit
[
    {
        "product_id": 1,
        "quantity": 10,
        "revenue": 1000.0,
        "date": "2023-05-10T12:34:56"
    }
]
3. Analyze Revenue
GET /sales/revenue

Get a breakdown of sales revenue for daily, weekly, monthly, or annual periods. You can also compare periods.

Query Parameters:

period: (default: "daily") Choose daily, weekly, monthly, or annually.

compare_period: (optional) Compare with another period.

category: (optional) Filter by category.

start_date: (optional) Filter by start date.

end_date: (optional) Filter by end date.

Response:

json
Copy
Edit
{
    "period": "daily",
    "main_data": [
        {
            "date": "2023-05-10",
            "total_revenue": 1000.0
        }
    ],
    "comparison_period": "weekly",
    "comparison_data": [
        {
            "date": "2023-05-01",
            "total_revenue": 2000.0
        }
    ]
}
4. View Inventory
GET /inventory

Get the current inventory status and view any low-stock alerts.

Query Parameters:

low_stock_threshold: (optional, default: 10) Set the threshold for low stock.

Response:

json
Copy
Edit
{
    "inventory": [
        {
            "product_id": 1,
            "stock_level": 50
        }
    ],
    "low_stock_alerts": [
        {
            "product_id": 2,
            "stock_level": 5
        }
    ]
}
5. Update Inventory
POST /inventory/update

Update the stock level for a product.

Request Body:

json
Copy
Edit
{
    "product_id": 1,
    "stock_level": 100
}
Response:

json
Copy
Edit
{
    "message": "Inventory updated"
}
Database Structure
Products Table
Stores product details.

Columns:

id: Primary key

name: Name of the product

category: Category of the product

price: Price of the product

Sales Table
Stores sales records.

Columns:

id: Primary key

product_id: Foreign key to Products

quantity: Number of units sold

revenue: Revenue from the sale

date: Date of the sale

Inventory Table
Tracks product inventory.

Columns:

id: Primary key

product_id: Foreign key to Products

stock_level: Current stock level of the product

Inventory Logs Table
Tracks changes to inventory levels.

Columns:

id: Primary key

product_id: Foreign key to Products

stock_level: Stock level after the change

updated_at: Timestamp of the update

Testing the API
You can test the endpoints using Postman or a similar tool, or by using curl commands. Here's an example of how to call the GET /sales endpoint:

bash
Copy
Edit
curl "http://localhost:8000/sales?start_date=2023-05-01&end_date=2023-05-10"
License
This project is licensed under the MIT License. See the LICENSE file for more details.

