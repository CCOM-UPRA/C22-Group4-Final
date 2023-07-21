from frontend_model.cartModel import *


def getCart():
    # Go to cartModel to get cart items and session variables: total and quantity
    return getCartModel()


def addCartController(p_id, name, image, price, quantity, total, brand, category, pounds, stock):
    # Receive the variables that we got from POST originally and save in a dictItem to add to session cart
    # The add happens over at the cartModel
    dictitems = {p_id: {'name': name, 'image': image, 'price': price, 'quantity': int(quantity), 'brand': brand,
                       'total_price': int(total), 'category': category, 'pound': pounds, 'stock': stock}}

    return addCartModel(dictitems)

def editCartController(id, quantity):
    return editCartModel(id=id, quantity=quantity)
    

def deleteCartItem(item_id):
    return deleteCartItemModel(item_id)



