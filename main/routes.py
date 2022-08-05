import os
import uuid
from main import app,db,secure_filename
from flask import redirect,render_template,request,url_for,session,flash
from main.models import  User,Product,Typec,Category,Carto
from flask_login import login_required,login_user,logout_user,current_user
from datetime import datetime
from dateutil.relativedelta import relativedelta


@app.route('/')
def index():
    
    if current_user.is_authenticated:
        carts = Carto.query.filter_by(userId=current_user.get_id())
    else:
        sesID()
        carts = Carto.query.filter_by(sessionId = session['id'])
    categorys = Category.query.all()
    products = Product.query.all()
    sesCheck()
    return render_template('index.html', categorys=categorys, products=products, carts=carts)


@app.route('/shop')
def product():
    categorys = Category.query.all()
    types = Typec.query.all()
    return render_template('productList.html', categorys=categorys, types=types)


@app.route('/shop/<int:id>')
def shops(id):
    categorys = Category.query.all()
    types = Typec.query.all()
    products = Product.query.filter_by(category=id)
    return render_template('productList.html', categorys=categorys, types=types, products=products)


@app.route('/cart')
def Cart():
    subPrice = 0
    b = 0
    if current_user.is_authenticated:
        carts = Carto.query.filter_by(userId=current_user.get_id())
        for a in carts:
            b = b + (a.price * a.pieces)
        subPrice = b
    else:
        sesID()
        carts = Carto.query.filter_by(sessionId=sesID())
        for a in carts:
            b = b + (a.price * a.pieces)
        subPrice = b
        sesCheck()
    return render_template('cart.html', carts=carts, subPrice=subPrice)

@app.route('/cartIncrease/<int:id>')
def cartIncrease(id):
    if current_user.is_authenticated:
        try:
            cart = Carto.query.filter_by(id=id, userId=current_user.get_id()).first()
            cart.pieces += 1
            db.session.commit()
            return redirect(request.referrer)
        except:
            return ('nonwowrk')


@app.route('/addCart/<int:id>', methods=['GET','POST'])
def addCart(id):
    if current_user.is_authenticated:
        try:
            cart = Carto.query.filter_by(productId=id, userId=current_user.get_id()).first()
            cart.pieces += 1
            db.session.commit()
        except:
            product = Product.query.get(id)
            content_to_create = Carto(productId=product.id, price=product.price, seller=product.stuff_user, userId=current_user.id)
            db.session.add(content_to_create)
            db.session.commit()
    else:
        try:
            cart = Carto.query.filter_by(productId=id, sessionId=session['id']).first()
            cart.pieces += 1
            db.session.commit()
        except:
            sessionID = sesID()
            product = Product.query.get(id)
            content_to_create = Carto(productId=product.id, price=product.price, seller=product.stuff_user, sessionId=sessionID)
            db.session.add(content_to_create)
            db.session.commit()
    return redirect(request.referrer)


@app.route('/delCart/<int:id>')
def delCart(id):
    cartProduct = Carto.query.get(id)
    db.session.delete(cartProduct)
    db.session.commit()
    return redirect(url_for('Cart'))
    

@app.route('/product/<int:id>')
def productDetail(id):
    product = Product.query.get(id)
    return render_template('productDetail.html', product=product)


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        attempted_user = User.query.filter_by(email=email).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password = password):
            if attempted_user.role == 1:
                login_user(attempted_user)
                return redirect(url_for('admin'))
            else: 
                flash ("Email Or Password Not Correct")
                return redirect(url_for('login'))   
        else:
            flash ("Email Or Password Not Correct")
            return redirect(url_for('login'))               
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


#-------------------------------Admin----------------------------------------#


@app.route('/admin') #-- Admin home page
def admin():
    if current_user.is_authenticated:
        return render_template('admin/index.html')
    else:
        return redirect(url_for('login'))


@app.route('/registration', methods=['GET','POST']) #-- Admin registration
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        password = request.form.get('password')
        re_password = request.form.get('re-password')
        if password == re_password:
            content_to_create = User(name=name, lastname=lastname, email=email, password=password, role=1)
            db.session.add(content_to_create)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            flash ('Passwords not same')
            return redirect(url_for('login'))
    return render_template('admin/registration.html')


@app.route('/products') # -- Admin Products Page
def products():       
    products = Product.query.all()
    return render_template('admin/Products/product.html', products=products)


@app.route('/productadd', methods=['GET','POST'])
def productAdd():
    categorys=Category.query.all()
    if request.method == 'POST':
        file = request.files['photo']
        fname = file.filename
        if fname:
            file.save(os.path.join('main/static/img/products', secure_filename(fname)))
            photo = fname
        name = request.form.get('name')
        title = request.form.get('title')
        about = request.form.get('about')
        productCode = request.form.get('productCode')
        stock = request.form.get('stock')
        category = request.form.get('category')
        price = request.form.get('price')
        size = request.form.get('size')
        user = current_user.get_id()
        content_to_create = Product(name=name, title=title, about=about, product_code=productCode, stock=stock, photo_1=fname, 
                                    stuff_user=user,  category=category, price=price, size=size)
        db.session.add(content_to_create)
        db.session.commit()
        return redirect(url_for('products'))
    return render_template('admin/Products/addProduct.html', categorys=categorys)


