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
    # Check if the quantity of each product is available in the session cart
    if 'cart' in session:
        for key, item in dictitems.items():
            product_id = key
            amount_to_add = item['quantity']

            if key in session['cart']:
                current_quantity_in_cart = int(session['cart'][key]['quantity'])
                available_stock = int(session['cart'][key]['stock'])
                total_quantity_after_adding = current_quantity_in_cart + amount_to_add

                if total_quantity_after_adding > available_stock:
                    # Handle insufficient stock here
                    print(f"Insufficient stock for product with ID {product_id}. Available stock: {available_stock}, Requested quantity: {total_quantity_after_adding}")
                    return  # Return to stop the addition

    # If stock available, add new product to cart
    if 'cart' in session:
        for key, item in dictitems.items():
            if key in session['cart']:
                # Update the quantity if the product already exists in the cart
                session['cart'][key]['quantity'] += item['quantity']
                session['cart'][key]['total_price'] += item['total_price']
            else:
                session['cart'][key] = item
    else:
        session['cart'] = dictitems

    # Update the session 
    for key, item in dictitems.items():
        session['amount'] += item['quantity']
        session['total'] += item['total_price']

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






