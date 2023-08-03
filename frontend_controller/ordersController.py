from frontend_model.ordersModel import *

def getOrdersAndProductsController(order_id):
    return getOrdersAndProductsModel(order_id)

def updateOrdersController():
    return updateOrdersModel()

def deleteOrderController(order_id):
    return deleteOrder(order_id)



