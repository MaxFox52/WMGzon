from flask import Flask, render_template, url_for, redirect, request
import json
from jsonmanager import ProductManager
from models import Product

app = Flask(__name__)

#################################### Misc ####################################

loginErrorInfo = ""
createAccountErrorInfor = ""

possible_storage = [16, 32, 64, 128, 256, 512, 1, 2, 4]


filteredBrands = []
filteredRatings = []
priceDict = {
        "filteredBrands":[],
        "filteredRatings":[],
        "priceLower":0,
        "priceUpper":99999
    }

#################################### Users / Accounts ####################################

#users
class User:
    def __init__(self, id, email, password, permission, first_name, last_name, basket_count):
        self.id = id
        self.email = email
        self.password = password
        self.permission = permission
        self.first_name = first_name
        self.last_name = last_name
        self.basket_count = basket_count
        
#list of users
class UserList:
    UserArray = []
    def addUser(self, User):
        self.UserArray.append(User)

OpenedJSONUser = open("static/User.json")

ReadJSONUser = json.load(OpenedJSONUser)

#used to fill the array in "UserList"
def user_populate(data):
    values = []
    for key in data:
        values.append(data[key])
    return values

UserListObj = UserList()
for each in ReadJSONUser:
    values = user_populate(each)
    id = values[0]
    email = values[1]
    password = values[2]
    permissions = values[3]
    first_name = values[4]
    last_name = values[5]
    basket_count = values[6]
    UserData = User(id, email, password, permissions, first_name, last_name, basket_count)
    UserListObj.addUser(UserData)

CurrentUser = None

#################################### Interacting with Products ####################################

@app.route('/product-details/<int:indexID>')
def detail(indexID):
    # getting details of one specific product to display on the page
    aPManager = ProductManager()
    aProduct = aPManager.getProduct(indexID)
    if aProduct is not None:
        return render_template('Product-Details.html', product = aProduct)
    return redirect(url_for('phones_page'))

@app.route('/product-editing')
@app.route('/product-editing/<int:indexID>')
def form(indexID=None):
    aProduct = None
    if indexID is not None:
        aPManager = ProductManager()
        aProduct = aPManager.getProduct(indexID)
    return render_template('Edit-Save-Product.html', indexID=indexID, product = aProduct, possible_storage = possible_storage)

@app.route('/save', methods=['POST'])
def save():
    aProduct = Product.populate(request.form)
    # setting storage sizes
    aProduct.storage_sizes = []
    for i in range (len(possible_storage)):
        checkbox_value = request.form.get(str(possible_storage[i]))
        if(checkbox_value):
            aProduct.storage_sizes.append(possible_storage[i])
    # colours
    aProduct.colours = request.form.getlist("entries[]")
    # sellerid
    aProduct.sellerid = CurrentUser.email
    # rating
    aProduct.rating = aProduct.rating
    # finalising product
    aPManager = ProductManager()
    aPManager.insertProduct(aProduct)
    return redirect(url_for('phones_page'))

@app.route('/update/<int:indexID>', methods=['GET', 'POST'])
def update(indexID):
    global CurrentUser
    # setting most values that don't have other complications
    aProduct = Product.populate(request.form)
    # setting id
    aProduct.id = indexID
    # setting storage sizes
    aProduct.storage_sizes = []
    for i in range (len(possible_storage)):
        checkbox_value = request.form.get(str(possible_storage[i]))
        if(checkbox_value):
            aProduct.storage_sizes.append(possible_storage[i])
    # colours
    aProduct.colours = request.form.getlist("entries[]")
    # sellerid
    aProduct.sellerid = CurrentUser.email
    # rating
    aProduct.rating = aProduct.rating
    # finalising product
    aPManager = ProductManager()
    aPManager.updateProduct(indexID, aProduct)
    return redirect(url_for('phones_page'))

@app.route('/delete/<int:indexID>', methods=['GET'])
def delete(indexID):
    aPManager = ProductManager()
    aPManager.deleteProduct(indexID)
    return redirect(url_for('phones_page'))

#################################### Pages ####################################

@app.route('/')
def landing_page():
    return render_template('Landing-Page.html', page_name="Landing Page", CurrentUser = CurrentUser)

@app.route('/phones')
def phones_page():
    aPManager = ProductManager()
    products = aPManager.getProducts()
    return render_template('Phones-Page.html', page_name="Phones Page", products = products, CurrentUser = CurrentUser,  priceDict = priceDict, filteredBrands = filteredBrands, filteredRatings = filteredRatings)