@app.route('/categorys')
def categorys():
    categorys = Category.query.all()
    return render_template('admin/Categorys/categorys.html', categorys=categorys)


@app.route('/categorys/add', methods=['GET','POST'])
def categoryAdd():
    types = Typec.query.all()
    if request.method == 'POST':
        name = request.form.get('name')
        type = request.form.get('type')
        file = request.files['photo']
        fname = file.filename
        if fname:
            file.save(os.path.join('main/static/img/categorys', secure_filename(fname)))
        content_to_create = Category(name=name, type=type, img=fname)
        db.session.add(content_to_create)
        db.session.commit()
    return render_template('admin/Categorys/addCategorys.html', types=types)


@app.route('/productdelete/<int:id>', methods=['GET', 'POST'])
def productDelete(id):
    model=Product.query.get(id)
    file = model.photo_1
    if file:
        file_path = os.path.join('main/static/img/product', file)
        os.remove(file_path)
    db.session.delete(model)
    db.session.commit()
    return redirect(url_for('products'))


@app.route('/productUpgrate/<int:id>', methods=['GET','POST'])
def productUpgrade(id):
    product = Product.query.get(id)
    categorys = Category.query.all()
 
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.title = request.form.get('title')

        product.about = request.form.get('about')
        product.stock = request.form.get('stock')
        
        product.product_code = request.form.get('productCode')
        product.size = request.form.get('size')
        product.price = request.form.get('price')
        db.session.commit()
        return redirect('productUpgrade')
    return render_template('admin/Products/upgradeProduct.html', product=product, categorys=categorys)


@app.route('/admin/request')
def adminRequest():
    products = Product.query.filter_by(control=0)
    return render_template('admin/Request/checkRequest.html',products=products)


@app.route('/admin/request/info/<int:id>', methods=['GET','POST'])
def infoRequset(id):
    products = Product.query.get(id)
    typecs = Typec.query.all()
    if request.method == 'POST':
        if request.form['submit_button'] == 'create':
            r_type = request.form.get('rtype')
            if r_type:
                content_to_create = Typec(name=r_type)
                db.session.add(content_to_create)
                db.session.commit()
            return redirect(request.referrer)
        elif request.form['submit_button'] == 'change':
            ncat = products.req_cat
            if ncat:
                print('-----------------------------------Debug--------------------------------------------------')
                category = request.form.get('ncategory')
                type = request.form.get('type')
                content_to_category = Category(name=category, type=type)
                db.session.add(content_to_category)
                db.session.commit()
                products.control = 1
                products.category = Category.query.filter_by(name=category).first().id
                db.session.commit()
                return redirect(url_for('adminRequest'))
            else:
                print('-----------------------------------Debug2--------------------------------------------------')
                products.control = 1
                db.session.commit()
                return redirect(url_for('adminRequest'))
    return render_template('admin/Request/infoRequest.html',products=products,typecs=typecs)


@app.route('/admin/request/<int:id>',methods=['GET','POST'])
def adminRequestCheck(id):
    product = Product.query.get(id)
    product.control = 1
    db.session.commit()
    return redirect(url_for('adminRequest'))

#--------------------------Session---------------------------------#-

@app.route('/test', methods=['GET', 'POST'])
def test():
    sesid = sesID()
    return render_template('test.html', sessionID=sesid)


def sesCheck():
    time = datetime.now().date()
    carts = Carto.query.all()
    for cart in carts:
        if not cart.userId:
            cartTime = cart.created_on + relativedelta(month=+1)
            if time == cartTime or time > cartTime:
                db.session.delete(cart)
                db.session.commit()
    print('test')

    
def sesID(): #-- Check Session['id']
    try:
        sessionID=session['id']
    except:
        try:
            if sessionID:
                carts = Carto.query.filter_by(sessionId=sessionID) #Delete column about old session
                db.session.delete(carts)
                db.session.commit()
        except:
            pass
        session['id'] = uuid.uuid4()
        sessionID = session['id']
    return sessionID


@app.route('/delSesId', methods=['GET', 'POST'])
def delSesId():
    del session['id']
    return redirect(url_for('test'))


#--------------------User-----------------------------------------------#


@app.route('/userLogin', methods=['GET', 'POST'])
def userLogin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.check_password_correction(attempted_password = password):
            login_user(user)
            try:
                cartos = Carto.query.filter_by(sessionId=session['id'])
                for carto in cartos:
                    carto.userId = current_user.get_id()
                    db.session.commit()
            except:
                pass
            return redirect(url_for('userLogin'))
        else:
            flash ("Email Or Password Not Correct")
            return redirect(url_for('userLogin'))             
    return render_template('userLogin.html')


@app.route('/user-registration', methods=['GET','POST'])
def userRegistration():
    if request.method == 'POST':
        name = request.form.get('name')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        number = request.form.get('phone')
        password = request.form.get('password')
        re_password = request.form.get('re-password')
        if password == re_password:
            usercontent = User(name=name, lastname=lastname, email=email, number=number, password=password)
            db.session.add(usercontent)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            flash ('Password not same')
            return redirect(url_for('userLogin'))
    return render_template('user/registration.html')


@app.route('/user-profile', methods=['GET', 'POST'])
def userProfile():
    return render_template('user/profile.html')





