class Product:
    def __init__(self, productId, productName, categoryPath, price):
        self.productId = productId
        self.productName = productName
        self.categoryPath = categoryPath
        self.price = price

    def print(self):
        print('productId:     '+str(self.productId) +'\n'+
              'productName:   '+self.productName +'\n'+
              'categoryPath:  '+self.categoryPath +'\n'+
              'price:         '+str(self.price) +'\n')