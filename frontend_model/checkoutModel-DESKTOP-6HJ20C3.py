import pymysql
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
            "card_name": users[13],
            "card_type": users[14],
            "card_number": users[15],
            "exp_date": users[16],
            "status": users[17]
        })

    return user
