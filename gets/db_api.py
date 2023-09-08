import psycopg2
import json

def select_cameras(user_id):
    conn = psycopg2.connect(dbname='refrigeratorDB', user='refrigeratorUser', password='rupass', host='localhost', port="5432")
    cur = conn.cursor()
    sql = "SELECT * FROM fridge_camera WHERE user_id = %s"
    cur.execute(sql, (user_id,))
    cameras = cur.fetchall()
    cur.close()
    conn.commit()
    conn.close()
    return cameras

def select_user_id(username):
    conn = psycopg2.connect(dbname='refrigeratorDB', user='refrigeratorUser', password='rupass', host='localhost', port="5432")
    cur = conn.cursor()
    sql = "SELECT id FROM auth_user WHERE username = %s"
    cur.execute(sql, (username,))
    user_id = cur.fetchone()[0]
    cur.close()
    conn.commit()
    conn.close()
    return user_id

def select_product_id(name):
    conn = psycopg2.connect(dbname='refrigeratorDB', user='refrigeratorUser', password='rupass', host='localhost', port="5432")
    cur = conn.cursor()
    sql = "SELECT id FROM fridge_product WHERE name = %s"
    cur.execute(sql, (name,))
    product_id = cur.fetchone()[0]
    cur.close()
    conn.commit()
    conn.close()
    return product_id

def select_product_name(product_id):
    conn = psycopg2.connect(dbname='refrigeratorDB', user='refrigeratorUser', password='rupass', host='localhost', port="5432")
    cur = conn.cursor()
    sql = "SELECT name FROM fridge_product WHERE id = %s"
    cur.execute(sql, (product_id,))
    name = cur.fetchone()[0]
    cur.close()
    conn.commit()
    conn.close()
    return name

def select_counters(camera_id):
    conn = psycopg2.connect(dbname='refrigeratorDB', user='refrigeratorUser', password='rupass', host='localhost', port="5432")
    cur = conn.cursor()
    sql = "SELECT fridge_counter.id, fridge_counter.current_counter, fridge_product.name \
    FROM fridge_counter JOIN fridge_product \
    ON fridge_counter.product_id = fridge_product.id WHERE camera_id = %s"
    cur.execute(sql, (camera_id,))
    counters = cur.fetchall()
    cur.close()
    conn.commit()
    conn.close()
    return counters

def delete_counter(counter_id):
    conn = psycopg2.connect(dbname='refrigeratorDB', user='refrigeratorUser', password='rupass', host='localhost', port="5432")
    cur = conn.cursor()
    sql = "DELETE FROM fridge_counter WHERE id = %s"
    cur.execute(sql, (counter_id,))
    cur.close()
    conn.commit()
    conn.close()

def update_counter(counter_id, count):
    conn = psycopg2.connect(dbname='refrigeratorDB', user='refrigeratorUser', password='rupass', host='localhost', port="5432")
    cur = conn.cursor()
    sql = "UPDATE fridge_counter SET current_counter = %s WHERE id = %s"
    cur.execute(sql, (count, counter_id))
    cur.close()
    conn.commit()
    conn.close()