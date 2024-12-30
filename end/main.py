from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pymysql
from PIL import Image
import json
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
        sql = f"select Bname, press, price from book where Bno = '{Bno}' and Bsubno = {Bsubno};"
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
        book = {"Bno":Bno, "Bsubno":Bsubno, "Bname":Bname, "authors":authors, "press":press, "price":price, "orderNumber":orderNumber, "total":total}
        books.append(book)
    return books

def getBookInfo(p_cursor, p_Bno, p_Bsubno):
    book = {}
    book["Bno"] = p_Bno
    book["Bsubno"] = p_Bsubno    
    sql = f"select Bname, press, price, quantity, cover, catalog, position from book where Bno = '{p_Bno}' and Bsubno = {p_Bsubno} and isValid = 1;"
    p_cursor.execute(sql)
    result = p_cursor.fetchone()
    if result == None:
        return {}
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

def processBookOrder(p_cursor, p_Ono, p_level, p_Uno):
    sql = f"select Bno, Bsubno, orderNumber from ob where Ono = {p_Ono};"
    p_cursor.execute(sql)
    result_out = p_cursor.fetchall()
    totalMoney = 0
    for row_out in result_out:
        Bno = row_out[0]
        Bsubno = row_out[1]
        orderNumber = row_out[2]
        sql = f"select price, quantity from book where Bno = '{Bno}' and Bsubno = {Bsubno};"
        p_cursor.execute(sql)
        result = p_cursor.fetchone()
        price = result[0]
        quantity = result[1]
        total = orderNumber * price 
        totalMoney = totalMoney + total
        if quantity < orderNumber:
            insufficientNumber = orderNumber - quantity 
            f_registerShortage(p_cursor, Bno, Bsubno, p_Uno, insufficientNumber)
    rate = [0.1, 0.15, 0.15, 0.2, 0.25]
    discountMoney = totalMoney * (1 - rate[p_level + 1])
    return totalMoney, discountMoney

def f_registerShortage(cursor, Bno, Bsubno, Uno, insufficientNumber):
    sql = f"select Sno from shortage where Bno = '{Bno}' and Bsubno = {Bsubno};"
    cursor.execute(sql)
    result = cursor.fetchone()
    if result == None:
        sql = f"insert into shortage(Bno, Bsubno, Uno, insufficientNumber, purchaseTime) values('{Bno}', {Bsubno}, '{Uno}', {insufficientNumber}, now());"
        cursor.execute(sql)
    else:
        Sno = result[0]
        sql = f"update shortage set insufficientNumber = insufficientNumber + {insufficientNumber}, Uno = '{Uno}' where Sno = {Sno};"
        cursor.execute(sql)

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
    sql = f"select Ono from `order` where Uno = '{Uno}' and state in('submitted', 'delivery', 'finished');"
    cursor.execute(sql)
    result = cursor.fetchall()
    if result == None:
        data = {"ret": 1, "msg": "用户没有历史订单！"}
    else:
        orders = []
        for row in result:
            sql = f"select totalMoney, deliveryAddress, discountMoney, state, orderTime from `order` where Ono = '{row[0]}';"
            cursor.execute(sql)
            result = cursor.fetchone()
            totalMoney = result[0]
            deliveryAddress = result[1]
            discountMoney = result[2]
            state = result[3]
            orderTime = result[4]
            books = getOrderBook(cursor, row[0])
            order = {"Ono":row[0], "books":books, "totalMoney":totalMoney, "discountMoney":discountMoney, "deliveryAddress":deliveryAddress, "state":state, "orderTime":orderTime}
            orders.append(order)
        data = {"ret": 0, "orders":orders}
    closeSQL(conn, cursor)
    return jsonify(data)

@app.route('/api/searchBooks', methods=["GET", "POST"])
def searchBooks():
    books = []
    conn, cursor = connectSQL()
    type = request.form.get("type")
    if type == 'null':
        return jsonify({"ret":1, "msg":"未选择类型！"})
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
    if result == {}:
        return jsonify({"ret":1, "msg":"无目标图书！"})
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
    books = json.loads(books)
    sql = f"select Ono from `order` where Uno = '{Uno}' and state = 'shopping';"
    cursor.execute(sql)
    result = cursor.fetchone()
    if result == None:
        sql = f"insert into `order`(Uno, state) values('{Uno}', 'new');"
        cursor.execute(sql)
        sql = f"select Ono from `order` where state = 'new';"
        cursor.execute(sql)
        Ono = cursor.fetchone()[0]
        for book in books:
            Bno = book[0]
            Bsubno = book[1]
            orderNumber = book[2]
            sql = f"insert into `ob` values('{Bno}', {Bsubno}, {Ono}, {orderNumber});"
            cursor.execute(sql)
        sql = f"update `order` set state = 'shopping' where Ono = {Ono}"
        cursor.execute(sql)
    else:
        Ono = result[0]
        for book in books:
            Bno = book[0]
            Bsubno = book[1]
            orderNumber = book[2]
            sql = f"delete from ob where Ono = {Ono};"
            cursor.execute(sql)
            sql = f"insert into ob(Bno, Bsubno, Ono, orderNumber) values('{Bno}', {Bsubno}, {Ono}, {orderNumber});"
            cursor.execute(sql)
    data = {"ret":0}
    closeSQL(conn, cursor)
    return jsonify(data)

