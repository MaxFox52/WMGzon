class Product:
    def toDic(self):
        return {'id':self.id,
                'product_name':self.product_name,
                'storage_sizes':self.storage_sizes,
                'colours':self.colours,
                'description': self.description,
                'imageid': self.imageid,
                'product_type': self.product_type,
                'price': self.price,
                'sellerid': self.sellerid,
                'rating': self.rating }
    
    @staticmethod
    def populate(row):
        aProduct = Product()
        aProduct.id = row.get('id')
        aProduct.product_name = row.get('product_name')
        aProduct.storage_sizes = row.get('storage_sizes')
        aProduct.colours = row.get('colours')
        aProduct.description = row.get('description')
        aProduct.imageid = row.get('imageid')
        aProduct.product_type = row.get('product_type')
        aProduct.price = row.get('price')
        aProduct.sellerid = row.get('sellerid')
        aProduct.rating = row.get('rating')

        return aProduct