from app import db, create_app, bcrypt
import app.models.farmer as farmerModel

# class Tests(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(120), nullable=False)
#     description = db.Column(db.String(120), nullable=True)


app = create_app()


# def create_user(username, password):
#     with app.app_context():
#         password_hash = bcrypt.generate_password_hash(password)
#         user = model.Users(username = username, password_hash = password_hash)
#         db.session.add(user)
#         db.session.commit()
    

# def create():
#     with app.app_context():
#         db.create_all()

# def addToDb():
#     with app.app_context():
        
#         categories = model.Categories(
#             name = 'Molido'
#         )

#         products = model.Products(
#             category_id = 1,
#             name = 'Cafe 250gr',
#             price = 15000
#         )

#         inventories = model.Inventories(
#             product_id = 1,
#             quantity = 2
#         )

#         sales = model.Sales(
#             product_id = 1,
#             quantity = 10,
#             price = 20000,
#             total_price = 200000
#         )

#         db.session.add(categories)
#         db.session.add(products)
#         # db.session.add(inventories)
#         # db.session.add(sales)
#         db.session.commit()




def temp():
    # pass
    with app.app_context():
        farmer = farmerModel.Farmers()
        # products = model.Products.query.all()

        # for product in products:
        #     print(product.inventory.quantity)



if __name__ == '__main__':
    create_user('Juan','juan')
