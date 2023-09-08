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

def select_counters(camera_id):
    conn = psycopg2.connect(dbname='refrigeratorDB', user='refrigeratorUser', password='rupass', host='localhost', port="5432")
    cur = conn.cursor()
    sql = "SELECT * FROM fridge_counter WHERE camera_id = %s"
    cur.execute(sql, (camera_id,))
    counters = cur.fetchall()
    cur.close()
    conn.commit()
    conn.close()
    return counters