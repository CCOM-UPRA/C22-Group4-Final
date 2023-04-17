from flask import Flask, render_template, redirect, request, session
from frontend_controller.cartController import *
from frontend_controller.checkoutController import *
from frontend_controller.invoiceController import *
from frontend_controller.loginController import *
from frontend_controller.ordersController import *
from frontend_controller.profileController import *
from frontend_controller.shopController import *
import decimal

app = Flask(__name__, template_folder='frontend/')
app.secret_key = 'akeythatissecret'

contador = 2

# In this template, you will usually find functions with comments tying them to a specific controller
# main.py accesses the frontend folders
# Every controller accesses its relevant model and will send the information back to this Flask app
# LOGIN INFO:
    # javier.quinones3@upr.edu (pass1234)


# Redirects us here if no url is given
@app.route("/", defaults={'message': None})
# Or if any url other than the ones set in this Flask application is provided, making it a <message>
@app.route("/<message>")
def enterpage(message):

    if message is None:
        return redirect("/shop")
    elif message == 'enter':
        return render_template('login (2).html')
    else:
        return render_template('login (2).html', message=message)


@app.route("/change")
def change():
    # An optional function for students to hash a specific password
    # changePass function can be found in profileController
    # Access this function by typing the word 'change' after your Flask url
    # http://127.0.0.1:5000/change
    changePass()
    return render_template("login (2).html")


@app.route("/clear")
def clear():
    # Whenever you wish to log out or clear the session info, you can type /clear at the end of the Flask address
    session.clear()
    return redirect("/")


@app.route("/login", methods=['POST'])
def login():
    # Enters here when logging in
    email = request.form.get('email')
    passcode = request.form.get('password')
    # Receive your login information and send to the loginController's logincontroller()
    return logincontroller(email=email, password=passcode)


@app.route("/register/", defaults={'message': None})
@app.route('/register/<message>')
def register(message):

    return render_template('register.html', message=message)


@app.route("/registerinfo", methods=['POST'])
def registerinfo():
    # Process the register info
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')
    pass1 = request.form.get('pass1')
    phonenumber = request.form.get('phone')
    address = request.form.get('address')
    address2 = request.form.get('address2')
    city = request.form.get('city')
    state = request.form.get('state')
    zipCode = request.form.get('zipcode')
    cardName = request.form.get('cardname')
    cardType = request.form.get('cardtype')
    expDate = request.form.get('expdate')
    cardNumber = request.form.get('cardnumber')
    
    conn = pymysql.connect(host='sql9.freemysqlhosting.net', db='sql9607922',
                           user='sql9607922', password='d7cwbda3De', port=3306)
    cur = conn.cursor()

    # Check if the user already exists in the database
    query = f"SELECT c_id FROM customer WHERE c_email='{email}'"
    cur.execute(query)
    result = cur.fetchone()
    
    if result:
        # User already exists, so do not proceed with registration
        return redirect('/login?message=This email is already registered. Please try with a different email.')

    else:
        # User does not exist, so proceed with registration
        # Get the next available customer id from the database
        query = "SELECT MAX(c_id) FROM customer"
        cur.execute(query)
        result = cur.fetchone()
        next_id = result[0] + 1 if result[0] else 1

        # Insert the new customer into the database
        pass1 = sha256_crypt.encrypt(pass1)
        query = f"INSERT INTO customer(c_id, c_name, c_last_name, c_email, c_password, c_phone_number, c_address_line1, c_address_line2, c_city, c_state, c_zipcode, c_card_name, c_card_type, c_exp_date, c_card_num) VALUES ({next_id},'{fname}','{lname}','{email}','{pass1}',{phonenumber},'{address}','{address2}','{city}','{state}',{zipCode},'{cardName}','{cardType}','{expDate}',{cardNumber})"
        cur.execute(query)
        conn.commit()

        # Log in the new user
        if logincontroller2(email=email, password=pass1):
            return redirect('/login?message=You have created a new account.')
        else:
            return redirect('/shop')



@app.route("/shop")
def shop():
    # First we receive the list of products by accessing getProducts() from shopController
    products = getProducts()

    # Then we create the shopping cart by accessing getCart in shopController
    getCart()

    # Find the different filter options for the products by accessing the functions from shopController
    brands = getBrands()

    # Redirect to shop page with the variables used
    return render_template("shop-4column.html", products=products, brands=brands)
                        #    colors=colors, videores=videores, wifi=wifi)


@app.route("/profile")
def profile():
    # To open the user's profile page
    # Get user info from getUser() in profileController
    user = getUser()

    # Since I specified the variable as user1, that is how it will be called on the html page
    return render_template("profile.html", user=user)


