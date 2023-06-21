import pymysql

# This is our simulation of the database
# We have two products here.
# The students must create their own productList when working on their eCommerce site
# Product images are loaded into static/images/product-images/
# Done in array instead of dictionaries to portray the differences

def getProductsModel():
    productList = []
    conn = pymysql.connect(host='sql9.freemysqlhosting.net', db='sql9607922',
                           user='sql9607922', password='d7cwbda3De', port=3306)
    cur = conn.cursor()
    cur.execute("SELECT * from products WHERE p_status = 'active'")
    results = cur.fetchall()
    for res in results:
        productList.append({
        'id': res[0],
        'name': res[1],
        'price': res[2],
        'cost': res[3],
        'stock': res[4],
        'brand': res[5],
        'pound': res[6],
        'description': res[7],
        'image': res[8],
        'category': res[9],
        'status': res[10]})
    return productList


def getBrandsModel():
    # Simulating grabbing these filters via SQL from the database
    brands = ["Higgins", "Tetra", "Purina"]
    return brands

def filterProductsModel(brand=None):
    productList = []
    conn = pymysql.connect(host='sql9.freemysqlhosting.net', db='sql9607922',
                           user='sql9607922', password='d7cwbda3De', port=3306)
    cur = conn.cursor()
    if brand:
        cur.execute("SELECT * from products WHERE p_status = 'active' AND brand = %s", (brand,))
    else:
        cur.execute("SELECT * from products WHERE p_status = 'active'")
    results = cur.fetchall()
    for res in results:
        productList.append({
        'id': res[0],
        'name': res[1],
        'price': res[2],
        'cost': res[3],
        'stock': res[4],
        'brand': res[5],
        'pound': res[6],
        'description': res[7],
        'image': res[8],
        'category': res[9],
        'status': res[10]})
    return productList
