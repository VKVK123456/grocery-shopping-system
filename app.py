from flask import Flask, redirect, render_template, flash, url_for
from flask import request, session
from flask_session import Session
import mysql.connector as mysql
from sql_connection import get_sql_connection
from datetime import date
import functools
from itertools import chain

app = Flask(__name__)
app.secret_key = "super secret key" 

def setCustid_glb(id):
    global custid_glob
    custid_glob =id

connection = get_sql_connection()
 
@app.route('/',methods=['GET'])
def MyhomeRoot():
    print("runs from app.py")
    return render_template('login.html')

@app.route("/My_Login_Process", methods=['POST'])
def My_Login_Process():
    uid = request.form["username"]
    pwd = request.form["password"] 
    try: 
        db_connect = mysql.connect(
            host="localhost", database="grocery", user="root", passwd="Vinay@111", use_pure=True)
        sql = "Select username,password,custid From login where username = " + "'" + uid + "'"
        mycursor = db_connect.cursor()
        mycursor.execute(sql)
        cno = mycursor.fetchall()
        res = [tuple(str(item) for item in t) for t in cno]
        #print(res)
    except Exception as err:
        print(err)
        return render_template('MyError.html')
    if len(res) == 0:
        status = 0
        return render_template('MyError.html')
    else:
        usrid  = res[0][0]
        passwd = res[0][1]
        custid = res[0][2]
        id=custid
        setCustid_glb(id)
        if (usrid == uid and pwd == passwd and uid=='Admin'):
            return render_template('home.html', usrid=usrid)
        elif (usrid == uid and pwd == passwd):
            print("loggedin as user")
            return render_template('home2.html', usrid=usrid,custid=custid_glob)
        else:
            return render_template('MyError.html')

@app.route('/getallproducts')
def getallproducts():
    try:
        db_connect = mysql.connect(
            host="localhost", database="grocery", user="root", passwd="Vinay@111", use_pure=True)
        sql = "SELECT products.product_id,products.product_name,products.uom_id,products.price_per_unit,uom.uom_name FROM grocery.products inner join uom on products.uom_id=uom.uom_id"
        mycursor = db_connect.cursor()
        mycursor.execute(sql)
        cdata = mycursor.fetchall()
        return render_template('viewproduct.html', cdata=cdata)
    except Exception as err:
        print(err)
        return render_template('MyError.html')


@app.route("/AddProduct", methods=['POST'])
def AddProduct():
    product_name = request.form["product_name"]
    uom_id = request.form["uom_id"] 
    price_per_unit = request.form["price_per_unit"]
    try:
        db_connect = mysql.connect(
            host="localhost", database="grocery", user="root", passwd="Vinay@111", use_pure=True)
        sql = "INSERT INTO grocery.products(product_name,uom_id,price_per_unit) VALUES ("  + "'" + product_name + "'" + "," + uom_id  + ","+ price_per_unit + ")" 
        mycursor = db_connect.cursor()
        mycursor.execute(sql)
        db_connect.commit()
        return render_template('addproduct.html')
    except Exception as err:
        print(err)
        return render_template('MyError.html')

@app.route('/getallorders')
def getallorders():
    try:
        db_connect = mysql.connect(
            host="localhost", database="grocery", user="root", passwd="Vinay@111", use_pure=True)
        sql = "SELECT * FROM orders"
        mycursor = db_connect.cursor()
        mycursor.execute(sql)
        cdata = mycursor.fetchall()
        return render_template('vieworders.html', cdata=cdata)
    except Exception as err:
        print(err)
        return render_template('MyError.html')


@app.route('/getallorderdetails')
def getallorderdetails():
    try:
        db_connect = mysql.connect(
            host="localhost", database="grocery", user="root", passwd="Vinay@111", use_pure=True)
        sql = "SELECT * FROM order_details"
        mycursor = db_connect.cursor()
        mycursor.execute(sql)
        cdata = mycursor.fetchall()
        return render_template('vieworderdetails.html', cdata=cdata)
    except Exception as err:
        print(err)
        return render_template('MyError.html')


@app.route("/Delproducts", methods=['POST'])
def Delproducts():
    product_id = request.form["product_id"]
    try:
        print(product_id)
        db_connect = mysql.connect(
            host="localhost", database="grocery", user="root", passwd="Vinay@111", use_pure=True)
        sql_std = "DELETE FROM products WHERE product_id = " + "'" + product_id + "'"
        mycursor = db_connect.cursor()
        mycursor.execute(sql_std)
        db_connect.commit()
        return render_template('Deleteproduct.html')
    except Exception as err:
        print(err)
        return render_template('MyError.html')
        



