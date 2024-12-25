from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
# import cv2
import os
import numpy as np
import re
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
CORS(app, resource={r'/*': {'origins': '*'}})

def connectSQL(p_user = 'root', p_db = 'online_bookshop'):
    f_conn = pymysql.connect(
        host='127.0.0.1', 
        port=3306, 
        user=p_user, 
        password='123456', 
        charset='utf8', 
        autocommit=True
    )
    f_cursor = f_conn.cursor()
    f_cursor.execute("use " + p_db)
    return f_conn, f_cursor

def closeSQL(p_conn, p_cursor):
    p_cursor.close()
    p_conn.close()

def getOrderBook(p_cursor, p_Ono):
    sql = f"select Bno, Bsubno, orderNumber from ob where Ono = {p_Ono};"
    p_cursor.execute(sql)
    result_out = p_cursor.fetchall()
    books = []
    for row_out in result_out:
        Bno = row_out[0]
        Bsubno = row_out[1]
        orderNumber = row_out[2]
        sql = f"select Bname, press, price from book where Bno = {Bno} and Bsubno = {Bsubno};"
        p_cursor.execute(sql)
        result = p_cursor.fetchone()
        Bname = result[0]
        press = result[1]
        price = result[2]
        total = orderNumber * price 
        sql = f"select Ano, sort from write where Bno = '{Bno}' and Bsubno = {Bsubno} order by sort asc;"
        p_cursor.execute(sql)
        result = p_cursor.fetchall()
        authors = []
        for row in result:
            sql = f"select Aname from author where Ano = {row[0]};"
            p_cursor.execute(sql)
            result = p_cursor.fetchone()
            authors.append(result[0])
        book = {"Bname":Bname, "authors":authors, "press":press, "price":price, "orderNumber":orderNumber, "total":total}
        books.append(book)
    return books

def getBookInfo(p_cursor, p_Bno, p_Bsubno):
    book = {}
    book["Bno"] = p_Bno
    book["p_Bsubno"] = p_Bsubno    
    sql = f"select Bname, press, price, quantity, cover, catalog, position from book where Bno = '{p_Bno}' and Bsubno = {p_Bsubno};"
    p_cursor.execute(sql)
    result = p_cursor.fetchone()
    book["Bname"] = result[0]
    book["press"] = result[1]
    book["price"] = result[2]
    book["quantity"] = result[3]
    book["cover"] = result[4]
    book["catalog"] = result[5]
    book["position"] = result[6]
    sql = f"select Ano, sort from write where Bno = '{p_Bno}' and Bsubno = {p_Bsubno} order by sort asc;"
    p_cursor.execute(sql)
    result = p_cursor.fetchall()
    authors = []
    for row in result:
        sql = f"select Aname from author where Ano = {row[0]};"
        p_cursor.execute(sql)
        result = p_cursor.fetchone()
        authors.append(result[0])
    book["authors"] = authors
    sql = f"select Kno from tags where Bno = '{p_Bno}' and Bsubno = {p_Bsubno};"
    p_cursor.execute(sql)
    result = p_cursor.fetchall()
    keys = []
    for row in result:
        sql = f"select keyword from keywords where Kno = {row[0]};"
        p_cursor.execute(sql)
        result = p_cursor.fetchone()
        keys.append(result[0])
    book["keys"] = keys
    return book

# 用户登录与注册
@app.route('/api/signIn', methods=["GET", "POST"])
def signIn():
    conn, cursor = connectSQL()
    Uno = request.form.get("Uno")
    password = request.form.get("password")
    sql = f"select password from user where Uno = '{Uno}';"
    cursor.execute(sql)
    result = cursor.fetchone()
    if result == None:
        data = {"ret": 1, "msg": "用户名不存在！"}
    elif password != result[0]:
        data = {"ret": 1, "msg": "密码错误！"}
    else:
        data = {"ret": 0, "type":Uno[0]}
    closeSQL(conn, cursor)
    return jsonify(data)

@app.route('/api/signUp', methods=["GET", "POST"])
def signUp():
    conn, cursor = connectSQL()
    Uno = request.form.get("Uno")
    password = request.form.get("password")
    Uname = request.form.get("Uname")
    sql = f"select Uno from user where Uno = '{Uno}';"
    cursor.execute(sql)
    result = cursor.fetchone()
    if result != None or Uno == "S00000":
        data = {"ret": 1, "msg": "用户名已存在！"}
    else:
        sql = f"insert into user(Uno, password, Uname) values('{Uno}', '{password}', '{Uname}');"
        cursor.execute(sql)
        data = {"ret": 0}
    closeSQL(conn, cursor)
    return jsonify(data)

