
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from database import get_connection

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


# =====================================
# GET PRODUCTS FROM MYSQL
# =====================================

def get_products():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM products ORDER BY id")
            rows = cursor.fetchall()

        products = []

        for row in rows:
            products.append({
                "id": row["id"],
                "title": row["title"],
                "price": float(row["price"]),
                "description": row["description"],
                "category": row["category"],
                "image": row["image"],
                "rating": {
                    "rate": float(row["rating_rate"] or 0),
                    "count": row["rating_count"]
                },
                "in_stock": bool(row["in_stock"]),
                "promoted": bool(row["promoted"])
            })

        return products

    finally:
        connection.close()


# =====================================
# GET CART ITEMS FROM MYSQL
# =====================================

def get_cart_items():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    products.id,
                    products.title,
                    products.price,
                    products.image,
                    cart_items.quantity
                FROM cart_items
                JOIN products
                ON cart_items.product_id = products.id
                ORDER BY cart_items.id
            """)

            rows = cursor.fetchall()

            cart_items = []

            for row in rows:
                price = float(row["price"])
                quantity = row["quantity"]

                cart_items.append({
                    "id": row["id"],
                    "title": row["title"],
                    "price": price,
                    "image": row["image"],
                    "quantity": quantity,
                    "subtotal": price * quantity
                })

            return cart_items

    finally:
        connection.close()


# =====================================
# ADD PRODUCT TO MYSQL CART
# =====================================

def add_product_to_cart(product_id):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT quantity
                FROM cart_items
                WHERE product_id = %s
            """, (product_id,))

            item = cursor.fetchone()

            if item:
                cursor.execute("""
                    UPDATE cart_items
                    SET quantity = quantity + 1
                    WHERE product_id = %s
                """, (product_id,))
            else:
                cursor.execute("""
                    INSERT INTO cart_items (product_id, quantity)
                    VALUES (%s, 1)
                """, (product_id,))

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


# =====================================
# HOME PAGE
# =====================================

@app.get("/")
def home(request: Request):
    products = get_products()

    return templates.TemplateResponse(
        request=request,
        name="products.html",
        context={
            "products": products,
            "selected_category": "",
            "search_query": "",
            "selected_sort": ""
        }
    )


# =====================================
# PRODUCTS PAGE
# =====================================

@app.get("/products")
def show_products(
    request: Request,
    category: str = "",
    search: str = "",
    sort: str = ""
):
    products = get_products()

    if category:
        products = [
            p for p in products
            if p["category"].lower() == category.lower()
        ]

    if search:
        products = [
            p for p in products
            if search.lower() in p["title"].lower()
            or search.lower() in p["description"].lower()
        ]

    if sort == "low":
        products.sort(key=lambda p: p["price"])
    elif sort == "high":
        products.sort(key=lambda p: p["price"], reverse=True)
    elif sort == "rating":
        products.sort(
            key=lambda p: p["rating"]["rate"],
            reverse=True
        )

    return templates.TemplateResponse(
        request=request,
        name="products.html",
        context={
            "products": products,
            "selected_category": category,
            "search_query": search,
            "selected_sort": sort
        }
    )


# =====================================
# PRODUCT DETAILS
# =====================================

@app.get("/product/{product_id}")
def product_details(request: Request, product_id: int):
    products = get_products()

    product = next(
        (p for p in products if p["id"] == product_id),
        None
    )

    if product is None:
        return templates.TemplateResponse(
            request=request,
            name="404.html",
            context={},
            status_code=404
        )

    return templates.TemplateResponse(
        request=request,
        name="product_details.html",
        context={"product": product}
    )


# =====================================
# CART PAGE
# =====================================

@app.get("/cart")
def view_cart(request: Request):
    cart_items = get_cart_items()

    total_price = sum(
        item["subtotal"] for item in cart_items
    )

    cart_count = sum(
        item["quantity"] for item in cart_items
    )

    return templates.TemplateResponse(
        request=request,
        name="cart.html",
        context={
            "cart_items": cart_items,
            "total_price": total_price,
            "cart_count": cart_count
        }
    )