@app.route('/login')
def login():
    global loginErrorInfo

    # user is logged into an account
    if CurrentUser is not None:
        return redirect(url_for('form_login'))
    # user is NOT logged into an account
    else:
        loginErrorInfo = request.args.get('loginErrorInfo', '')
        return render_template("Login-Page.html", page_name="Login", CurrentUser = CurrentUser, loginErrorInfo=loginErrorInfo)

@app.route('/account', methods=['GET', 'POST'])
def form_login():
    global CurrentUser

    # user is logged into an account
    if CurrentUser is not None:
        return render_template('Account-Management.html', page_name="Account Management", CurrentUser=CurrentUser)
    # user is NOT logged into an account
    else:
        tempemail = request.form['username']
        temppass = request.form['password']

        # checking login details against the database to see if they can log in
        for each in UserListObj.UserArray:
            if each.email == tempemail and each.password == temppass:
                CurrentUser = each
                return render_template('Account-Management.html', page_name="Account Management", CurrentUser=CurrentUser)
        
        return redirect(url_for('login', loginErrorInfo="Invalid Information"))

@app.route('/logout')
def LogOut():
    global CurrentUser
    CurrentUser = None
    return redirect(url_for('login', loginErrorInfo=""))

@app.route('/create-account')
def CreateAccount():
    return render_template('Create-Account.html', page_name="Create Account")

@app.route('/create-account-form', methods=['GET', 'POST'])
def CreateAccountForm():

    # get all entered data
    account_em = request.form['account_em']
    account_fn = request.form['account_fn']
    account_ln = request.form['account_ln']
    account_pw = request.form['account_pw']
    account_cpw = request.form['account_cpw']

    # check if passwords match
    if account_pw != account_cpw:
        return redirect(url_for('CreateAccount', createAccountErrorInfor="Passwords do not match"))

    # check if email is already in database
    for each in UserListObj.UserArray:
        if each == account_em:
            return redirect(url_for('CreateAccount', createAccountErrorInfor="Email already exists"))

    # create account
    if request.form.get('account_seller'):
        permissionsLevel = "Seller"
    else:
        permissionsLevel = "User"

    filename = "static/User.json"

    with open(filename, 'r') as file:
        data = json.load(file)

        indexID = data[-1]['ID'] + 1

        temp_dict = {
            "ID": indexID,
            "Email": account_em,
            "Password": account_pw,
            "Permissions": permissionsLevel,
            "First_Name": account_fn,
            "Last_Name": account_ln,
            "Basket_Count": 0
        }

        if isinstance(data, list):
            data.append(temp_dict)
        elif isinstance(data, dict):
            new_key = 'new_entry'  # Make sure this key is unique in your dictionary
            data[new_key] = temp_dict

    # Write the updated data back to the file
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

    return redirect(url_for('login', loginErrorInfo=""))

@app.route('/filter-products', methods=['GET', 'POST'])
def FilterProducts():
    global filteredBrands
    global filteredRatings
    global priceDict

    # brand filtering
    if request.form.get('apple_brand'):
        filteredBrands.append("admin@apple.com")
    if request.form.get('samsung_brand'):
        filteredBrands.append("admin@samsung.com")
    if request.form.get('oneplus_brand'):
        filteredBrands.append("admin@oneplus.com")
    if request.form.get('google_brand'):
        filteredBrands.append("admin@google.com")
    if request.form.get('huawei_brand'):
        filteredBrands.append("admin@huawei.com")
    if request.form.get('xiaomi_brand'):
        filteredBrands.append("admin@xiaomi.com")

    priceDict = {
        "priceLower":0,
        "priceUpper":99999
    }
    return redirect(url_for('phones_page', priceDict = priceDict, filteredBrands = filteredBrands, filteredRatings = filteredRatings))

@app.route('/resetFilters')
def resetFilters():
    global filteredBrands
    global filteredRatings
    global priceDict

    priceDict = {
        "priceLower":0,
        "priceUpper":99999
    }

    filteredBrands = []
    filteredRatings = []

    return redirect(url_for('phones_page', priceDict = priceDict, filteredBrands = filteredBrands, filteredRatings = filteredRatings))

#################################### Start ####################################

if __name__ == "__main__":
    app.run(debug=True)