@app.route('/api/getInfo', methods=["GET", "POST"])
def getInfo():
    conn, cursor = connectSQL()
    Uno = request.form.get("Uno")
    sql = f"select * from u_user where Uno = '{Uno}';"
    cursor.execute(sql)
    result = cursor.fetchone()
    if result == None:
        data = {"ret": 1, "msg": "用户不存在！"}
    else:
        info = {"Uno":result[0], "Uname":result[2], "level":result[3], "address":result[4], "balance":result[5]}
        data = {"ret": 0, "info":info}
    closeSQL(conn, cursor)
    return jsonify(data)

@app.route('/api/updateInfo', methods=["GET", "POST"])
def updateInfo():
    conn, cursor = connectSQL()
    Uno = request.form.get("Uno")
    password = request.form.get("password")
    Uname = request.form.get("Uname")
    address = request.form.get("address")
    sql = f"select Uno from u_user where Uno = '{Uno}';"
    cursor.execute(sql)
    result = cursor.fetchone()
    if result == None:
        data = {"ret": 1, "msg": "用户不存在！"}
    else:
        sql = f"update u_user set password = '{password}', Uname = '{Uname}', address = '{address}' where Uno = '{Uno}';"
        cursor.execute(sql)
        data = {"ret": 0}
    closeSQL(conn, cursor)
    return jsonify(data)

@app.route('/api/pre_pay', methods=["GET", "POST"])
def pre_pay():
    conn, cursor = connectSQL()
    Uno = request.form.get("Uno")
    money = request.form.get("money")
    sql = f"select Uno from u_user where Uno = '{Uno}';"
    cursor.execute(sql)
    result = cursor.fetchone()
    if result == None:
        data = {"ret": 1, "msg": "用户不存在！"}
    else:
        sql = f"update u_user set balance = balance + {money} where Uno = '{Uno}';"
        cursor.execute(sql)
        data = {"ret": 0}
    closeSQL(conn, cursor)
    return jsonify(data)

@app.route('/api/sendMsg', methods=["GET", "POST"])
def sendMsg():
    conn, cursor = connectSQL()
    Uno = request.form.get("Uno")
    message = request.form.get("message")
    sql = f"select Uno from u_user where Uno = '{Uno}';"
    cursor.execute(sql)
    result = cursor.fetchone()
    if result == None:
        data = {"ret": 1, "msg": "用户不存在！"}
    else:
        sql = f"update u_user set message = '{message}' where Uno = '{Uno}';"
        cursor.execute(sql)
        data = {"ret": 0}
    closeSQL(conn, cursor)
    return jsonify(data)

@app.route('/api/getHistory', methods=["GET", "POST"])
def getHistory():
    conn, cursor = connectSQL()
    Uno = request.form.get("Uno")
    sql = f"select Ono from history where Uno = '{Uno}';"
    cursor.execute(sql)
    result = cursor.fetchall()
    if result == None:
        data = {"ret": 1, "msg": "用户没有历史订单！"}
    else:
        orders = []
        for row in result:
            sql = f"select totalMoney, deliveryAddress, state, orderTime from order where Ono = '{row[0]}';"
            cursor.execute(sql)
            result = cursor.fetchone()
            totalMoney = result[0]
            deliveryAddress = result[1]
            state = result[2]
            orderTime = result[3]
            books = getOrderBook(cursor, row[0])
            order = {"books":books, "totalMoney":totalMoney, "deliveryAddress":deliveryAddress, "state":state, "orderTime":orderTime}
            orders.append(order)
        data = {"ret": 0, "orders":orders}
    closeSQL(conn, cursor)
    return jsonify(data)

@app.route('/api/searchBooks', methods=["GET", "POST"])
def searchBooks():
    conn, cursor = connectSQL()
    type = request.form.get("type")
    content = request.form.get("content")
    sql = f"select Ono from history where Uno = '{Uno}';"
    cursor.execute(sql)
    result = cursor.fetchall()
    if result == None:
        data = {"ret": 1, "msg": "用户没有历史订单！"}
    else:
        orders = []
        for row in result:
            sql = f"select totalMoney, deliveryAddress, state, orderTime from order where Ono = '{row[0]}';"
            cursor.execute(sql)
            result = cursor.fetchone()
            totalMoney = result[0]
            deliveryAddress = result[1]
            state = result[2]
            orderTime = result[3]
            books = getOrderBook(cursor, row[0])
            order = {"books":books, "totalMoney":totalMoney, "deliveryAddress":deliveryAddress, "state":state, "orderTime":orderTime}
            orders.append(order)
        data = {"ret": 0, "orders":orders}
    closeSQL(conn, cursor)
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)