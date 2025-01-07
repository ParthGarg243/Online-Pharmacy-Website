from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import *
from django.http import HttpResponseRedirect
from django.db import connection
from django.shortcuts import redirect
from django.db import OperationalError, IntegrityError, DataError

#use views.py for serving a page
#for updating elements use ajax

#what if i need a function to just post / update and refresh
#then in that case you can use a form and redirect to a page that does the update in db and redirects to previous page
#or have the same function but instead of form you do a ajax post request and then reload the page/update

#for post and redirect same ajax/form works/ ajax better because no form resubmission headaches

#serving a page - python
#a form - html
#post and refresh - ajax
#post and redirect - html

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
            
            #Transaction 1
            try:
                with connection.cursor() as cursor:
                    #insert the data into table
                    cursor.execute('START TRANSACTION;')
                    cursor.execute('INSERT INTO customer (customer_email, customer_password, first_name, last_name, phone_number, date_of_birth, gender, membership, address_line, pincode) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);', 
                    (data_received['email'], data_received['pswd'], data_received['fname'], data_received['lname'], data_received['phone'], data_received['dob'], 'M', 'N', data_received['address'], data_received['pincode'])) 
                    connection.commit()

            except OperationalError as e:
                # Handle operational errors such as data type mismatch
                print("An operational error occurred during the insert:", e)
                # Roll back the transaction
                connection.rollback()
                return redirect('login')

            except IntegrityError as e:
                # Handle integrity errors
                print("An integrity error occurred during the insert:", e)
                # Roll back the transaction
                connection.rollback()
                return redirect('login')
            
            #create cooki
            #redirect
            response = redirect('main')
            # Set the cookie on the response object
            response.set_cookie('login_set', data_received['email'], path='/')
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
                response.set_cookie('login_set', data_received['email'], path='/')
                # Return the response
                return response
            else:
                context = {'invalid': 'Invalid credentials! Please try again!'}
                return render(request, 'login.html', context) #only instance of render because i need to pass data
        else:
            return redirect('login')

#check for 5 limit update
def main(request):
    cookie_value = request.COOKIES.get('login_set', 'no')
    print(cookie_value)
    if(cookie_value != None and cookie_value != 'no'):
        #render page shit
        #fetch all items from database
        #put relevant shit in context and pass to html
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM product WHERE stock >= 0') # out of stock if less than 5
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
            #need to check if 5 limit is reached
            data_received = request.POST
            print(data_received)
            if 'action' in data_received: #if its about updating value increment decrement 
                #check
                print(data_received['pid'])
                #update inventory and stock
                #Transaction 2
                err = False
                if (data_received['action'] == 'add'): #if stock is there                    
                   #update value of cart
                    try:
                        with connection.cursor() as cursor:
                            cursor.execute('START TRANSACTION;')
                            cursor.execute('UPDATE cart SET quantity = quantity + 1 WHERE product_id = %s and customer_email = %s ', (data_received['pid'][0], cookie_value, ))
                            connection.commit()

                    except OperationalError as e:
                        # Handle operational errors such as data type mismatch
                        print("An operational error occurred during the insert:", e)
                        # Roll back the transaction
                        connection.rollback()
                        return redirect('cart')

                    except IntegrityError as e:
                        # Handle integrity errors
                        print("An integrity error occurred during the insert:", e)
                        # Roll back the transaction
                        connection.rollback()
                        return redirect('cart')
                    
                    return redirect('cart')
  
                elif(data_received['action'] == 'remove'):
                    #update value of cart
                    with connection.cursor() as cursor:
                        cursor.execute('SELECT * FROM cart, product WHERE customer_email = %s and cart.product_id = product.product_id and cart.product_id = %s', (cookie_value, data_received['pid'][0],))
                        cart_data_product = cursor.fetchall()
                
                    print(cart_data_product)

                    #Transaction 2.5
                    newQty = cart_data_product[0][0] - 1
                    print("New Quantity = ", newQty)
                    if newQty == 0:
                        with connection.cursor() as cursor:
                            cursor.execute('START TRANSACTION;')
                            cursor.execute('DELETE FROM cart WHERE product_id = %s and customer_email = %s', (data_received['pid'][0], cookie_value, ))
                            connection.commit()
                        
                    else:
                        with connection.cursor() as cursor:
                            cursor.execute('START TRANSACTION;')
                            cursor.execute('UPDATE cart SET quantity = %s WHERE product_id = %s and customer_email = %s ', (newQty, data_received['pid'][0], cookie_value, ))
                            connection.commit()
                
                with connection.cursor() as cursor:
                    cursor.execute('SELECT * FROM cart, product WHERE customer_email = %s and cart.product_id = product.product_id', (cookie_value,))
                    cart_all = cursor.fetchall()

                print(cart_all)
                total = 0
                for item in cart_all:
                    total += item[0] * item[5]
                print(total)

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
                #transaction 4
                #print(sql_cart_data)
                if(len(sql_cart_data) == 1): #if its to be updated
                    print("piddi")
                    print(data_received)
                    try:
                        with connection.cursor() as cursor:
                            cursor.execute('START TRANSACTION;')
                            cursor.execute('UPDATE cart SET quantity = quantity + 1 WHERE product_id = %s and customer_email = %s ', (data_received['field1'][0], cookie_value, ))
                            connection.commit()

                    except OperationalError as e:
                        # Handle operational errors such as data type mismatch
                        print("An operational error occurred during the insert:", e)
                        # Roll back the transaction
                        connection.rollback()
                        return redirect('cart')

                    except IntegrityError as e:
                        # Handle integrity errors
                        print("An integrity error occurred during the insert:", e)
                        # Roll back the transaction
                        connection.rollback()
                        return redirect('cart')
                    
                    return redirect('cart')
                else: #fresh insert
                    with connection.cursor() as cursor:
                        cursor.execute('START TRANSACTION;')
                        cursor.execute('INSERT INTO cart (quantity, customer_email, product_id) VALUES (1, %s, %s)', (cookie_value, data_received['field1'][0],))        
                        connection.commit()

                #then fetch
                with connection.cursor() as cursor:
                    cursor.execute('SELECT * FROM cart, product WHERE customer_email = %s and cart.product_id = product.product_id', (cookie_value,))
                    sql_data2 = cursor.fetchall()

                print(sql_data2)
                total = 0
                for item in sql_data2:
                    total += item[0] * item[5]
                print(total)

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

            err_cookie = request.COOKIES.get('err')
            if(err_cookie != None):
                response = render(request, "cart.html", {'cart': sql_data2, 'total': total, 'total_delivery': total+5, 'error': err_cookie})

                # Delete the cookie 'my_cookie' by setting its max_age to 0
                response.delete_cookie('err')

                return response
            else:
                return render(request, "cart.html", {'cart': sql_data2, 'total': total, 'total_delivery': total+5})

            '''
            error_message = request.session.pop('error', None)
            if error_message:
                return render(request, "cart.html", {'cart': sql_data2, 'total': total, 'total_delivery': total+5, 'error': error_message})
            #then render#
            else:'''
            
    else:
        return redirect('login')

