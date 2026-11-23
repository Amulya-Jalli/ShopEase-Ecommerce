from database import get_connection
from data import products

connection = get_connection()

try:
    with connection.cursor() as cursor:

        for product in products:
            cursor.execute(
                """
                INSERT INTO products (
                    id, title, price, description, category,
                    image, rating_rate, rating_count,
                    in_stock, promoted
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)

                ON DUPLICATE KEY UPDATE
                    title = VALUES(title),
                    price = VALUES(price),
                    description = VALUES(description),
                    category = VALUES(category),
                    image = VALUES(image),
                    rating_rate = VALUES(rating_rate),
                    rating_count = VALUES(rating_count),
                    in_stock = VALUES(in_stock),
                    promoted = VALUES(promoted)
                """,
                (
                    product["id"],
                    product["title"],
                    product["price"],
                    product["description"],
                    product["category"],
                    product["image"],
                    product["rating"]["rate"],
                    product["rating"]["count"],
                    product["in_stock"],
                    product["promoted"]
                )
            )

    connection.commit()
    print("All products inserted successfully!")

except Exception as e:
    connection.rollback()
    print("Error:", e)

finally:
    connection.close()