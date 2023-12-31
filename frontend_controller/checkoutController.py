from flask import url_for, redirect

from frontend_model.checkoutModel import *


def validateUserCheckout():
    # Find the user in DB via checkoutModel function
    user = validateUserModel()

    for u in user:
        # Check if a specific part is empty/null/0/etc and save the appropriate message to send back to checkout
        # Checkout will display an error message according to the variable 'message' if some info is missing
        # Otherwise, it will proceed to invoice
        if u['address_line1'] == "" or u['address_line2'] == "" or u['city'] == "" or u['state'] == "" or u['zipcode'] == "":
            message = "address"
            return redirect(url_for('checkout', message=message))
        elif u['phone_number'] == 0:
            message = "number"
            return redirect(url_for('checkout', message=message))
        elif u['card_name'] == "" or u['card_type'] == "" or u['exp_date'] is None or u['card_number'] == 0:
            message = "payment"
            return redirect(url_for('checkout', message=message))
        else:
            # Esto ocurre cuando presiono el boton de procede to checkout
            # Envio la informacion del usuario y el carrito de compras para subirlo a la base de datos
            cart = session.get('cart', {})  # Get the cart dictionary
            order_id = sendToDatabase(u, cart)

            return redirect(url_for('invoice', order_id=order_id))

def sendToDatabase(user,cart):
    return sendToDatabaseModel(user,cart)

    