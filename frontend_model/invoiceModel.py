import pymysql


def getOrderModel(order_id):
    conn = pymysql.connect(host='sql9.freemysqlhosting.net', db='sql9607922',
                           user='sql9607922', password='d7cwbda3De', port=3306)
    cur = conn.cursor()

    # Perform the JOIN operation between 'orders', 'customer', and 'payment' tables
    query = """
        SELECT o.tracking_num, o.order_date, o.arrival_date, c.c_address_line1, c.c_address_line2, o.total_price, p.card_type
        FROM orders o
        JOIN customer c ON o.c_id = c.c_id
        JOIN payment p ON o.payment_id = p.payment_id
        WHERE o.o_id = %s
    """
    print("Orderid:", order_id)
    cur.execute(query, (order_id,))
    result = cur.fetchone()

    order_info = {
        "tracking_num": result[0],
        "order_date": result[1].strftime('%Y-%m-%d'),
        "arrival_date": result[2].strftime('%Y-%m-%d'),
        "address_line_1": result[3],
        "address_line_2": result[4],
        "total": result[5],
        "payment_method": result[6]
    }

    conn.close()
    return order_info





def getProductsModel(cart):

    # Create the dictionary using the cart data
    products = {}
    for product_id, product_details in cart.items():
        products[product_id] = {
            "image": product_details['image'],
            "name": product_details['name'],
            "brand": product_details['brand'],
            "price": product_details['price'],
            "quantity": product_details['quantity'],
            "total_price": product_details['total_price']
        }

    return products
