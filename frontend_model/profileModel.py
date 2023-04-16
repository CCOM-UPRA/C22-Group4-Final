import pymysql
from flask import session


def getUserModel():
    user = []
    # Connect to DB using given credentials
    conn = pymysql.connect(host='sql9.freemysqlhosting.net', db='sql9607922',
                           user='sql9607922', password='d7cwbda3De', port=3306)
    cur = conn.cursor()
    # Find user via the customer ID saved in session
    cur.execute("SELECT * from customer WHERE c_id = %s", session['customer'])
    userFound = cur.fetchall()

    # Save tuple information in a list
    for users in userFound:
        user.append({"id": users[0], "name": users[1], "last_name": users[2], "email": users[3], "password": users[4],
                    "phone_number": users[5], "address_line1": users[6], "address_line2": users[7], "city": users[8], "state": users[9], "zipcode": users[10],
                     "card_name": users[11], "card_type": users[12], "exp_date": users[13], "card_number": users[14], "status": users[15]})

    # To access user info:

        # for u in user:
        # u['id'], u['name'], u['email'], etc...
    return user


def editnumbermodel(number):
    conn = pymysql.connect(host='sql9.freemysqlhosting.net', db='sql9607922',
                           user='sql9607922', password='d7cwbda3De', port=3306)
    cur = conn.cursor()
    try:
        cur.execute("UPDATE customer SET c_phone_number = %s WHERE c_id = %s", (number, session['customer']))
        conn.commit()
        return 0

    except pymysql.Error as error:
        print(error)
        return 0

    else:
        cur.close()
        return 1


def editaddressmodel(aline1, aline2, state, zipcode, city):
    conn = None
    try:
        conn = pymysql.connect(host='sql9.freemysqlhosting.net', db='sql9607922',user='sql9607922', password='d7cwbda3De', port=3306)
        cur = conn.cursor()
        cur.execute("UPDATE customer SET c_address_line1 = %s, c_address_line2 = %s, c_city = %s,"
                    "c_state = %s, c_zipcode = %s WHERE c_id = %s", (aline1, aline2, city, state, zipcode, session['customer']))
        conn.commit()
        return 0
    except pymysql.Error as e:
        print(f"Error: {e}")
        return 1
    finally:
        if conn:
            conn.close()



def editpaymentmodel(name, c_type, number, exp_date):
    conn = None
    try:
        conn = pymysql.connect(host='sql9.freemysqlhosting.net', db='sql9607922',user='sql9607922', password='d7cwbda3De', port=3306)
        cur = conn.cursor()
        cur.execute("UPDATE customer SET c_card_name = %s, c_card_num = %s, "
                    "c_card_type = %s, c_exp_date = %s WHERE c_id = %s", (name, number, c_type, exp_date, session['customer']))
        conn.commit()
        return 0
    except pymysql.Error as e:
        print(f"Error: {e}")
        return 1
    finally:
        if conn:
            conn.close()


def editprofilemodel(fname, lname, email):
    conn = pymysql.connect(host='sql9.freemysqlhosting.net', db='sql9607922',
                           user='sql9607922', password='d7cwbda3De', port=3306)
    cur = conn.cursor()
    try:
        cur.execute("UPDATE customer SET c_name = %s, c_last_name = %s, "
                    "c_email = %s WHERE c_id = %s",
                    (fname, lname, email, session['customer']))
        conn.commit()
        return 0

    except pymysql.Error as error:
        print(error)
        return 0

    else:
        cur.close()
        return 1
