from flask import Flask, request
from config.database import get_connection, pool


app = Flask(__name__)


@app.route("/create", methods=['POST'])
def create():
    body = request.json
    categoria = body.get('categoria')
    produto = body.get('produto')
    quantidade = body.get('quantidade')
    sql = "INSERT INTO produtos (categoria, produto, quantidade) VALUES (%s, %s, %s)"
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql, (categoria, produto, quantidade))
    connection.commit()
    cursor.close()
    pool.putconn(connection)

    return {"message": "Produto adicionado"}, 201


@app.route("/delete", methods=['DELETE'])
def delete():
    body = request.json
    produto = body.get('produto')
    sql = "DELETE FROM produtos WHERE produto like %s"
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql, (produto,))
    connection.commit()
    cursor.close()
    pool.putconn(connection)

    return {"message": "Produto deletado"}, 200


@app.route("/")
def read_all():
    sql = "select * from produtos;"
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql)
    produtos = cursor.fetchall()
    return produtos


@app.route("/read_one")
def read_one():
    body = request.json
    produto = body.get('produto')
    sql = "SELECT quantidade FROM produtos WHERE produto=%s;"
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql, (produto,))
    resultado = cursor.fetchall()
    return resultado


@app.route("/update", methods=['PUT'])
def update():
    body = request.json
    produto = body.get('produto')
    quantidade = body.get('quantidade')
    sql = "UPDATE produtos SET quantidade=%s WHERE produto=%s"
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql, [quantidade, produto])
    connection.commit()
    cursor.close()
    pool.putconn(connection)

    return {"message": "Quantidade Atualizada"}, 200


@app.route('/update_add', methods=['PUT'])
def update_add():
    produto_add = request.json['produto']
    quantidade = request.json['quantidade']
    sql= "SELECT quantidade FROM produtos WHERE produto = %s"
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql,[produto_add])
    produto_quantidade = cursor.fetchone()[0]
    produto_quantidade += quantidade
    sql_add= "UPDATE produtos SET quantidade = %s WHERE produto = %s"
    cursor.execute(sql_add, [produto_quantidade,produto_add,])
    connection.commit()
    cursor.close()
    pool.putconn(connection)

    return {"message": "Quantidade Acrescentada"}, 200
