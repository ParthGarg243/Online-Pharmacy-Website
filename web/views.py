from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import *
from django.http import HttpResponseRedirect
from django.db import connection
from django.shortcuts import redirect

#use views.py for serving a page
#for updating elements use ajax

#what if i need a function to just post / update and refresh
#then in that case you can use a form and redirect to a page that does the update in db and redirects to previous page
#or have the same function but instead of form you do a ajax post request and then reload the page/update

#for post and redirect same ajax/form works/ ajax better because no form resubmission headaches

#one url one function one render
# Create your views here.
def login(request):
    #if cookies exist
    cookie_value = request.COOKIES.get('login_set', 'no')
    print(cookie_value)
    if(cookie_value != None and cookie_value != 'no'):
        return redirect('main')
    else:
        return render(request, 'login.html')

from datetime import datetime

def checkNPD(tupleNPD) -> tuple:
    #always tuple len is always 3 so dont worry for that  
    #check for number
    result = [False, False, False]
    phone = tupleNPD[0]
    if len(phone) == 10:
        result[0] = True

    pincode = tupleNPD[1]
    if len(pincode) == 6:
        result[1] = True

    #dob
    dob_date = datetime.strptime(tupleNPD[2], '%Y-%m-%d')
    current_date = datetime.now()
    age = current_date.year - dob_date.year - ((current_date.month, current_date.day) < (dob_date.month, dob_date.day))
    if age > 18:
        result[2] = True

    return result

@csrf_protect
def helperS(request):
    cookie_value = request.COOKIES.get('login_set', 'no')
    print(cookie_value)
    if(cookie_value != None and cookie_value != 'no'):
        return redirect('main')
    else:
        #theres no user logged in
        if request.method == 'POST':
            data_received = request.POST
            sql_data = []
            with connection.cursor() as cursor:
                cursor.execute('SELECT customer_email FROM customer where customer_email = %s', (data_received['email'], ))
                sql_data = cursor.fetchall()
            print(sql_data, data_received)
            print(len(sql_data))
            #Trigger 1

            with connection.cursor() as cursor:
                #insert the data into table
                cursor.execute('START TRANSACTION; INSERT INTO customer (customer_email, customer_password, first_name, last_name, phone_number, date_of_birth, gender, membership, address_line, pincode) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); COMMIT;', 
                (data_received['email'], data_received['pswd'], data_received['fname'], data_received['lname'], data_received['phone'], data_received['dob'], 'M', 'N', data_received['address'], data_received['pincode'])) 
                
                #create cooki
                #redirect
                response = redirect('main')
                # Set the cookie on the response object
                response.set_cookie('login_set', data_received['email'], expires='Thu, 31 Dec 2024 23:59:59 GMT', path='/')
                # Return the response
                return response
            #can use ajax instead of this so that you dont have to refresh the page better for security as well 
            
        else:
            return redirect('main')

        
        
    #handle the post request first of updating the db if the type is post
    #get the relevant details from db
    #check if its valid
    #if its valid
    #update html
    #then return
    #if not
    #return login.html modified to say username alr exists!

    #if type is not post then you check for cookies
    #retrieve db data and show the html
    # if not redirect to main

#PRG method #helper url
@csrf_protect
def helper(request):
    #if cookies exist
    cookie_value = request.COOKIES.get('login_set', 'no')
    print(cookie_value)
    if(cookie_value != None and cookie_value != 'no'):
        return redirect('main')
    else:
        if request.method == 'POST':
            data_received = request.POST
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM customer WHERE customer_email = %s AND customer_password = %s', (data_received['email'], data_received['pswd']))
                sql_data = cursor.fetchall()
            
            print(sql_data, data_received)
            if len(sql_data) == 1:
                # Login successful
                response = redirect('main')
                # Set the cookie on the response object
                response.set_cookie('login_set', data_received['email'], expires='Thu, 31 Dec 2024 23:59:59 GMT', path='/')
                # Return the response
                return response
            else:
                context = {'invalid': 'Invalid credentials! Please try again!'}
                return render(request, 'login.html', context) #only instance of render because i need to pass data
        else:
            return redirect('login')

