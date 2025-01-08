from ext import app,db
from models import Products,Users
from uuid import uuid4

with app.app_context():
    db.drop_all()
    db.create_all()

    usr = Users(name="Admin",
                password="12341234",
                id=str(uuid4().int),
                email="support@bibo.zip",
                birthdate="12-12-2000",
                cart="[]",
                rank=1
                )

    for i in range(0,60):
        product = Products(
            name = "Lorem ipsum",
            price = "5000",
            image = "static/productIMGS/img.png",
            id = str(uuid4().int),
            description = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            tag="carousel",
            likes="[]",
            reviews="[]",
            author = usr.id
        )
        db.session.add(product)


    db.session.add(usr)

    db.session.commit()