@app.route('/api/getShoppingCart', methods=["GET", "POST"])
def getShoppingCart():
    conn, cursor = connectSQL()
    Uno = request.form.get("Uno")
    sql = f"select Ono from `order` where Uno = '{Uno}' and state = 'shopping';"
    cursor.execute(sql)
    result = cursor.fetchone()
    if result == None:
        data = {"ret":1, "msg":"用户购物车为空！"}
    else:
        Ono = result[0]
        books = getOrderBook(cursor, Ono)
        data = {"ret":0, "books":books}
    closeSQL(conn, cursor)
    return jsonify(data)

@app.route('/api/submitOrder', methods=["GET", "POST"])
def submitOrder():
    conn, cursor = connectSQL()
    Uno = request.form.get("Uno")
    sql = f"select Ono from `order` where Uno = '{Uno}' and state  ='shopping';"
    cursor.execute(sql)
    result = cursor.fetchone()
    if result == None:
        return jsonify({"ret":1, "msg":"历史购物车不存在！"})
    Ono = result[0]
    sql = f"select address, level from `user` where Uno = '{Uno}';"
    cursor.execute(sql)
    result = cursor.fetchone()
    deliveryAddress = result[0]
    level = result[1]
    totalMoney, discountMoney = processBookOrder(cursor, Ono, level, Uno)
    sql = f'''update `user` set balance = balance - {discountMoney}, 
        total = total + {discountMoney}
        where Uno = '{Uno}';'''
    cursor.execute(sql)
    sql = f'''update `order` set state = 'submitted', totalMoney = {totalMoney}, discountMoney = {discountMoney},
            deliveryAddress = '{deliveryAddress}', orderTime = NOW()
        where Ono = {Ono};'''
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
    sql = f"select Ono, Uno, totalMoney, discountMoney, deliveryAddress, state, orderTime from `order` where state in('submitted', 'delivery');"
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        books = getOrderBook(cursor, row[0])
        order = {"Ono":row[0],
                "Uno":row[1],
                "books":books,
                "totalMoney":row[2], 
                "discountMoney":row[3],
                "deliveryAddress":row[4], 
                "state":row[5], 
                "orderTime":row[6]}
        orders.append(order)
    data = {"ret":0, "orders":orders}
    closeSQL(conn, cursor)
    return jsonify(data)

@app.route('/api/getBooks', methods=["GET", "POST"])
def getBooks():
    books = []
    conn, cursor = connectSQL()
    sql = f"select Bno, Bsubno from book where isValid = 1;"
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
        if row[0] == 0:
            continue
        sql = f"select Sno from shortage where Pno = {row[0]};"
        cursor.execute(sql)
        SnoSet = cursor.fetchall()
        SnoSet = [item[0] for item in SnoSet]
        purchase.append({"Pno":row[0], "SnoSet":SnoSet})
    data = {"ret":0, "purchase":purchase}
    closeSQL(conn, cursor)
    return jsonify(data)

@app.route('/api/updateUserInfo', methods=["GET", "POST"])
def updateUserInfo():
    conn, cursor = connectSQL()
    Uno = request.form.get("Uno")
    level = request.form.get("level")
    sql = f"select Uno from user where Uno = '{Uno}';"
    cursor.execute(sql)
    result = cursor.fetchone()
    if result == None:
        data = {"ret": 1, "msg": "用户不存在！"}
    else:
        sql = f"update user set level = {level} where Uno = '{Uno}';"
        cursor.execute(sql)
        data = {"ret": 0}
    closeSQL(conn, cursor)
    return jsonify(data)

