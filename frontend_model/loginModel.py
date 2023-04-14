from flask import session
import pymysql
from passlib.hash import sha256_crypt

def loginmodel(email, password):

    # Receive email and password to check in the "database"

    user = []
    conn = pymysql.connect(host='sql9.freemysqlhosting.net', db='sql9607922',
                           user='sql9607922', password='d7cwbda3De', port=3306)
    cur = conn.cursor()
    cur.execute("SELECT * from customer WHERE c_email = %s", email)
    userFound = cur.fetchall()
    for users in userFound:
        user.append({"id": users[0], "name": users[1], "last_name": users[2], "email": users[3], "password": users[4],
                    "phone_number": users[5], "address_line1": users[6], "address_line2": users[7], "city": users[8], "state": users[9], "zipcode": users[10],
                     "card_name": users[11], "card_type": users[12], "exp_date": users[13], "card_number": users[14], "status": users[15]})

    # Save user info in list

    # sha256_crypt.encrypt("password") = this is what is used to encrypt a password
    # sha256_crypt.verify(password_unhashed, password_hashed) = this is what is used to compare an unhashed and hashed password

    for u in user:
        print(user)
        print("Hashed password from user: ", u['password'])
        if email == u['email'] and sha256_crypt.verify(password, u['password']) is True:
            session['customer'] = u['id']
            # Create the session['customer'] saving the customer ID if user is found
            return "true"

    # If it didn't find user
    return "false"
