from werkzeug.utils import redirect
from App import app
import os
from flask_cors import CORS
from flask import Flask,render_template, jsonify, request, redirect, url_for
from bson import ObjectId
from pymongo import MongoClient

client = MongoClient( 'localhost',27017)


db = client['MongoDb']

collection = db['cadastro']


print(client.list_database_names())


@app.route('/')
@app.route('/index')


def index():
    # Buscar todos os documentos na coleção
    documentos = list(collection.find())
    
    return render_template('index.html', documentos=documentos)


@app.route('/cadastro', methods=['POST'])
def cadastro():
    
    # Obter dados do formulário
    codigo = request.form['m-codigo']
    Nomecidade = request.form['m-Cidade']
    estado = request.form['m-Estado']

    # Inserir dados no MongoDB
    dados = {'m-codigo': codigo, 'm-Cidade': Nomecidade, 'm-Estado': estado}
    collection.insert_one(dados)

    return 'Cadastro realizado com sucesso!'


# Editar
@app.route('/editar/<string:documento_id>', methods=['POST'])

def editar(documento_id):
    # Connect to the MongoDB client and get the collection
    client = MongoClient('localhost', 27017)
    db = client['MongoDb']
    collection = db['cadastro']

    # Get the updated values for the document from the form data
    codigo = request.form['m-codigo']
    Nomecidade = request.form['m-Cidade']
    estado = request.form['m-Estado']

    # Update the document in the collection
    result = collection.update_one(
        {'_id': ObjectId(documento_id)},
        {'$set': {'m-codigo': codigo, 'm-Cidade': Nomecidade, 'm-Estado': estado}}
    )

    # Redirect back to the index page
    return redirect('/')


@app.route('/excluir/<string:documento_id>', methods=['POST'])
def excluir(documento_id):
        
    result = collection.delete_one({'_id': ObjectId(documento_id)})
    return redirect('/')



@app.route('/update/<document_id>', methods=['POST'])
def update(document_id):
    # Get the updated values from the form data
    codigo = request.form['m-codigo']
    cidade = request.form['m-Cidade']
    estado = request.form['m-Estado']
    
    # Create an object with the updated data
    data = {
        'm-codigo': codigo,
        'm-Cidade': cidade,
        'm-Estado': estado
    }
    
    result = collection.update_one({'_id': ObjectId(document_id)}, {'$set': data})
    # Return a response
    if result.modified_count == 1:
        return 'Update successful', 200
    else:
        return 'Update failed', 400
  
# @app.route('/listagem')
# def listagem():
#     # Obter dados do MongoDB
#     dados = collection.find()
#     # Renderizar template com os dados
#     return render_template('listagem.html', dados=dados)


if __name__ == '__main__':
    app.run(debug=True)
