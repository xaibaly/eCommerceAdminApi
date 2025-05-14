from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from .database import Base, engine, get_db
from .models import Product, Sale, Inventory
from .schemas import ProductCreate, InventoryUpdate, SalesData
from sqlalchemy import func, extract

Base.metadata.create_all(bind=engine)

app = FastAPI()
#Core Features #1.1 Endpoints to retrieve, filter, and analyze sales data.
#Core Features #1.4 Provide sales data by date range, product, and category.

@app.get("/sales")
def get_sale_data(
    start_date: str = None,
    end_date: str = None,
    product_id: int = None,
    category: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(Sale)

    if start_date and end_date:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        query = query.filter(Sale.date >= start, Sale.date <= end)

    if product_id:
        query = query.filter(Sale.product_id == product_id)

    if category:
        query = query.join(Product).filter(Product.category == category)

    sales_data = query.all()
    return sales_data

#Core Features #1.4 Endpoints to analyze revenue on a daily, weekly, monthly, and annual basis
#Core Features #1.3 Ability to compare revenue across different periods and categories
@app.get("/sales/revenue")
def get_sale_revenue(
    period: str = "daily",
    compare_period: str = None,
    category: str = None,
    start_date: str = None,
    end_date: str = None,
    db: Session = Depends(get_db)
):
    try:
        query = db.query(Sale.date, func.sum(Sale.revenue).label("total_revenue"))
        if category:
            query = query.join(Product).filter(Product.category == category)
        if start_date and end_date:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            query = query.filter(Sale.date >= start, Sale.date <= end)
        if period == "daily":
            query = query.group_by(Sale.date)
        elif period == "weekly":
            query = query.group_by(extract('week', Sale.date))
        elif period == "monthly":
            query = query.group_by(extract('month', Sale.date))
        elif period == "annually":
            query = query.group_by(extract('year', Sale.date))
        else:
            return {"error": "Invalid period. Choose from daily, weekly, monthly, annually."}
        revenue_data = query.all()
        main_result = [{"date": str(record[0]), "total_revenue": float(record[1])} for record in revenue_data]
        comparison_result = []

        if compare_period:
            compare_query = db.query(Sale.date, func.sum(Sale.revenue).label("total_revenue"))
            if category:
                compare_query = compare_query.join(Product).filter(Product.category == category)
            if start_date and end_date:
                compare_query = compare_query.filter(Sale.date >= start, Sale.date <= end)
            if compare_period == "daily":
                compare_query = compare_query.group_by(Sale.date)
            elif compare_period == "weekly":
                compare_query = compare_query.group_by(extract('week', Sale.date))
            elif compare_period == "monthly":
                compare_query = compare_query.group_by(extract('month', Sale.date))
            elif compare_period == "annually":
                compare_query = compare_query.group_by(extract('year', Sale.date))
            else:
                return {"error": "Invalid compare_period. Choose from daily, weekly, monthly, annually."}
            comparison_data = compare_query.all()
            comparison_result = [{"date": str(record[0]), "total_revenue": float(record[1])} for record in comparison_data]

        response = {
            "period": period,
            "main_data": main_result,
            "comparison_period": compare_period,
            "comparison_data": comparison_result
        }

        return response

    except Exception as e:
        return {"error": str(e)}
    
#Core Features #2.1 Endpoints to view current inventory status, including low stock alerts
@app.get("/inventory")
def get_inventory(low_stock_threshold: int = 10, db: Session = Depends(get_db)):
    query = db.query(Inventory).all()

    #Check for Stock which are low in this example less than or equal to 10
    low_stock_items = db.query(Inventory).filter(Inventory.stock_level <= low_stock_threshold).all()

    return {
        "inventory": query,
        "low_stock_alerts": low_stock_items
    }
#requirement #4 allow new product registration
@app.post("/products/register")
def register_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = Product(
        name=product.name,
        category=product.category,
        price=product.price
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {"message": "Product registered successfully", "product_id": new_product.id}




@app.post("/inventory/update")
def update_inventory(data: InventoryUpdate, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == data.product_id).first()
    if inventory:
        inventory.stock_level = data.stock_level
        db.commit()
        return {"message": "Inventory updated"}
    return {"error": "Product not found"}

@app.get('/')
def get_status():
    #checking for API working or not
    return 'working'

