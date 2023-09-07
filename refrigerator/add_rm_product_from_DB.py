import argparse

import psycopg2

parser = argparse.ArgumentParser(description="Arguments for sql counter update")
parser.add_argument(
    "--how_much", type=int, help="How much products", required=False, default=1
)
parser.add_argument("--product_name", type=str, help="Product name", required=True)
parser.add_argument("--rm", action="store_true", help="Rm product, default add")
parser.add_argument("--fridge_id", type=int, help="Fridge/camera id", required=True)

my_namespace = parser.parse_args()

print(my_namespace)
# exit()
conn = psycopg2.connect(
    host="127.0.0.1",
    database="refrigeratorDB",
    user="refrigeratorUser",
    password="rupass",
)
cur = conn.cursor()

# exit()

if my_namespace.rm:
    sql_update_counter = """UPDATE fridge_counter SET current_counter = current_counter - %s WHERE camera_id = %s and product_id = %s"""
else:
    sql_update_counter = """UPDATE fridge_counter SET current_counter = current_counter + %s WHERE camera_id = %s and product_id = %s"""

current_product = None

cur.execute("select * from fridge_product")
products = cur.fetchall()
conn.commit()
current_product = [(x, y) for x, y in products if y == my_namespace.product_name][0]
print(products)
print(current_product)

current_camera = None
cur.execute("select * from fridge_camera")
cameras = cur.fetchall()
conn.commit()
for cam in cameras:
    if cam[0] == my_namespace.fridge_id:
        current_camera = cam

print(cameras)
print(current_camera)

if not current_camera or not current_product:
    print("Camera or product doesn't exist")
    exit()

cur.execute(
    sql_update_counter, (my_namespace.how_much, current_camera[0], current_product[0])
)
conn.commit()
exit()

# name
# поместили/забрали