def main(request):
    cookie_value = request.COOKIES.get('login_set', 'no')
    print(cookie_value)
    if(cookie_value != None and cookie_value != 'no'):
        #render page shit
        #fetch all items from database
        #put relevant shit in context and pass to html
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM product WHERE stock != 0')
            sql_data = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM customer WHERE customer_email = %s', (cookie_value,))
            sql_data1 = cursor.fetchall()
        print(sql_data1)
        # Create a dictionary
        result = {}
        for item in sql_data:
            # Extract the key (first element) and value (remaining elements as a tuple)
            key = item[0]
            value = item[1:]
            # Add the key-value pair to the dictionary
            result[key] = value
        print(result)
        return render(request, 'main.html', {'result': result, 'name': sql_data1[0][2]})
    else:   
        return redirect('login')

def cart(request):
    cookie_value = request.COOKIES.get('login_set', 'no')
    print(cookie_value)
    if(cookie_value != None and cookie_value != 'no'):
        if request.method == 'POST':
            #if theres already stuff to update
            data_received = request.POST
            print(data_received)
            if 'action' in data_received: #if its about updating value increment decrement
                #check
                print(data_received['pid'])
                with connection.cursor() as cursor:
                    cursor.execute('SELECT stock, name FROM product WHERE product_id = %s', (data_received['pid'][0],))
                    curr_product_stock = cursor.fetchall() 
                print(curr_product_stock)
                #update inventory and stock
                err = False
                if (curr_product_stock[0][0] > 0 and data_received['action'] == 'add'): #if stock is there
                    #update value of stock
                    print(curr_product_stock)
                    newStock = curr_product_stock[0][0] - 1

                    with connection.cursor() as cursor:
                        cursor.execute('UPDATE product SET stock = %s WHERE product_id = %s', (newStock, data_received['pid'][0],))
                    #update value of cart
                    with connection.cursor() as cursor:
                        cursor.execute('SELECT * FROM cart, product WHERE customer_email = %s and cart.product_id = product.product_id and cart.product_id = %s', (cookie_value, data_received['pid'][0],))
                        cart_data_product = cursor.fetchall()
                
                    print(cart_data_product)
                
                    newQty = cart_data_product[0][0] + 1

                    with connection.cursor() as cursor:
                        cursor.execute('START TRANSACTION;')
                        cursor.execute('UPDATE cart SET quantity = %s WHERE product_id = %s and customer_email = %s ', (newQty, data_received['pid'][0], cookie_value, ))
                        cursor.execute('COMMIT;')
                elif(data_received['action'] == 'remove'):
                     #update value of stock
                    newStock = curr_product_stock[0][0] + 1

                    with connection.cursor() as cursor:
                        cursor.execute('UPDATE product SET stock = %s WHERE product_id = %s', (newStock, data_received['pid'][0],))
                    #update value of cart
                    with connection.cursor() as cursor:
                        cursor.execute('SELECT * FROM cart, product WHERE customer_email = %s and cart.product_id = product.product_id and cart.product_id = %s', (cookie_value, data_received['pid'][0],))
                        cart_data_product = cursor.fetchall()
                
                    print(cart_data_product)
                
                    newQty = cart_data_product[0][0] - 1
                    if newQty == 0:
                        with connection.cursor() as cursor:
                            cursor.execute('START TRANSACTION;')
                            cursor.execute('DELETE FROM cart WHERE product_id = %s and customer_email = %s', (data_received['pid'][0], cookie_value, ))
                            cursor.execute('COMMIT;')
                    else:
                        with connection.cursor() as cursor:
                            cursor.execute('START TRANSACTION;')
                            cursor.execute('UPDATE cart SET quantity = %s WHERE product_id = %s and customer_email = %s ', (newQty, data_received['pid'][0], cookie_value, ))
                            cursor.exectue('COMMIT;')
                elif(curr_product_stock[0][0] == 0 and data_received['action'] == 'add'): #if stock is not there
                    #then fetch
                    err = True
                
                with connection.cursor() as cursor:
                    cursor.execute('SELECT * FROM cart, product WHERE customer_email = %s and cart.product_id = product.product_id', (cookie_value,))
                    cart_all = cursor.fetchall()

                print(cart_all)
                total = 0
                for item in cart_all:
                    total += item[0] * item[5]
                print(total)

                #then render#
                if err: # need  to fix a appropriate error message for out of stock
                    #append to the item and uhhhhhh yeah so if it matches pid and then append it to the thing and thang
                    return render(request, "cart.html", {'cart': cart_all, 'total': total, 'total_delivery': total+5, 'error': curr_product_stock[0][1] + ' is out of stock!'})
                else:
                    return render(request, "cart.html", {'cart': cart_all, 'total': total, 'total_delivery': total+5})
        
                        #update
                    #update cart
                    #update stock

                #render

            else: #if its add cart from main
                #update #for out of stock make changes on main and blur out the button so you cant add

                ''' #customer data why did i do this nigesh?
                with connection.cursor() as cursor:
                    cursor.execute('SELECT * FROM customer WHERE customer_email = %s', (cookie_value,))
                    sql_customer = cursor.fetchall()'''
                #fetch and then delete and then insert
                with connection.cursor() as cursor:
                    cursor.execute('SELECT * FROM cart, product WHERE customer_email = %s and cart.product_id = product.product_id and cart.product_id = %s', (cookie_value, data_received['field1'][0],))
                    sql_cart_data = cursor.fetchall()
                
                print(sql_cart_data)
                
                if(len(sql_cart_data) == 1): #if its to be updated
                    currQty = sql_cart_data[0][0] + 1

                    #print(data_received, sql_customer)
                    print(int(data_received['field1'][0]))

                    with connection.cursor() as cursor:
                        cursor.execute('START TRANSACTION')
                        cursor.execute('UPDATE cart SET quantity = %s WHERE product_id = %s and customer_email = %s ', (currQty, data_received['field1'][0], cookie_value, ))
                        cursor.execute('COMMIT;')
                else: #fresh insert
                    with connection.cursor() as cursor:
                        cursor.execute('START TRANSACTION')
                        cursor.execute('INSERT INTO cart (quantity, customer_email, product_id) VALUES (1, %s, %s)', (cookie_value, data_received['field1'][0],))        
                        cursor.execute('COMMIT;')
                #update stock
    
                with connection.cursor() as cursor:
                    cursor.execute('SELECT stock, name FROM product WHERE product_id = %s', (data_received['field1'][0],))
                    curr_product_stock = cursor.fetchall() 
                
                newStock = curr_product_stock[0][0] - 1

                with connection.cursor() as cursor:
                    cursor.execute('UPDATE product SET stock = %s WHERE product_id = %s', (newStock, data_received['field1'][0],))


                #then fetch
                with connection.cursor() as cursor:
                    cursor.execute('SELECT * FROM cart, product WHERE customer_email = %s and cart.product_id = product.product_id', (cookie_value,))
                    sql_data2 = cursor.fetchall()

                print(sql_data2)
                total = 0
                for item in sql_data2:
                    total += item[0] * item[5]
                print(total)

                #then render
                return render(request, "cart.html", {'cart': sql_data2, 'total': total, 'total_delivery': total+5})
        else:
            #then fetch
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM cart, product WHERE customer_email = %s and cart.product_id = product.product_id', (cookie_value,))
                sql_data2 = cursor.fetchall()

            print(sql_data2)
            total = 0
            for item in sql_data2:
                total += item[0] * item[5]
            print(total)

            #then render#
            return render(request, "cart.html", {'cart': sql_data2, 'total': total, 'total_delivery': total+5})
            
    else:
        return redirect('login')