# =====================================
# ADD TO CART
# =====================================

@app.get("/add-to-cart/{product_id}")
def add_to_cart(product_id: int):
    products = get_products()

    product = next(
        (p for p in products if p["id"] == product_id),
        None
    )

    if product and product["in_stock"]:
        add_product_to_cart(product_id)

    return RedirectResponse(url="/cart", status_code=303)


# =====================================
# REMOVE FROM CART
# =====================================

@app.get("/remove-from-cart/{product_id}")
def remove_from_cart(product_id: int):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                DELETE FROM cart_items
                WHERE product_id = %s
            """, (product_id,))

        connection.commit()

    finally:
        connection.close()

    return RedirectResponse(url="/cart", status_code=303)


# =====================================
# INCREASE QUANTITY
# =====================================

@app.get("/increase-quantity/{product_id}")
def increase_quantity(product_id: int):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE cart_items
                SET quantity = quantity + 1
                WHERE product_id = %s
            """, (product_id,))

        connection.commit()

    finally:
        connection.close()

    return RedirectResponse(url="/cart", status_code=303)


# =====================================
# DECREASE QUANTITY
# =====================================

@app.get("/decrease-quantity/{product_id}")
def decrease_quantity(product_id: int):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE cart_items
                SET quantity = quantity - 1
                WHERE product_id = %s
            """, (product_id,))

            cursor.execute("""
                DELETE FROM cart_items
                WHERE product_id = %s AND quantity <= 0
            """, (product_id,))

        connection.commit()

    finally:
        connection.close()

    return RedirectResponse(url="/cart", status_code=303)


# =====================================
# CHECKOUT PAGE
# =====================================

@app.get("/checkout")
def checkout(request: Request):
    cart_items = get_cart_items()

    if not cart_items:
        return RedirectResponse(url="/cart", status_code=303)

    total_price = sum(
        item["subtotal"] for item in cart_items
    )

    return templates.TemplateResponse(
        request=request,
        name="checkout.html",
        context={"total_price": total_price}
    )


# =====================================
# PLACE ORDER
# =====================================

@app.post("/place-order")
def place_order(
    customer_name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    address: str = Form(...)
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            # Get current cart items from database
            cursor.execute("""
                SELECT
                    products.id,
                    products.title,
                    products.price,
                    cart_items.quantity
                FROM cart_items
                JOIN products
                ON cart_items.product_id = products.id
            """)

            cart_items = cursor.fetchall()

            if not cart_items:
                return RedirectResponse(
                    url="/cart",
                    status_code=303
                )

            # Calculate total amount
            total_amount = sum(
                float(item["price"]) * item["quantity"]
                for item in cart_items
            )

            # Start database transaction
            connection.begin()

            # Insert order
            cursor.execute("""
                INSERT INTO orders (
                    customer_name,
                    email,
                    phone,
                    address,
                    total_amount
                )
                VALUES (%s, %s, %s, %s, %s)
            """, (
                customer_name,
                email,
                phone,
                address,
                total_amount
            ))

            order_id = cursor.lastrowid

            # Insert ordered products
            for item in cart_items:
                cursor.execute("""
                    INSERT INTO order_items (
                        order_id,
                        product_id,
                        product_title,
                        price,
                        quantity
                    )
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    order_id,
                    item["id"],
                    item["title"],
                    item["price"],
                    item["quantity"]
                ))

            # Clear cart after successful order
            cursor.execute("DELETE FROM cart_items")

        connection.commit()

        return RedirectResponse(
            url=f"/order-success/{order_id}",
            status_code=303
        )

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

# =====================================
# ORDER SUCCESS PAGE
# =====================================

@app.get("/order-success/{order_id}")
def order_success(request: Request, order_id: int):

    return templates.TemplateResponse(
        request=request,
        name="order_success.html",
        context={
            "order_id": order_id
        }
    )
