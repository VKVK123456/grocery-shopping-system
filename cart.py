from sql_connection import get_sql_connection
connection = get_sql_connection()
import datetime

class product_cart(connection.Model):
    id = connection.Column(connection.Integer, primary_key=True)
    name = connection.Column(connection.String(50))
    category = connection.Column(connection.String(50))
    price = connection.Column(connection.Float)
    image = connection.Column(connection.String(120))
    about = connection.Column(connection.String(50))
    cart = connection.relationship('Cart', backref="cart", lazy=True)
  
    def toDict(self):
      return{
        'id':self.id,
        'name':self.name,
        'category':self.category,
        'price':self.price,
        'image':self.image,
        'about':self.about,
        'cart':[ product_cart.toDict() for product in self.products]
      }

class Cart(connection.Model):
    id = connection.Column(connection.Integer, primary_key=True)
    quantity = connection.Column(connection.Integer)
    product_id = connection.Column(connection.Integer, connection.ForeignKey('product_cart.id'))

    def toDict(self):
      return{
        'id':self.id,
        'quantity':self.quantity,
        'product_id':self.product_id,
        'product':self.product_cart.toDict()
      }