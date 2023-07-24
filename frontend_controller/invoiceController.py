from frontend_model.invoiceModel import *

def getOrder(order_id):
    return getOrderModel(order_id)


def getOrderProducts(cart):
    return getProductsModel(cart)