def checkout(request):
    cookie_value = request.COOKIES.get('login_set', 'no')
    #print(cookie_value)
    if(cookie_value != None and cookie_value != 'no'):
        if request.method == 'POST':
            user_data = request.POST

            pids = user_data.getlist('pid')
            qtys = user_data.getlist('qty')
                
            #main transaction5
            with connection.cursor() as cursor:
                cursor.execute('SELECT w FROM lock_stock WHERE id = %s', (1,))
                write = cursor.fetchall()

            if write[0][0] != 0: #if someones updating the stock w-w case 
                return redirect('main')
            else:#lock is free, acquire it
                print("this block")
                with connection.cursor() as cursor:
                    cursor.execute('UPDATE lock_stock SET w = 1 WHERE id = %s', (1,))

                with connection.cursor() as cursor:
                    cursor.execute('SELECT max(order_id) FROM orders')
                    order_data = cursor.fetchall()
                latestCount = order_data[0][0] + 1
                
                #building the sql query string
                SQLString = "START TRANSACTION;\nINSERT INTO orders (order_id, customer_email, status, amount, ordered_at, commission, rider_id) VALUES (%s, %s, %s, %s, %s, %s, %s);"
                SQLString = SQLString %  (latestCount, cookie_value, 'Received', user_data['total'], datetime.now(), 0, 1)

                n = len(pids)
                for i in range(n):
                    SQLString = SQLString + '\nINSERT INTO order_details (quantity, order_id, product_id) VALUES (%s, %s, %s);'
                    SQLString = SQLString % (qtys[i], latestCount, pids[i])
                    
                    SQLString = SQLString + '\nUPDATE product SET stock = stock - %s WHERE product_id = %s;'
                    SQLString = SQLString % (qtys[i], pids[i])

                SQLString = SQLString + '\nDELETE FROM cart WHERE customer_email = %s;'
                SQLString = SQLString % (cookie_value)
                SQLString = SQLString + '\nCOMMIT;'
                print(SQLString)

                try:
                    with connection.cursor() as cursor:
                        cursor.execute(SQLString)
                    connection.commit()

                except OperationalError as e:
                # Handle operational errors such as data type mismatch
                    print("An operational error occurred during the insert:", e)
                    # Roll back the transaction
                    connection.rollback()

                    for i in range(len(pids)):
                        with connection.cursor() as cursor:
                            cursor.execute('SELECT stock FROM product WHERE product_id = %s;', (pids[i],))
                            stock_data = cursor.fetchall()

                        if int(qtys[i]) > int(stock_data[0][0]):
                            #remove from cart
                            with connection.cursor() as cursor:
                                cursor.execute('DELETE FROM cart WHERE customer_email = %s and product_id = %s', (cookie_value, pids[i]))

                    with connection.cursor() as cursor:
                        cursor.execute('UPDATE lock_stock SET w = 0 WHERE id = %s', (1,))           
                    return redirect('cart')

                except IntegrityError as e:
                    # Handle integrity errors
                    print("An integrity error occurred during the insert:", e)                    
                    # Roll back the transaction
                    connection.rollback()

                    with connection.cursor() as cursor:
                        cursor.execute('UPDATE lock_stock SET w = 0 WHERE id = %s', (1,))
                    return redirect('cart')
                
                #release lock
                with connection.cursor() as cursor:
                    cursor.execute('UPDATE lock_stock SET w = 0 WHERE id = %s', (1,))

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
                response.set_cookie('admin_set', data_received['id'], path='/')
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
    #print(cookie_value)
    if(cookie_value != None and cookie_value != 'no'):
        if request.method == 'POST':
            user_data = request.POST
            #print(user_data)
            #need to check data like during signup
            #Transaction 4
            try:
                with connection.cursor() as cursor:
                    #insert the data into table
                    cursor.execute('START TRANSACTION;')
                    cursor.execute('UPDATE customer SET first_name = %s, last_name = %s, phone_number = %s, address_line = %s, pincode = %s WHERE customer_email = %s;', (user_data['fname'], user_data['lname'], user_data['phone'], user_data['address'], user_data['pin'], cookie_value))
                    connection.commit()

            except OperationalError as e:
                # Handle operational errors such as data type mismatch
                print("An operational error occurred during the insert:", e)
                # Roll back the transaction
                connection.rollback()
                return redirect('profile')

            except IntegrityError as e:
                # Handle integrity errors
                print("An integrity error occurred during the insert:", e)
                # Roll back the transaction
                connection.rollback()
                return redirect('profile')
            
            except DataError as e:
                # Handle integrity errors
                print("An integrity error occurred during the insert:", e)
                # Roll back the transaction
                connection.rollback()
                return redirect('profile')
            #update the user data
            
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

        print("orderiddd")
        print(order_id_data)
        
        order_data={}
        for order_id in order_id_data:
            #transaction 6
            #check for write lock acuire lock before user reads else redirect to profile even if one is bad
            with connection.cursor() as cursor:
                cursor.execute('SELECT w FROM lock_order WHERE order_id = %s', (order_id[0],))
                write = cursor.fetchall()
            print("write")
            print(write)
            if write[0][0] != 0: #if someones updating the status 
                return redirect('profile')
            else:
                #acquire lock
                with connection.cursor() as cursor:
                    cursor.execute('UPDATE lock_order SET r = 1 WHERE order_id = %s', (order_id[0],))
               
                with connection.cursor() as cursor:
                    cursor.execute('START TRANSACTION;')
                    cursor.execute('SELECT * FROM order_details, product WHERE order_id = %s and order_details.product_id = product.product_id; ', (order_id[0],))
                    order_data[(order_id[0], order_id[1], order_id[2])] = cursor.fetchall()
                    cursor.execute('COMMIT;')

                #release lock
                with connection.cursor() as cursor:
                    cursor.execute('UPDATE lock_order SET r = 0 WHERE order_id = %s', (order_id[0],))
        print()
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
            #acquire lock - no one else acquires the lock
            with connection.cursor() as cursor:
                cursor.execute('UPDATE lock_order SET w = 1 WHERE order_id = %s', (data_received['orderid'], ))

            try:
                #update the stock
                with connection.cursor() as cursor:
                    cursor.execute('START TRANSACTION;')
                    
                    # Update the order status
                    cursor.execute('UPDATE orders SET status = %s WHERE order_id = %s;', ("Shipped", data_received['orderid']))
                    
                    # Select pharmacist orders
                    
                    # Commit the transaction
                    connection.commit()

            except OperationalError as e: 
                # Handle operational errors
                print("An operational error occurred during the insert:", e)
                # Roll back the transaction
                connection.rollback()
                with connection.cursor() as cursor:
                    cursor.execute('UPDATE lock_order SET w = 0 WHERE order_id = %s', (data_received['orderid'], ))
                return redirect('approval')

            except IntegrityError as e:
                # Handle integrity errors
                print("An integrity error occurred during the insert:", e)
                # Roll back the transaction
                connection.rollback()
                with connection.cursor() as cursor:
                    cursor.execute('UPDATE lock_order SET w = 0 WHERE order_id = %s', (data_received['orderid'], ))
                return redirect('approval')            

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

            #release lock
            with connection.cursor() as cursor:
                cursor.execute('UPDATE lock_order SET w = 0 WHERE order_id = %s', (data_received['orderid'], ))

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
                    #acquire lock
                    with connection.cursor() as cursor:
                        cursor.execute('UPDATE lock_stock SET w = 1 WHERE id = %s', (str(1), ))
                    #do this
                    with connection.cursor() as cursor:
                        cursor.execute('START TRANSACTION;')
                        cursor.execute('SELECT stock FROM product WHERE product_id = %s;', (key,))
                        curr_stock = cursor.fetchall()
                        print(curr_stock[0][0])
                        cursor.execute('UPDATE product SET stock = %s WHERE product_id = %s;', (curr_stock[0][0] + int(data_received[key]), key))
                        cursor.execute('COMMIT;')
                    #release lock
                    with connection.cursor() as cursor:
                        cursor.execute('UPDATE lock_stock SET w = 0 WHERE id = %s', (1, ))

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