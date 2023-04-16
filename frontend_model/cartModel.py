from flask import session

# Dictionary uniter
def MagerDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False



def getCartModel():
    # Initialize the amount and totaL for the cart
    session['amount'] = 0
    session['total'] = 0
    if 'cart' in session:
        for key, item in session['cart'].items():
            session['amount'] += int(item['quantity'])
            session['total'] += float(item['total_price'])
        return session['cart']
    else:
        print("CART NOT FOUND")
        return


def addCartModel(dictitems):
    # Add new product to cart using MagerDicts if cart already has items in
    if 'cart' in session:
        session['cart'] = MagerDicts(session['cart'], dictitems)
    else:
        session['cart'] = dictitems

    # Update the session variables with the new additions
    # Pointer: POST variables can sometimes end up returning strings, so we must type_cast our variables for the operations
    for key, item in dictitems.items():
        session['amount'] += int(item['quantity'])
        session['total'] += float(item['total_price'])
    return


def deleteCartItemModel(item_id):
    # Check if cart exists
    if 'cart' in session:

        # Check if the item exists in the cart with the ID
        if str(item_id) in session['cart']:
            # Updates before deleting the item from the cart
            item = session['cart'][str(item_id)]
            session['amount'] -= int(item['quantity'])
            session['total'] -= float(item['total_price'])

            # Remove the item from the cart
            del session['cart'][str(item_id)]

def editCartModel(id, quantity):
    if 'cart' in session:
        if id in session['cart']:
            print(session)
            item = session['cart'][id]
            old_quantity = int(item['quantity'])
            item['quantity'] = str(quantity)
            item['total_price'] = float(item['price']) * int(item['quantity'])
            session['amount'] += (int(item['quantity']) - old_quantity)
            session['total'] += (float(item['price']) * int(item['quantity']) - float(item['price']) * old_quantity)