@app.route('/AddTocart',methods=['POST'])
def AddTocart():
    try:
        addvalue=request.form["quantity"]
        Pid_1name=request.form["pid"]
        print(addvalue)
        print(Pid_1name)
        cdate= date.today()
        db_connect = mysql.connect(
            host="localhost", database="grocery", user="root", passwd="Vinay@111",use_pure=True)
        mycursor=db_connect.cursor()     
        #=====================fetch product type ======================== 
        fetchTypeSql="select category from products where product_id ="+"'"+Pid_1name+"'"
        print(fetchTypeSql)
        mycursor.execute(fetchTypeSql)
        Prodtype=mycursor.fetchone()
        Prodtype=Prodtype[0]
        print(Prodtype)
        #====================fetch product name ========================
        fetchpnameSql="select product_name from products where product_id ="+"'"+Pid_1name+"'"
        print(fetchpnameSql)
        mycursor.execute(fetchpnameSql)
        Prodname=mycursor.fetchone()
        print(Prodname)
        Prodname=Prodname[0]
        print(Prodname)
        #==================fetch user cart id ===========================
        sql="select cart_id from cart where cust_id = " +"'"+custid_glob+"'"
        print(sql)
        mycursor.execute(sql)
        cartid=mycursor.fetchone()
        cartid=int(cartid[0])
        print(cartid)
        #===================fetch price================= 

        sqlPprice="select price_per_unit from products where product_id= "+"'"+Pid_1name+"'"
        print(sqlPprice)
        mycursor.execute(sqlPprice)
        ProdPrice=mycursor.fetchone()
        ProdPrice=ProdPrice[0]
        print(ProdPrice)
        #==================Quantity * price================
        cost = int(addvalue)*ProdPrice
        print(cost)
        #==================update product table=============
        sqlRetQuaty="select quantity from products where product_id= "+"'"+Pid_1name+"'"
        print(sqlRetQuaty)
        mycursor.execute(sqlRetQuaty)
        productQuantity=mycursor.fetchone()
        print(productQuantity)
        productQuantity=productQuantity[0]
        newQuantity=int(productQuantity)-int(addvalue)
        print(newQuantity)
        sqlSetnewqua="update products set quantity ="+"'"+str(newQuantity)+"' where product_id="+"'"+Pid_1name+"'"
        print(sqlSetnewqua)
        mycursor.execute(sqlSetnewqua)
        db_connect.commit()
        #================== insert into cart_items===============
        sqlinsert="insert into cart_items (cartid,pid,pname,quantity,cost,date)values("+"'"+str(cartid)+"',"+"'"+Pid_1name+"',"+"'"+str(Prodname)+"',"+"'"+addvalue+"',"+"'"+str(cost)+"',"+"'"+str(cdate)+"')"
        print(sqlinsert)
        mycursor.execute(sqlinsert)
        db_connect.commit()

        #================== return the page =========================
        if Prodtype=="fruit":
            return render_template('fruits.html',Pid_name=Pid_name,custid=custid_glob) 
        if Prodtype=="vegetable":
            return render_template('vegetable.html',Pid_name=Pid_name,custid=custid_glob) 
        if Prodtype=="grocery":
            return render_template('grocery.html',Pid_name=Pid_name,custid=custid_glob)      
    except Exception as err:
        print(err)
        return render_template('MyError.html')  

@app.route("/vegetables")    
def vegetables():
    try:
        db_connect = mysql.connect( host="localhost", database="grocery", user="root", passwd="Vinay@111", use_pure=True)
        sql="select product_id,product_name,price_per_unit from products where category = 'vegetable'"
        mycursor=db_connect.cursor()
        mycursor.execute(sql)
        global Pid_name
        Pid_name=mycursor.fetchall()
        print(Pid_name)
        print('vegetable section')
        return render_template("vegetable.html",Pid_name=Pid_name,custid=custid_glob)
    except Exception as err:
        print(err)
        return render_template("MyError.html")

