import pymysql
import random
import string
from datetime import datetime
from flask import session


def validateUserModel():
    user = []
    # Find user in DB according to customer ID saved in session
    conn = pymysql.connect(host='sql9.freemysqlhosting.net', db='sql9607922',
                           user='sql9607922', password='d7cwbda3De', port=3306)
    cur = conn.cursor()
   
    cur.execute("SELECT * FROM customer JOIN payment ON customer.c_id = payment.c_id WHERE customer.c_id = %s", session['customer'])
    userFound = cur.fetchall()

    # Save tuple information in a list
    for users in userFound:
        user.append({
            "id": users[0],
            "name": users[1],
            "last_name": users[2],
            "email": users[3],
            "password": users[4],
            "phone_number": users[5],
            "address_line1": users[6],
            "address_line2": users[7],
            "city": users[8],
            "state": users[9],
            "zipcode": users[10],
            "payment_id": users[11],
            "card_name": users[13],
            "card_type": users[14],
            "card_number": users[15],
            "exp_date": users[16],
            "status": users[17]
        })

    return user

    # Function to generate a random 6-digit tracking number
def generate_random_tracking_num():
    return str(random.randint(100000, 999999))

def calculate_cart_total(cart):
    total = 0
    for product_data in cart.values():
        total += product_data['total_price']
    return total

def sendToDatabaseModel(user, cart):
    conn = pymysql.connect(host='sql9.freemysqlhosting.net', db='sql9607922',user='sql9607922', password='d7cwbda3De', port=3306)
    cur = conn.cursor()

    c_id = user['id']
    payment_id = user['payment_id']

    print(cart)

    # Abrir el diccionario con la informacion del producto
    total_price = calculate_cart_total(cart)

    # Generate a unique tracking number
    tracking_num = generate_random_tracking_num()

    # Get the current date
    order_date = datetime.now().strftime('%Y-%m-%d')

    # Insert the order into the 'orders' table
    query = f"INSERT INTO orders(c_id, payment_id, tracking_num, order_date, total_price, o_status) VALUES ('{c_id}','{payment_id}','{tracking_num}','{order_date}',{total_price},'Standby')"
    cur.execute(query)
    conn.commit()
    conn.close()