def checkout(request):
    cookie_value = request.COOKIES.get('login_set', 'no')
    print(cookie_value)
    if(cookie_value != None and cookie_value != 'no'):
        if request.method == 'POST':
            user_data = request.POST
            print(user_data)

            pids = user_data.getlist('pid')
            qtys = user_data.getlist('qty')

            print(pids)
            print(qtys)
            
            #find the new new boy in the town
            with connection.cursor() as cursor:
                cursor.execute('SELECT max(order_id) FROM orders')
                order_data = cursor.fetchall()
            
            latestCount = order_data[0][0] + 1
            print(latestCount)

            print(user_data['total'])
            #order_id INT PRIMARY KEY NOT NULL,
            #put in order_history
            with connection.cursor() as cursor:
                cursor.execute('INSERT INTO orders (order_id, customer_email, status, amount, ordered_at, commission, rider_id) VALUES (%s, %s, %s, %s, %s, %s, %s)', (latestCount, cookie_value, 'Received', user_data['total'], datetime.now(), 0, 1))

            #need to fix rider and comisssion , default value for now 0
            
            #put in order_details
            n = len(pids)
            for i in range(n):
                currProduct = pids[i]
                currQty = qtys[i]

                with connection.cursor() as cursor:
                    cursor.execute('INSERT INTO order_details (quantity, order_id, product_id) VALUES (%s, %s, %s)', (currQty, latestCount, currProduct))        
            
            #delete from cart
            with connection.cursor() as cursor:
                cursor.execute('DELETE FROM cart WHERE customer_email = %s', (cookie_value,))

            #should fix resubmission form

            return render(request, 'thankyou.html')
        else:
            return redirect('main')
            
    else:
        return redirect('login')