@app.route('/api/deliver', methods=["GET", "POST"])
def deliver():
    conn, cursor = connectSQL()
    Ono = request.form.get("Ono")
    sql = f"select Ono from `order` where Ono = {Ono};"
    cursor.execute(sql)
    result = cursor.fetchone()
    if result == None:
        data = {"ret": 1, "msg": "订单不存在！"}
    else:
        sql = f"select Bno, Bsubno, orderNumber from ob where Ono = {Ono};"
        cursor.execute(sql)
        result_out = cursor.fetchall()
        for row_out in result_out:
            Bno = row_out[0]
            Bsubno = row_out[1]
            orderNumber = row_out[2]
            sql = f"select quantity from book where Bno = '{Bno}' and Bsubno = {Bsubno};"
            cursor.execute(sql)
            quantity = cursor.fetchone()[0]
            if quantity < orderNumber:
                return jsonify({"ret": 1, "msg": f"书号{Bno}_{Bsubno}存货不足！"})
            sql = f"update `book` set quantity = quantity - {orderNumber} where Bno = '{Bno}' and Bsubno = {Bsubno};"
            cursor.execute(sql)
        sql = f"update `order` set state = 'delivery' where Ono = {Ono};"
        cursor.execute(sql)
        data = {"ret": 0}
    closeSQL(conn, cursor)
    return jsonify(data)

@app.route('/api/finish', methods=["GET", "POST"])
def finish():
    conn, cursor = connectSQL()
    Ono = request.form.get("Ono")
    sql = f"select Ono from `order` where Ono = {Ono};"
    cursor.execute(sql)
    result = cursor.fetchone()
    if result == None:
        data = {"ret": 1, "msg": "订单不存在！"}
    else:
        sql = f"update `order` set state = 'finished' where Ono = {Ono};"
        cursor.execute(sql)
        data = {"ret": 0}
    closeSQL(conn, cursor)
    return jsonify(data)

@app.route('/api/purchase', methods=["GET", "POST"])
def purchase():
    conn, cursor = connectSQL()
    shortageSet = request.form.get("shortageSet")
    shortageSet = json.loads(shortageSet)
    sql = f"select max(Pno) from shortage;"
    cursor.execute(sql)
    Pno = cursor.fetchone()
    if Pno[0] == None:
        Pno = 1
    else:
        Pno = Pno[0] + 1
    for Sno in shortageSet:
        sql = f"update shortage set Pno = {Pno} where Sno = {Sno};"
        cursor.execute(sql)
    data = {"ret":0}
    closeSQL(conn, cursor)
    return jsonify(data)

@app.route('/api/finishPurchase', methods=["GET", "POST"])
def finishPurchase():
    conn, cursor = connectSQL()
    Pno = request.form.get("Pno")
    sql = f"select Bno, Bsubno, insufficientNumber from shortage where Pno = {Pno};"
    cursor.execute(sql)
    result = cursor.fetchall()
    if result == None:
        data = {"ret":1, "msg":"该采购单不存在！"}
    else:
        for row in result:
            sql = f"updata book set quantity = quantity + {row[2]} where Bno = '{row[0]}' and Bsubno = {row[1]}"
        sql = f"update shortage set Pno = 0 where Pno = {Pno};"
        cursor.execute(sql)
    data = {"ret":0}
    closeSQL(conn, cursor)
    return jsonify(data)

@app.route('/api/registerShortage', methods=["GET", "POST"])
def registerShortage():
    conn, cursor = connectSQL()
    Bno = request.form.get("Bno")
    Bsubno = request.form.get("Bsubno")
    Uno = request.form.get("Uno")
    insufficientNumber = request.form.get("insufficientNumber")
    f_registerShortage(cursor, Bno, Bsubno, Uno, insufficientNumber)
    data = {"ret":0}
    closeSQL(conn, cursor)
    return jsonify(data)

@app.route('/api/updatePrice', methods=["GET", "POST"])
def updatePrice():
    conn, cursor = connectSQL()
    Bno = request.form.get("Bno")
    Bsubno = request.form.get("Bsubno")
    price = request.form.get("price")
    sql = f"update book set price = {price} where Bno = '{Bno}' and Bsubno = {Bsubno};"
    cursor.execute(sql)
    data = {"ret":0}
    closeSQL(conn, cursor)
    return jsonify(data)

