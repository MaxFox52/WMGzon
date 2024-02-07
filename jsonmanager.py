from datamanager import DataManager
import json

class ProductManager(DataManager):
    JSON_FILE = "static/Products.json"

    def __init__(self):
        self.__products = self.loadData()

    def loadData(self):
        with open(ProductManager.JSON_FILE) as f:
            return json.load(f)
        
    def saveData(self, products):
        with open(ProductManager.JSON_FILE, 'w') as f:
            json.dump(products, f) 
        
    def insertProduct(self, aProduct):
        aProduct.id = self.__products[0]['id'] + 1
        self.__products.insert(0, aProduct.toDic())
        self.saveData(self.__products)
        
    def updateProduct(self, indexID, aProduct):
        for _idx, _product in enumerate(self.__products):
            if indexID == _product['id']:
                self.__products[_idx] = aProduct.toDic()
        self.saveData(self.__products)

    def deleteProduct(self, indexID):
        for _idx, _product in enumerate(self.__products):
            if indexID == _product['id']:
                del self.__products[_idx]
        self.saveData(self.__products)

    def getProducts(self):
        return self.__products

    def getProduct(self, indexID):
        for _idx, _product in enumerate(self.__products):
            if indexID == _product['id']:
                self.saveData(self.__products)
                return _product
        return None