import os
import uuid
from main import app,db,secure_filename
from flask import redirect,render_template, render_template_string,request,url_for,session,flash
from main.models import  User,Product,Typec,Category,Carto
from flask_login import login_required,login_user,logout_user,current_user
from datetime import datetime
from dateutil.relativedelta import relativedelta


@app.route('/seller/login', methods=['GET','POST'])
def sellerLogin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        seller = User.query.filter_by(email=email).first()
        if seller and seller.check_password_correction(attempted_password = password):
            if seller.role == 3:
                login_user(seller)
                return redirect(url_for('seller'))
            else:
                flash ('Your Email Or Passwod Not Work')
                return redirect(url_for('sellerLogin'))
        else:
            flash ('Email Or Password Not correct ')
    return render_template('seller/login.html')

@app.route('/sellerRegistration', methods=['GET', 'POST'])
def sellerRegistration():
    if request.method == 'POST':
        name = request.form.get('name')
        last_name = request.form.get('lastname')
        company = request.form.get('company')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        re_password = request.form.get('re-password')
        seller = User.query.filter_by(email=email, role=3).first()
        if not seller:
            if password and password == re_password:
                content_to_create = User (name=name, lastname=last_name, email=email, number=phone, company=company, role=3, password=password)
                db.session.add(content_to_create)
                db.session.commit()
                return redirect(url_for('sellerLogin'))
            else:
                flash ('Passwords Not Same')
                return redirect(url_for('sellerRegistration'))
        else:
            flash ('Mail Already')
            return redirect(url_for('sellerRegistration'))
    return render_template('seller/registration.html')

@app.route('/seller')
def seller():
    return render_template('seller/index.html')

@app.route('/seller/Products')
def sellerProducts():
    products = Product.query.filter_by(stuff_user=current_user.get_id())
    return render_template('seller/Products/products.html',products=products)

@app.route('/seller/addProduct', methods=['GET','POST'])
def sellerAddProducts():
    categorys = Category.query.all()
    if request.method == 'POST':
        file = request.files['photo']
        fname = file.filename
        if fname:
            file.save(os.path.join('main/static/img/products',secure_filename(fname)))
        name = request.form.get('name')
        title = request.form.get('title')
        about = request.form.get('about')
        code = request.form.get('productCode')
        stock = request.form.get('stock')
        size = request.form.get('size')
        category = request.form.get('category')
        re_cat = request.form.get('newCategory')
        user = current_user.get_id()
        if category:
            content_to_create = Product(name=name,title=title,about=about,product_code=code,stock=stock,size=size,category=category,stuff_user=user,photo_1=fname)
        else:
            content_to_create = Product(name=name,title=title,about=about,product_code=code,stock=stock,size=size,req_cat=re_cat,stuff_user=user,photo_1=fname)
        db.session.add(content_to_create)
        db.session.commit()
    return render_template('seller/Products/addProduct.html', categorys=categorys)

@app.route('/seller/updateProduct')
def sellerUpdateProducts():
    return render_template('seller/Products/updateProduct.html')