@csrf_protect
def admin(request):
    cookie_value = request.COOKIES.get('admin_set', 'no')
    print(cookie_value)
    if(cookie_value != None and cookie_value != 'no'):
        return redirect('dashboard')
    else:
        #if its post or not
        if request.method == 'POST':
            data_received = request.POST
            print(data_received)

            #check db
            with connection.cursor() as cursor:
                cursor.execute('SELECT pharmacist_id, pharmacist_password FROM pharmacist WHERE pharmacist_id = %s AND pharmacist_password = %s', (data_received['id'], data_received['pswd']))
                sql_data = cursor.fetchall()
            
            if len(sql_data) == 1:
                #redirect
                response = redirect('dashboard')
                response.set_cookie('admin_set', data_received['id'], expires='Thu, 31 Dec 2024 23:59:59 GMT', path='/')
                return response
            else:
                context = {'invalid': 'Invalid credentials! Please try again!'}
                return render(request, 'adminLogin.html', context)

        else:
            return render(request, 'adminLogin.html')

def dashboard(request):
    cookie_value = request.COOKIES.get('admin_set', 'no')
    print(cookie_value)
    if(cookie_value != None and cookie_value != 'no'):
        #stick to page
        #fetch values
        with connection.cursor() as cursor:
            cursor.execute('SELECT name, image_path, buys, stock FROM product as p, (SELECT sum(quantity) As \'buys\', product_id FROM order_details GROUP BY product_id) as r WHERE p.product_id = r.product_id')

            sql_data = cursor.fetchall()
        print(sql_data)
        #then send
        return render(request, 'productStats.html', {'stats' : sql_data})
    else:
        redirect('admin')

def profile(request):
    #only on logout you set the cookie to no
    cookie_value = request.COOKIES.get('login_set')
    print(cookie_value)
    if(cookie_value != None and cookie_value != 'no'):
        #fetch user data
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM customer WHERE customer_email = %s', (cookie_value,))
            user_data = cursor.fetchall()
        print(user_data)
        return render(request, 'profile.html', {'user': user_data[0], 'order_history': None})
    else:
        return redirect('login')
    
def update (request):
    cookie_value = request.COOKIES.get('login_set')
    print(cookie_value)
    if(cookie_value != None and cookie_value != 'no'):
        if request.method == 'POST':
            user_data = request.POST
            print(user_data)
            #need to check data like during signup

            
            #update the user data
            with connection.cursor() as cursor:
                cursor.execute('START TRANSACTION; UPDATE customer SET first_name = %s, last_name = %s, phone_number = %s, address_line = %s, pincode = %s WHERE customer_email = %s; COMMIT;', (user_data['fname'], user_data['lname'], user_data['phone'], user_data['address'], user_data['pin'], cookie_value))
            
            return redirect('profile')
            
        else:
            return redirect('profile')
    else:
        return redirect('login')
    
