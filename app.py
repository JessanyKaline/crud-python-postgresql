from flask import Flask, request, jsonify
from config.database import get_connection, pool
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/create", methods=['POST'])
def create():
    try:
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

        response = jsonify({"message": "Produto adicionado com sucesso"})     
        return response
    except Exception as e:
        print (e)
        return {"message": str(e)}, 500


@app.route("/delete", methods=['DELETE'])
def delete():
    try:
        body = request.json
        produto = body.get('produto')
        sql = "DELETE FROM produtos WHERE produto like %s"
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (produto,))
        connection.commit()
        cursor.close()
        pool.putconn(connection)
    except Exception as e:
        return {"message": f"Erro ao deletar o produto: {str(e)}"}, 500

    return {"message": "Produto deletado"}, 200


@app.route("/")
def read_all():
    try:
        sql = "select * from produtos;"
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql)
        produtos = cursor.fetchall()
    except Exception as e:
        return {"message": f"Erro ao ler os produtos: {str(e)}"}, 500

    return produtos, 200


@app.route("/update", methods=['PUT'])
def update():
    try:
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

        return {"message": "Quantidade Total do Produto Atualizada"}, 200
    except Exception as e:
        return {"message": str(e)}, 500


@app.route('/update_add', methods=['PUT'])
def update_add():

    try:
        produto_add = request.json['produto']
        quantidade = request.json['quantidade']
        sql = "SELECT quantidade FROM produtos WHERE produto = %s"
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [produto_add])
        produto_quantidade = cursor.fetchone()[0]
        produto_quantidade += quantidade
        sql_add = "UPDATE produtos SET quantidade = %s WHERE produto = %s"
        cursor.execute(sql_add, [produto_quantidade, produto_add,])
        connection.commit()
        cursor.close()
        pool.putconn(connection)

        return {"message": "Quantidade Acrescentada"}, 200

    except Exception as e:
        return {"message": "Erro ao atualizar a quantidade do produto: {}".format(e)}, 500


@app.route('/update_sub', methods=['PUT'])
def update_sub():
    try:
        produto_sub = request.json['produto']
        quantidade = request.json['quantidade']
        sql = "SELECT quantidade FROM produtos WHERE produto = %s"
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, [produto_sub])
        produto_quantidade = cursor.fetchone()[0]
        if produto_quantidade < quantidade:
            return {"message": "Não é possível subtrair a quantidade informada, pois é maior do que a quantidade atual do produto"}, 400
        produto_quantidade -= quantidade
        sql_sub = "UPDATE produtos SET quantidade = %s WHERE produto = %s"
        cursor.execute(sql_sub, [produto_quantidade, produto_sub,])
        connection.commit()
        cursor.close()
        pool.putconn(connection)

        return {"message": "Quantidade Subtraída"}, 200

    except Exception as e:
        return {"message": "Erro ao subtrair a quantidade do produto: {}".format(e)}, 500
