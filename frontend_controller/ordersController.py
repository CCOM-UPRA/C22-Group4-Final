from frontend_model.ordersModel import *

def getOrdersAndProductsController():
    return getOrdersAndProductsModel()

def updateOrdersController():
    return updateOrdersModel()

def deleteOrderController(order_id):
    return deleteOrder(order_id)



