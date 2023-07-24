import pymysql
from datetime import datetime, timedelta

def getOrdersAndProductsModel():
    conn = pymysql.connect(host='sql9.freemysqlhosting.net', db='sql9607922',user='sql9607922', password='d7cwbda3De', port=3306)
    cur = conn.cursor()

    query = """
        SELECT o.o_id, o.tracking_num, o.order_date, o.arrival_date, c.c_address_line1, c.c_address_line2, o.total_price, p.card_type,
            prod.p_image, prod.p_name, prod.p_brand, con.amount, con.price, o.o_status
        FROM orders o
        JOIN customer c ON o.c_id = c.c_id
        JOIN payment p ON o.payment_id = p.payment_id
        JOIN contains con ON o.o_id = con.o_id
        JOIN products prod ON con.p_id = prod.p_id
        ORDER BY o.o_id, con.p_id
    """


    cur.execute(query)

    orders_with_products = {}
    current_order_id = None

    for row in cur.fetchall():
        order_id = row[0]

        # Create a new entry for a new order in the dictionary
        if order_id != current_order_id:
            current_order_id = order_id
            orders_with_products[order_id] = {
                'order_info': {
                    'tracking_num': row[1],
                    'order_date': row[2].strftime('%Y-%m-%d'),
                    'arrival_date': row[3].strftime('%Y-%m-%d'),
                    'address_line_1': row[4],
                    'address_line_2': row[5],
                    'total': row[6],
                    'payment_method': row[7],
                    'status': row[13]
                },
                'products': [],
                'total_items': 0
            }

        # Add the product to the respective order in the dictionary
        product_info = {
            'image': row[8],
            'name': row[9],
            'brand': row[10],
            'quantity': row[11],
            'price': row[12],
            'total_price': row[11] * row[12]
        }
        orders_with_products[order_id]['products'].append(product_info)
        orders_with_products[order_id]['total_items'] += row[11]

    conn.close()
    return orders_with_products

def updateOrdersModel():
    conn = pymysql.connect(host='sql9.freemysqlhosting.net', db='sql9607922',user='sql9607922', password='d7cwbda3De', port=3306)
    cur = conn.cursor()

    # Get all orders from the database
    query = "SELECT o_id, order_date, o_status FROM orders"
    cur.execute(query)
    results = cur.fetchall()

    # Calculate the status for each order
    for order_id, order_date, order_status in results:
        days_passed = (datetime.now().date() - order_date).days      
        print("This is how many days have passed: ",days_passed)
        if days_passed >= 2 and order_status == 'Received':
            new_status = 'Processed'
        elif days_passed >= 4 and order_status == 'Processed':
            new_status = 'Shipped'
        elif days_passed >= 7 and order_status == 'Shipped':
            new_status = 'Delivered'
        else:
            new_status = order_status

        # Update the order status in the database if it has changed
        if new_status != order_status:
            update_query = "UPDATE orders SET o_status = %s WHERE o_id = %s"
            cur.execute(update_query, (new_status, order_id))
            conn.commit()

    conn.close()