@app.route("/fruits")    
def fruits():
    try:
        db_connect = mysql.connect( host="localhost", database="grocery", user="root", passwd="Vinay@111", use_pure=True)
        sql="select product_id,product_name,price_per_unit from products where category = 'fruit'"
        mycursor=db_connect.cursor()
        mycursor.execute(sql)
        global Pid_name
        Pid_name=mycursor.fetchall()
        print('fruit section')
        return render_template("fruits.html",Pid_name=Pid_name,custid=custid_glob)
    except Exception as err:
        print(err)
        return render_template("MyError.html")

@app.route("/grains")    
def grains():
    try:
        db_connect = mysql.connect( host="localhost", database="grocery", user="root", passwd="Vinay@111", use_pure=True)
        sql="select product_id,product_name,price_per_unit from products where category = 'grocery'"
        mycursor=db_connect.cursor()
        mycursor.execute(sql)
        global Pid_name
        Pid_name=mycursor.fetchall()
        print(Pid_name)
        print('grocery section')
        return render_template("grocery.html",Pid_name=Pid_name,custid=custid_glob)
    except Exception as err:
        print(err)
        return render_template("MyError.html")

@app.route("/cartItems")
def cartItems():
    try:
        db_connect = mysql.connect( host="localhost", database="grocery", user="root", passwd="Vinay@111", use_pure=True)
        mycursor=db_connect.cursor()
        #======================CART Id=============================
        fetchcartid="select cart_id from cart where cust_id = "+"'"+str(custid_glob)+"'"
        mycursor.execute(fetchcartid)
        cartid=mycursor.fetchone()
        cartid=cartid[0]
        query1="select cost from cart_items where cartid = "+"'"+str(cartid)+"'"
        mycursor.execute(query1) 
        total=mycursor.fetchall()
        print(total)
        cost=list(chain(*total))
        print(cost)
        grandtotal=0
        for ele in range(0,len(cost)):
            print(ele)
            print(cost[ele])
            grandtotal = grandtotal + cost[ele]
        #===================cart items==============================
        fetchCartsql="select pid,pname,quantity,cost,cart_item_id from cart_items where cartid = "+"'"+str(cartid)+"'"
        mycursor.execute(fetchCartsql)
        cartitems=mycursor.fetchall()
        return render_template("cart.html",cartitems=cartitems,grandtotal=grandtotal)
    except Exception as err:
        print(err)
        return render_template("Error.html")

@app.route('/salesReport',methods=['POST'])
def salesReport():
    try:
        cartid=request.form["cartid"]
        db_connect = mysql.connect(
            host="localhost", database="grocery", user="root", passwd="Vinay@111",use_pure=True)
        mycursor=db_connect.cursor()   
        sql="select pid,pname,quantity,cost,date from cart_items where cartid = "+"'"+str(cartid)+"'"
        mycursor.execute(sql)
        cartitems=mycursor.fetchall()
        return render_template("report.html",cartitems=cartitems)
    except Exception as err:
        print(err)
        return render_template("MyError.html")

@app.route("/deletecart",methods=['POST'])
def deletecart():
    try:
        cartitemid=request.form["cart_item_id"]
        print(cartitemid)
        db_connect = mysql.connect( host="localhost", database="grocery", user="root", passwd="Vinay@111", use_pure=True)
        mycursor=db_connect.cursor()
        #======================CART Id=============================
        fetchcartid="select cart_id from cart where cust_id = "+"'"+str(custid_glob)+"'"
        mycursor.execute(fetchcartid)
        cartid=mycursor.fetchone()
        cartid=cartid[0]
        print(cartid)
        fetchprodquanid="select pid,quantity from cart_items where cart_item_id = "+"'"+str(cartitemid)+"'"
        print(fetchprodquanid)
        mycursor.execute(fetchprodquanid)
        prodquan=mycursor.fetchone()
        prodid=prodquan[0]
        quantity=prodquan[1]
        print(prodid)
        print(quantity)
        sqlRetQuaty="select quantity from products where product_id= "+"'" +str(prodid)+"'"
        print(sqlRetQuaty)
        mycursor.execute(sqlRetQuaty)
        productQuantity=mycursor.fetchone()
        productQuantity=productQuantity[0]
        print(productQuantity)

        newQuantity=productQuantity+int(quantity)
        print(newQuantity)
        sqlSetnewqua="update products set quantity ="+"'"+str(newQuantity)+"' where product_id="+"'"+str(prodid)+"'"
        print(sqlSetnewqua)
        mycursor.execute(sqlSetnewqua)
        
        sql1="DELETE FROM cart_items WHERE cart_item_id ="+"'" + str(cartitemid) + "'"
        print(sql1)
        sql2="select pid,pname,quantity,cost,cart_item_id from cart_items where cartid = "+"'"+str(cartid)+"'"
        print(sql2)
        mycursor.execute(sqlSetnewqua)
        mycursor.execute(sql1)
         
        query1="select cost from cart_items where cartid = "+"'"+str(cartid)+"'"
        mycursor.execute(query1) 
        total=mycursor.fetchall()
        cost=list(chain(*total))
        grandtotal=0
        for ele in range(0,len(cost)):
            print(ele)
            print(cost[ele])
            grandtotal = grandtotal + cost[ele] 
        mycursor.execute(sql2)
        cartitems=mycursor.fetchall()
        print(cartitems)
        db_connect.commit()
        return render_template('cart.html',cartitems=cartitems,grandtotal=grandtotal)      
    except Exception as err:
        print(err)
        return render_template('MyError.html')

