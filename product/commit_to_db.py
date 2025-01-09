import os
import shutil
import sqlite3
import psycopg2

sqlite_conn = sqlite3.connect('db.sqlite3')
sqlite_cursor = sqlite_conn.cursor()

sqlite_cursor.execute("SELECT name, image_1 FROM frontend_product")
sqlite_products = sqlite_cursor.fetchall()


postgres_conn = psycopg2.connect(
    dbname="moto_db",
    user="postgres",
    password="20090912",
    host="localhost"
)
postgres_cursor = postgres_conn.cursor()

media_dir = "./media/"
for product in sqlite_products:
    name, image = product
    if image:  # `image` bo'sh bo'lmaganini tekshirish
        src_image_path = os.path.join('path_to_sqlite_images', image)
        dest_image_path = os.path.join(media_dir, image)

        # Faylni nusxalash
        if os.path.exists(src_image_path):
            shutil.copy(src_image_path, dest_image_path)
        else:
            print(f"Fayl topilmadi: {src_image_path}")

    postgres_cursor.execute("""
        UPDATE product_product
        SET image = %s
        WHERE name = %s
    """, (image, name))

postgres_conn.commit()
sqlite_cursor.close()
sqlite_conn.close()
postgres_cursor.close()
postgres_conn.close()