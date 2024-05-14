from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
db = SQLAlchemy(app)

# Modelagem
# Produtp (id, name, preice, description)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)#Eu não quero que ela possa ser nula
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)

#Roda de adicionar um produto
@app.route('/api/products/add', methods=["POST"])
def add_product():
    data = request.json 
    if 'name' in data and 'price' in data:
        product = Product(name=data["name"], price=data["price"], description=data.get("description", ""))
        db.session.add(product)
        db.session.commit()
        return  jsonify({'message': "Product added successfully"})
    return jsonify({'message': "Invalid product data"}), 400

#Roda de remover produto
@app.route('/api/products/delete/<int:product_id>', methods=["DELETE"])
def delete_product(product_id):
    # Recuperar o produto da base de dados 
    product = Product.query.get(product_id)
    if product: 
        db.session.delete(product)
        db.session.commit()
        return  jsonify({'message': "Product deleted successfully"})
    return jsonify({'message': "Proct not found"}), 404
        

    # Verificar se o produto existe
    # Se existe apagar da base de dados 
    # se não existe retornar 404 not found 


# Definir uma rota raiz(página inicial) e a função que será executada ao requisitar
@app.route('/')
def hello_word():
    return 'Hello World Robson de Jesus'

if __name__ == "__main__":
    app.run(debug=True)