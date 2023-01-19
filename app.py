from flask import Flask, request
from config.database import get_connection, pool


app = Flask(__name__)

@app.route("/produtos", methods=['POST'])
def create():
    body = request.json
    categoria = body.get('categoria')
    produto = body.get('produto')
    quantidade = body.get('quantidade')
    sql =  "INSERT INTO produtos (categoria, produto, quantidade) VALUES (%s, %s, %s)"
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql, (categoria, produto, quantidade))
    connection.commit()
    cursor.close()
    pool.putconn(connection)
    
    return {"message":"Produto adicionado"}, 201

@app.route("/delete", methods=['DELETE'])
def delete():
    body = request.json
    produto = body.get('produto')
    sql =  "DELETE FROM produtos WHERE produto like %s"
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql,(produto,))
    connection.commit()
    cursor.close()
    pool.putconn(connection)
    
    return {"message":"Produto deletado"}, 200



@app.route("/")
def read_all():
    sql = "select * from produtos;"
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql)
    produtos = cursor.fetchall()
    return produtos


@app.route("/update", methods=['PUT'])
def update():
    body = request.json
    produto = body.get('produto')
    quantidade = body.get('quantidade')
    sql =  "UPDATE produtos SET quantidade=%s WHERE produto=%s"
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql, [quantidade,produto])
    connection.commit()
    cursor.close()
    pool.putconn(connection)
    
    return {"message":"Quantidade Atualizada"}, 200
