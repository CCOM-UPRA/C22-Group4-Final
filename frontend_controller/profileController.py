from passlib.handlers.sha2_crypt import sha256_crypt

from frontend_model.profileModel import *


def getUser():
    return getUserModel()


def editnumbercontroller(number):
    return editnumbermodel(number)


def editaddresscontroller(aline1, aline2, state, zipcode, city):
    return editaddressmodel(aline1, aline2, state, zipcode, city)


def editpaymentcontroller(name, c_type, number, exp_date):
    return editpaymentmodel(name, c_type, number, exp_date)


def editprofilecontroller(fname, lname, email):
    return editprofilemodel(fname, lname, email)


def changePass():
    user = []
    # Connect to MySQL database server using credentials provided
    conn = pymysql.connect(host='sql9.freemysqlhosting.net', db='sql9607922',
                           user='sql9607922', password='d7cwbda3De', port=3306)

    cur = conn.cursor()
    # Select the specific customer whose password you want to hash
    cur.execute("SELECT * from customer WHERE c_email = 'javier.quinones3@upr.edu' ")
    userFound = cur.fetchall()

    # This part isn't necessary here but is shown so student can visualize the DB structure
    for users in userFound:
        user.append({"id": users[0], "name": users[1], "last_name": users[2], "email": users[3], "password": users[4],
                    "phone_number": users[5], "address_line1": users[6], "address_line2": users[7], "city": users[8], "state": users[9], "zipcode": users[10],
                     "card_name": users[11], "card_type": users[12], "exp_date": users[13], "card_number": users[14], "status": users[15]})
        # Save the user's password in 'passw'
        passw = users[4]

    # Encrypt the password using the sha256_crypt function
    hash = sha256_crypt.encrypt(passw)
    print("Hashed password: ", hash)

    try:
        # Once encrypted, save this new hashed password to DB
        cur.execute("UPDATE customer SET c_password = %s WHERE c_email = 'javier.quinones3@upr.edu' ", hash)
        conn.commit()
        return 1

    except pymysql.Error as error:
        print(error)
        return 0

    else:
        cur.close()
        return 1