#only a get request
def history(request):
    cookie_value = request.COOKIES.get('login_set')
    print(cookie_value)
    if(cookie_value != None and cookie_value != 'no'):
        #fetch all the order id's
        with connection.cursor() as cursor:
            cursor.execute('SELECT order_id, amount, status  FROM orders WHERE customer_email = %s', (cookie_value,))
            order_id_data = cursor.fetchall()

        print(order_id_data)
        
        order_data={}
        for order_id in order_id_data:
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM order_details, product WHERE order_id = %s and order_details.product_id = product.product_id', (order_id[0],))
                order_data[(order_id[0], order_id[1], order_id[2])] = cursor.fetchall()

        print(order_data)
        return render(request, 'orderHistory.html', {'orders': order_data})
    else:
        return redirect('login')
    
def approval(request):
    #cache check
    cookie_value = request.COOKIES.get('admin_set', 'no')
    print(cookie_value)
    if(cookie_value != None and cookie_value != 'no'):
        if request.method == 'POST':
            #update and fetch couldve used ajax
            data_received = request.POST
            print(data_received)
            #update the stock
            with connection.cursor() as cursor:
                cursor.execute('START TRANSACTION;')
                
                # Update the order status
                cursor.execute('UPDATE orders SET status = %s WHERE order_id = %s;', ("Processing", data_received['orderid']))
                
                # Select pharmacist orders
                
                # Commit the transaction
                cursor.execute('COMMIT;')

                # Fetch the pharmacist orders
            with connection.cursor() as cursor:
                cursor.execute('select orders.order_id, orders.amount from pharmacist, order_approval, orders where pharmacist.pharmacist_id = %s and pharmacist.pharmacist_id = order_approval.pharmacist_id and order_approval.order_id = orders.order_id and orders.status = %s', (cookie_value, "Received"))
                pharmacist_orders = cursor.fetchall()

            print(pharmacist_orders)
            order_data={}
            for order_id in pharmacist_orders:
                with connection.cursor() as cursor:
                    cursor.execute('SELECT * FROM order_details, product WHERE order_id = %s and order_details.product_id = product.product_id', (order_id[0],))
                    order_data[(order_id[0], order_id[1])] = cursor.fetchall()

            print(order_data)
            return render(request, 'orderApproval.html', {'order': order_data})
                   
        else:
            #just fetch
            with connection.cursor() as cursor:
                cursor.execute('select orders.order_id, orders.amount from pharmacist, order_approval, orders where pharmacist.pharmacist_id = %s and pharmacist.pharmacist_id = order_approval.pharmacist_id and order_approval.order_id = orders.order_id and orders.status = %s', (cookie_value, "Received"))
                pharmacist_orders = cursor.fetchall()
            print(pharmacist_orders)

            #again go through each order and make a dictionary
            order_data={}
            for order_id in pharmacist_orders:
                with connection.cursor() as cursor:
                    cursor.execute('SELECT * FROM order_details, product WHERE order_id = %s and order_details.product_id = product.product_id', (order_id[0],))
                    order_data[(order_id[0], order_id[1])] = cursor.fetchall()

            print(order_data)
            return render(request, 'orderApproval.html', {'order': order_data})
    else:
        return redirect('admin')
    
def stock(request):
    cookie_value = request.COOKIES.get('admin_set', 'no')
    print(cookie_value)
    if(cookie_value != None and cookie_value != 'no'):
        if request.method == 'POST': #if updating value
            data_received = request.POST
            print(data_received)
            
            for key in data_received:
                if key != 'csrfmiddlewaretoken':
                    with connection.cursor() as cursor:
                        cursor.execute('SELECT stock FROM product WHERE product_id = %s', (key,))
                        curr_stock = cursor.fetchall()
                        print(curr_stock[0][0])
                        cursor.execute('UPDATE product SET stock = %s WHERE product_id = %s', (curr_stock[0][0] + int(data_received[key]), key))
            
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM product')
                product_data = cursor.fetchall()
            print(product_data)
            return render(request, 'stock.html', {'products': product_data})
        
        else: #if just fetching
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM product')
                product_data = cursor.fetchall()
            print(product_data)
            return render(request, 'stock.html', {'products': product_data})
    else:
        return redirect('admin')