@app.route('/insertorder',methods=['POST'])
def insertorder():
    cdate= date.today()
    try:
        db_connect = mysql.connect(
            host="localhost", database="grocery", user="root", passwd="Vinay@111",use_pure=True)
        mycursor=db_connect.cursor()
        sql1="select cart_id from cart where cust_id = "+"'"+str(custid_glob)+"'"
        mycursor.execute(sql1)
        cartid=mycursor.fetchone()
        cartid=cartid[0]
        print(cartid)

        query1="select cost from cart_items where cartid = "+"'"+str(cartid)+"'"
        mycursor.execute(query1) 
        total=mycursor.fetchall()
        cost=list(chain(*total))
        grandtotal=0
        for ele in range(0,len(cost)):
            grandtotal = grandtotal + cost[ele]
        print(grandtotal)

        sql2="select cname from customer where cart_id="+"'"+str(cartid)+"'"
        mycursor.execute(sql2)
        customername=mycursor.fetchall()
        custname=list(chain(*customername))
        cname=''.join([str(elem) for elem in custname])
        print(cname)
        sql4="insert into orders (order_id,customer_name,total,date_time) VALUES ("  +  str(cartid)  + "," +"'"+ str(cname)+"'"+ ","+ str(grandtotal) +","+"'"+str(cdate)+"'"+ ")"
        print(sql4)
        mycursor.execute(sql4)
        cdata=mycursor.fetchall()
        print(cdata)
        sql3="DELETE FROM cart_items WHERE cartid="+"'" + str(cartid)+ "'"
        mycursor.execute(sql3)
        deleted=mycursor.fetchall()
        print(deleted)
       
        
        fetchCartsql="select pid,pname,quantity,cost from cart_items where cartid = "+"'"+str(cartid)+"'"
        mycursor.execute(fetchCartsql)
        cartitems=mycursor.fetchall()
        db_connect.commit()
        return render_template("cart.html",cartitems=cartitems,grandtotal=grandtotal)     
    except Exception as err:
        print(err)
        return render_template('MyError.html')

@app.route('/getname')
def getname():
    try:
        db_connect = mysql.connect(
            host="localhost", database="grocery", user="root", passwd="Vinay@111",use_pure=True)
        mycursor=db_connect.cursor()
        sql="select cname from customer where cust_id="+"'"+str(custid_glob)+"'"
        mycursor.execute(sql)
        custname=mycursor.fetchone()
        custname=custname[0]
        return render_template('home2.html',custname=custname)
    except Exception as err:
        print(err)
        return render_template('MyError.html')















@app.route('/category')
def category():
    return render_template('category.html')



@app.route('/addproduct')
def addproduct():
    return render_template('addproduct.html')

@app.route('/deleteproduct')
def deleteproduct():
    return render_template('Deleteproduct.html')

@app.route('/viewproduct')
def viewproduct():
    return render_template('viewproduct.html')


@app.route('/vieworders')
def vieworders():
    return render_template('vieworders.html')


@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/home2')
def home2():
    return render_template('home2.html')

@app.route('/')
def MyError():
    return render_template('MyError.html')

@app.route('/cartItems1')
def cartItems1():
    return render_template("cart.html")

@app.route("/rendersales")
def rendersales():
    return render_template("report.html")

if __name__ == '__main__':
   connection = get_sql_connection()
   app.run(debug=True)
  
