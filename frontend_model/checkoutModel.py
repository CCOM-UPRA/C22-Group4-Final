import pymysql
import random
import string
from datetime import datetime, timedelta
from flask import session


def validateUserModel():
    user = []
    # Find user in DB from session
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

    # Genera 6 numeros aleatorios para el tracking number
def generate_random_tracking_num():
    return str(random.randint(100000, 999999))

    # Calcula el precio total del carrito
def calculate_cart_total(cart):
    total = 0
    for product_data in cart.values():
        total += product_data['total_price']
    return total

    # Esta funcion sube toda la informacion a la base de datos
def sendToDatabaseModel(user, cart):
    conn = pymysql.connect(host='sql9.freemysqlhosting.net', db='sql9607922',user='sql9607922', password='d7cwbda3De', port=3306)
    cur = conn.cursor()

    try:
        c_id = user['id']
        payment_id = user['payment_id']
        total_price = calculate_cart_total(cart)
        tracking_num = generate_random_tracking_num()
        order_date = datetime.now().strftime('%Y-%m-%d')

        order_date2 = datetime.strptime(order_date, '%Y-%m-%d')
        seven_days = timedelta(days=7)
        arrival_date = order_date2 + seven_days
        arrival_date = arrival_date.strftime('%Y-%m-%d')

        # Insert the order into the 'orders' table
        query = f"INSERT INTO orders(c_id, payment_id, tracking_num, order_date, arrival_date, total_price, o_status) " \
                f"VALUES ('{c_id}','{payment_id}','{tracking_num}','{order_date}','{arrival_date}',{total_price},'Received')"
        cur.execute(query)

        # Get the newly inserted order ID
        cur.execute("SELECT LAST_INSERT_ID()")
        order_id = cur.fetchone()[0]

        # Insert product information into the 'contains' table for each product in the cart
        for product_id, product_data in cart.items():
            price = product_data['price']
            amount = product_data['quantity']

            query = f"INSERT INTO contains(o_id, p_id, amount, price) " \
                    f"VALUES ({order_id}, {product_id}, {amount},  {price})"
            cur.execute(query)

            # Update the available_quantity in the products table
            update_query = f"UPDATE products SET p_stock = p_stock - {amount} WHERE p_id = {product_id}"
            cur.execute(update_query)


        conn.commit()
        print("Order and product information successfully added to the database!")

    except Exception as e:
        print(f"Error occurred: {e}")
        conn.rollback()

    finally:
        conn.close()