@app.route("/editinfo", methods=["POST"])
def editinfo():
    # If editing phone_number, edit phone_number -> profileController
    if 'number' in request.form:
        number = request.form.get('number')
        editnumbercontroller(number)

    # If editing address info, edit address -> profileController
    elif 'aline1' in request.form:
        aline1 = request.form.get('aline1')
        aline2 = request.form.get('aline2')
        state = request.form.get('state')
        zipcode = request.form.get('zipcode')
        city = request.form.get('city')

        editaddresscontroller(aline1, aline2, state, zipcode, city)

    # If editing payment info -> profileController
    elif 'card_name' in request.form:
        name = request.form.get('card_name')
        c_type = request.form.get('card_type')
        exp_date = request.form.get('date')
        number = request.form.get('card_num')
        editpaymentcontroller(name, c_type, number, exp_date)

    # If editing main info -> profileController
    elif 'fname' in request.form:
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        editprofilecontroller(fname, lname, email)

    # Checks if you're editing from your profile page or your checkout page
    if 'profile' in request.form:
        return redirect("/profile")
    elif 'checkout' in request.form:
        return redirect("/checkout")


@app.route("/password")
def password():
    # pass1 = request.form.get('pass1')
    # if pass1 != session[4]:

    return render_template("change-password.html")

@app.route('/editpassword', methods=['POST'])
def editpassword():
    email = request.form.get('email_o')
    old_password = request.form.get('pass_o')
    new_password = request.form.get('pass_n')
    new_password_confirm = request.form.get('pass_n1')

    conn = pymysql.connect(host='sql9.freemysqlhosting.net', db='sql9607922',
                           user='sql9607922', password='d7cwbda3De', port=3306)
    cur = conn.cursor()
    cur.execute(f"SELECT c_password from customer WHERE c_email = '{email}'")
    customer_data = cur.fetchone()[0]

    if sha256_crypt.verify(old_password, customer_data):

        if new_password == new_password_confirm:
                # Update the password in the database
                # Hashing the password
                new_password_hash = sha256_crypt.hash(new_password)
                cur.execute(f"UPDATE customer SET c_password='{new_password_hash}' WHERE c_email='{email}'")
                conn.commit()
                return redirect('/profile')
        else:
            return redirect('/password?error=1')
    else:
        return redirect('/password?error=2')






@app.route("/orders")
def orders():
    # TO BE CONNECTED TO MYSQL BY STUDENTS
    # Redirects us to the orders list page of the user
    # Fetches each order and its products from ordersController
    order1 = getorder1()
    products1 = getorder1products()
    order2 = getorder2()
    products2 = getorder2products()

    return render_template("orderlist.html", order1=order1, products1=products1, order2=order2, products2=products2)


@app.route("/addcart", methods=["POST"])
def addcart():
    # Get the relevant info for product to add to cart
    p_id = request.form.get('p_id')
    name = request.form.get('name')
    image = request.form.get('image')
    price = request.form.get('price')
    quantity = request.form.get('quantity')
    total = float(price) * int(quantity)
    # Find the add cart function in cartController
    addCartController(p_id, name, image, price, quantity, total)
    # request.referrer means you will be redirected to the current page you were in
    return redirect(request.referrer)


@app.route("/delete/<int:id>")
def delete(id):
    deleteCartItem(item_id = id)
    return redirect(request.referrer)



@app.route("/editcart", methods=["POST"])
def editcart():
    id = request.form.get("id")
    print("Este debe ser el id:",id)
    quantity = request.form.get("quantity")
    print("This is the amount:", quantity)
    editCartModel(id=id, quantity=quantity)
    return redirect(request.referrer)


@app.route("/checkout/", defaults={'message': None})
@app.route("/checkout/<message>")
def checkout(message):
    # Check if customer is logged in
    if 'customer' in session:
        # > profileController
        user = getUser()

        return render_template("checkout.html", user=user, message=message)

    else:
        # If customer isn't logged in, create session variable to tell us we're headed to checkout
        # Redirect us to login with message
        session['checkout'] = True
        return redirect("/wrong")


@app.route("/validate")
def validate():
    # Validates whether all user info is complete before processing the checkout
    # -> checkoutController
    return validateUserCheckout()


@app.route("/invoice")
def invoice():
    # TO BE CONNECTED TO MYSQL BY STUDENTS
    # > invoiceController
    order = getOrder()
    products = getOrderProducts()
    # Total amount of items in this simulated order:
    amount = 3
    return render_template("invoice.html", order=order, products=products, amount=amount)


from flask import request

@app.route("/filter")
def filter():
    # Guarda el tipo de boton que fue presionado
    filter_type = request.args.get("filter_type")

    if filter_type == "brand":
        # Si el producto tiene el mismo brand que el usuario selecciono, guardalo en filtered_products
        selected_brands = request.args.getlist("brand")
        filtered_products = [p for p in getProducts() if p["brand"] in selected_brands]
    elif filter_type == "price":
        # Si el producto tiene un precio entre esos dos valores que el usuario selecciono, guardalo en filtered_products
        min_price = float(request.args.get("min_price", 0))
        max_price = float(request.args.get("max_price", float("inf")))
        filtered_products = [p for p in getProducts() if min_price <= float(p["price"]) <= max_price]
    else:
        # Si el usuario presiono filter by all muestra todos los productos
        filtered_products = getProducts()
    return render_template("shop-4column.html", products=filtered_products, brands=getBrands())







# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/