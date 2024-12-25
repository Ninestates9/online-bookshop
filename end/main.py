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
        sql = f"select Ano, Aname, sort from easier_write where Bno = '{Bno}' and Bsubno = {Bsubno} order by sort asc;"
        p_cursor.execute(sql)
        result = p_cursor.fetchall()
        authors = []
        for row in result:
            authors.append(row[1])
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
    sql = f"select Ano, Aname, sort from easier_write where Bno = '{p_Bno}' and Bsubno = {p_Bsubno} order by sort asc;"
    p_cursor.execute(sql)
    result = p_cursor.fetchall()
    authors = []
    for row in result:
        authors.append(row[1])
    book["authors"] = authors
    sql = f"select keyword from easier_tags where Bno = '{p_Bno}' and Bsubno = {p_Bsubno};"
    p_cursor.execute(sql)
    result = p_cursor.fetchall()
    keys = []
    for row in result:
        keys.append(row[0])
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
    sql = f"select Ono from order where Uno = '{Uno}' and state in('submitted', 'sending', 'finished');"
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
    books = []
    conn, cursor = connectSQL()
    type = request.form.get("type")
    content = request.form.get("content")
    if content[0] == '!':
        if type == "Bno":
            sql = f"call searchBookBy{type}('{content}');"
        elif type[-1].isdigit():
            number = type[-1]
            type =  type[:-1]
            sql = f"call ssearchBookBy{type}('{content}', {number});"
        else:
            content = content[1:]
            sql = f"call ssearchBookBy{type}('{content}');"
    elif type[-1].isdigit():
        number = type[-1]
        type =  type[:-1]
        sql = f"call searchBookBy{type}('{content}', {number});"
    else:
        sql = f"call searchBookBy{type}('{content}');"
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        books.append(getBookInfo(cursor, row[0], row[1]))
    data = {"ret":0, "books":books}
    closeSQL(conn, cursor)
    return jsonify(data)

@app.route('/api/submitShoppingCart', methods=["GET", "POST"])
def submitShoppingCart():
    conn, cursor = connectSQL()
    Uno = request.form.get("Uno")
    books = request.form.get("books")
    sql = f"insert into order(Uno, state) values('{Uno}', 'new');select Ono from order where state = 'new';"
    cursor.execute(sql)
    Ono = cursor.fetchone()[0]
    for book in books:
        Bno = book[0]
        Bsubno = book[1]
        orderNumber = book[2]
        sql = f"insert into ob(Bno, Bsubno, Ono, orderNumber) values('{Bno}', {Bsubno}, {Ono}, {orderNumber});"
        cursor.execute(sql)
    sql = f"update order set state = 'shopping' where Ono = {Ono}"
    cursor.execute(sql)
    data = {"ret":0, "Ono":Ono}
    closeSQL(conn, cursor)
    return jsonify(data)

@app.route('/api/getShoppingCart', methods=["GET", "POST"])
def getShoppingCart():
    conn, cursor = connectSQL()
    Uno = request.form.get("Uno")
    sql = f"select Ono from order where Uno = '{Uno}' and state = 'shopping'"
    cursor.execute(sql)
    Ono = cursor.fetchone()[0]
    books = getOrderBook(cursor, Ono)
    data = {"ret":0, "books":books}
    closeSQL(conn, cursor)
    return jsonify(data)

@app.route('/api/submitOrder', methods=["GET", "POST"])
def submitOrder():
    conn, cursor = connectSQL()
    Ono = request.form.get("Ono")
    sql = f"update order set state = 'submitted' where Ono = {Ono}"
    cursor.execute(sql)
    data = {"ret":0}
    closeSQL(conn, cursor)
    return jsonify(data)

@app.route('/api/getUserInfo', methods=["GET", "POST"])
def getUserInfo():
    userInfo = []
    conn, cursor = connectSQL()
    sql = f"select Uno, Uname, level, address, balance, total from user where left(Uno, 1) = 'U';"
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        user = {"Uno":row[0], "Uname":row[1], "level":row[2], "address":row[3], "balance":row[4], "total":row[5]}
        userInfo.append(user)
    data = {"ret":0, "userInfo":userInfo}
    closeSQL(conn, cursor)
    return jsonify(data)

@app.route('/api/getMsg', methods=["GET", "POST"])
def getMsg():
    messageSet = []
    conn, cursor = connectSQL()
    sql = f"select Uno, message from user where message is not null;"
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        message = {"Uno":row[0], "message":row[1]}
        messageSet.append(message)
    data = {"ret":0, "messageSet":messageSet}
    closeSQL(conn, cursor)
    return jsonify(data)

@app.route('/api/getOrders', methods=["GET", "POST"])
def getOrders():
    orders = []
    conn, cursor = connectSQL()
    sql = f"select Ono, Uno, totalMoney, deliveryAddress, state, orderTime from order where state in('submitted', 'delivery');"
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        books = getOrderBook(cursor, row[0])
        order = {"Ono":row[0],
                "Uno":row[1],
                "books":books,
                "totalMoney":row[2], 
                "deliveryAddress":row[3], 
                "state":row[4], 
                "orderTime":row[5]}
        orders.append(order)
    data = {"ret":0, "orders":orders}
    closeSQL(conn, cursor)
    return jsonify(data)

@app.route('/api/getBooks', methods=["GET", "POST"])
def getBooks():
    books = []
    conn, cursor = connectSQL()
    sql = f"select Bno, Bsubno from book;"
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        book = getBookInfo(cursor, row[0], row[1])
        books.append(book)
    data = {"ret":0, "books":books}
    closeSQL(conn, cursor)
    return jsonify(data)

@app.route('/api/getShortage', methods=["GET", "POST"])
def getShortage():
    shortageSet = []
    conn, cursor = connectSQL()
    sql = f"select Sno, Bno, Bsubno, Uno, insufficientNumber, purchaseTime from shortage;"
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        sql = f"select Bname from book where Bno = '{row[1]}' and Bsubno = {row[2]};"
        cursor.execute(sql)
        res = cursor.fetchone()[0]
        shortage = {"Sno":row[0], 
                    "Bno":row[1], 
                    "Bsubno":row[2], 
                    "Bname":res,
                    "Uno":row[3], 
                    "insufficientNumber":row[4], 
                    "purchase":row[5]}
        shortageSet.append(shortage)
    data = {"ret":0, "shortageSet":shortageSet}
    closeSQL(conn, cursor)
    return jsonify(data)

@app.route('/api/getPurchase', methods=["GET", "POST"])
def getPurchase():
    purchase = []
    conn, cursor = connectSQL()
    sql = f"select distinct(Pno) from shortage where Pno is not null order by Pno desc;"
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        sql = f"select Sno from shortage where Pno = {row[0]};"
        cursor.execute(sql)
        SnoSet = cursor.fetchall()
        SnoSet = [item[0] for item in SnoSet]
        purchase.append({"Pno":row[0], "SnoSet":SnoSet})
    data = {"ret":0, "purchase":purchase}
    closeSQL(conn, cursor)
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)