from abc import ABC, abstractmethod

class DataManager(ABC):
    @abstractmethod
    def insertProduct(self, aProduct):
        pass

    @abstractmethod
    def updateProduct(self, indexID, aProduct):
        pass

    @abstractmethod
    def deleteProduct(self, indexID):
        pass

    @abstractmethod
    def getProducts(self):
        pass

    @abstractmethod
    def getProduct(self, indexID):
        pass