@app.route('/api/addBooks', methods=["GET", "POST"])
def addBooks():
    conn, cursor = connectSQL()
    Bno = request.form.get("Bno")
    Bsubno = request.form.get("Bsubno")
    Bname = request.form.get("Bname")
    authors = request.form.getlist("authors")
    keys = request.form.getlist("keys")
    press = request.form.get("press")
    price = request.form.get("price")
    quantity = request.form.get("quantity")
    catalog = request.form.get("catalog")
    position = request.form.get("position")
    cover_data = request.files["cover"]
    sql = f"select Bno from book where Bno = '{Bno}' and Bsubno = {Bsubno};"
    cursor.execute(sql)
    result = cursor.fetchone()
    if result != None:
        return jsonify({"ret":1, "msg":"与已有图书重复！"})
    coverName = cover_data.filename
    cover = Image.open(cover_data.stream)
    coverPath = f"../source/cover/{coverName}"
    cover.save(coverPath)
    sql = f"insert into book values('{Bno}', {Bsubno}, '{Bname}', '{press}', {price}, {quantity}, '{coverName}', '{catalog}', {position});"
    cursor.execute(sql)
    for keyword in keys:
        sql = f"select Kno from `keywords` where keyword = '{keyword}';"
        cursor.execute(sql)
        result = cursor.fetchone()
        if result == None:
            sql = f"insert into `keywords`(keyword) values('{keyword}');"
            cursor.execute(sql)
            sql = f"select Kno from `keywords` where keyword = '{keyword}';"
            cursor.execute(sql)
            result = cursor.fetchone()
        Kno = result[0]
        sql = f"insert into tags values('{Bno}', {Bsubno}, {Kno});"
        cursor.execute(sql)
    for index, author in enumerate(authors):
        sql = f"select Ano from author where Aname = '{author}';"
        cursor.execute(sql)
        result = cursor.fetchone()
        if result == None:
            sql = f"insert into author(Aname) values('{author}');"
            cursor.execute(sql)
            sql = f"select Ano from author where Aname = '{author}';"
            cursor.execute(sql)
            result = cursor.fetchone()
        Ano = result[0]
        sql = f"insert into `write` values('{Bno}', {Bsubno}, {Ano}, {index + 1});"
        cursor.execute(sql)
    data = {"ret":0}
    closeSQL(conn, cursor)
    return jsonify(data)

@app.route('/api/deleteMsg', methods=["GET", "POST"])
def deleteMsg():
    conn, cursor = connectSQL()
    Uno = request.form.get("Uno")
    sql = f"update user set message = NULL where Uno = '{Uno}';"
    cursor.execute(sql)
    data = {"ret":0}
    closeSQL(conn, cursor)
    return jsonify(data)

@app.route('/api/deleteBook', methods=["GET", "POST"])
def deleteBook():
    conn, cursor = connectSQL()
    Bno = request.form.get("Bno")
    Bsubno = request.form.get("Bsubno")
    sql = f"update book set isValid = 0 where Bno = '{Bno}' and Bsubno = {Bsubno};"
    cursor.execute(sql)
    data = {"ret":0}
    closeSQL(conn, cursor)
    return jsonify(data)

@app.route('/api/getVendors', methods=["GET", "POST"])
def getVendors():
    conn, cursor = connectSQL()
    vendors = []
    sql = f"select Vno, Vname, Vaddress from vendor;"
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        books = []
        sql = f"select Bno, Bsubno, Vstate from supply where Vno = {row[0]};"
        cursor.execute(sql)
        res = cursor.fetchall()
        for item in res:
            sql = f"select Bname from book where Bno = '{item[0]}' and Bsubno = {item[1]};"
            cursor.execute(sql)
            Bname = cursor.fetchall()[0]
            book = {"Bno":item[0], "Bsubno":item[1], "Bname":Bname, "state":item[2]}
            books.append(book)
        vendor = {"Vno":row[0], "Vname":row[1], "Vaddress":row[2], "books":books}
        vendors.append(vendor)
    data = {"ret":0, "vendors":vendors}
    closeSQL(conn, cursor)
    return jsonify(data)

@app.route('/api/addVendor', methods=["GET", "POST"])
def addVendor():
    conn, cursor = connectSQL()
    Vname = request.form.get("Vname")
    Vaddress = request.form.get("Vaddress")
    books = request.form.get("books")
    books = json.loads(books)
    sql = f"insert into vendor(Vname, Vaddress) values('{Vname}', '{Vaddress}');"
    cursor.execute(sql)
    sql = f"select Vno from vendor where Vname = '{Vname}' and Vaddress =  '{Vaddress}';"
    cursor.execute(sql)
    Vno = cursor.fetchone()[0]
    for book in books:
        sql = f'''insert into supply values('{book["Bno"]}', {book["Bsubno"]}, {Vno}, '{book["state"]}');'''
        cursor.execute(sql)
    data = {"ret":0}
    closeSQL(conn, cursor)
    return jsonify(data)

@app.route('/cover/<filename>')
def uploaded_file(filename):
    return send_from_directory(directory="../source/cover", path=filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)