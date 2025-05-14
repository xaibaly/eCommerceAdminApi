
# E-commerce Admin API

This is a backend API developed using Python and FastAPI to power an e-commerce admin dashboard. The API allows managers to retrieve and analyze sales data, track inventory, and register new products.

## Features

### 1. Sales Status
- Retrieve, filter, and analyze sales data.
- Analyze revenue on a daily, weekly, monthly, and annual basis.
- Compare revenue across different periods and categories.
- Filter sales data by date range, product, and category.

### 2. Inventory Management
- View current inventory status, including low stock alerts.
- Update inventory levels and track changes over time.

### 3. Product Management
- Register new products to the inventory.

## Requirements

- Python 3.7+
- FastAPI
- SQLAlchemy
- MySQL
- Pydantic
- Uvicorn (for running the FastAPI app)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/ecommerce-admin-api.git
    cd ecommerce-admin-api
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up the database:
   - Configure your database connection in the `.env` or `database.py` file (replace with your own MySQL credentials).
   - Run the migrations or use `Base.metadata.create_all(bind=engine)` to create the necessary tables in the database.

4. Run the FastAPI server:

    ```bash
    uvicorn main:app --reload
    ```

    The API will be accessible at `http://127.0.0.1:8000`.

## API Endpoints

### 1. Sales Data Endpoints

#### GET /sales

Retrieve all sales data, with optional filtering by:
- `start_date`: Start date in `YYYY-MM-DD` format.
- `end_date`: End date in `YYYY-MM-DD` format.
- `product_id`: Filter by product ID.
- `category`: Filter by product category.

Example response:

```json
[
  {
    "id": 1,
    "product_id": 101,
    "quantity_sold": 3,
    "revenue": 300.00,
    "date": "2023-05-15T00:00:00"
  }
]
```

#### GET /sales/revenue

Analyze sales revenue based on different periods (`daily`, `weekly`, `monthly`, `annually`). You can also compare revenue for two different periods.

Parameters:
- `period`: Specify the period (default: `daily`).
- `compare_period`: Compare with another period (optional).
- `category`: Filter by product category (optional).
- `start_date`: Start date for the analysis.
- `end_date`: End date for the analysis.

Example response:

```json
{
  "period": "daily",
  "main_data": [
    {
      "date": "2023-05-15",
      "total_revenue": 500.00
    }
  ],
  "comparison_period": "weekly",
  "comparison_data": [
    {
      "date": "2023-05-10",
      "total_revenue": 450.00
    }
  ]
}
```

### 2. Inventory Management Endpoints

#### GET /inventory

Retrieve the current inventory status. It also includes low stock alerts (items with stock levels below a given threshold).

Parameters:
- `low_stock_threshold`: The threshold for low stock (default: `10`).

Example response:

```json
{
  "inventory": [
    {
      "product_id": 101,
      "stock_level": 30
    }
  ],
  "low_stock_alerts": [
    {
      "product_id": 105,
      "stock_level": 5
    }
  ]
}
```

#### POST /inventory/update

Update the stock level of a product.

Request body:

```json
{
  "product_id": 101,
  "stock_level": 50
}
```

Example response:

```json
{
  "message": "Inventory updated"
}
```

### 3. Product Management Endpoints

#### POST /products/register

Register a new product in the inventory.

Request body:

```json
{
  "name": "New Product",
  "category": "Electronics",
  "price": 199.99
}
```

Example response:

```json
{
  "message": "Product registered successfully",
  "product_id": 123
}
```

## Database Schema

The database schema includes the following tables:

### 1. `products`
- `id`: Unique identifier for the product.
- `name`: Name of the product.
- `category`: Category to which the product belongs.
- `price`: Price of the product.

### 2. `sales`
- `id`: Unique identifier for the sale.
- `product_id`: Reference to the `products` table.
- `quantity_sold`: The quantity of the product sold.
- `revenue`: The revenue generated from the sale.
- `date`: Date of the sale.

### 3. `inventory`
- `id`: Unique identifier for the inventory record.
- `product_id`: Reference to the `products` table.
- `stock_level`: Current stock level of the product.

## License

This project is open-source and available under the [MIT License](LICENSE).
