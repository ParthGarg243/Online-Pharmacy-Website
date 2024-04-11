from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import *
from django.http import HttpResponseRedirect
from django.db import connection
from django.shortcuts import redirect

#one url one function one render
# Create your views here.
def login(request):
    #if cookies exist
    cookie_value = request.COOKIES.get('login_set', 'no')
    print(cookie_value)
    if(cookie_value != "no"):
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
    if(cookie_value != "no"):
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

            checkTuple = (data_received['phone'], data_received['pincode'], data_received['dob'])
            checkResult = checkNPD(checkTuple)
            if(checkResult[0] and checkResult[1] and checkResult[2] and len(sql_data) == 0):
                with connection.cursor() as cursor:
                    #insert the data into table
                    cursor.execute('INSERT INTO customer (customer_email, customer_password, first_name, last_name, phone_number, date_of_birth, gender, membership, address_line, pincode) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', 
                    (data_received['email'], data_received['pswd'], data_received['fName'], data_received['lName'], data_received['phone'], data_received['dob'], 'M', 'N', data_received['address'], data_received['pincode'])) 
                    
                    #create cookie

                    #redirect
                    response = redirect('main')
                    # Set the cookie on the response object
                    response.set_cookie('login_set', data_received['email'], expires='Thu, 31 Dec 2024 23:59:59 GMT', path='/')
                    # Return the response
                    return response
            else:
                #create a dictionary where you have to check for the individual things
                context = {}
                if not checkResult[0]:
                    context['number'] = "This is a invalid phone number!"
                if not checkResult[1]:
                    context['pin'] = "This is a invalid pin!"
                if not checkResult[2]:
                    context['dob'] = "You are below 18!"
                if not len(sql_data) == 0:
                    context['my_list', "This email is already in use!"]
                return render(request, 'login.html', context)
            
        else:
            return redirect('user')

        
        
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
    if(cookie_value != "no"):
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
    if(cookie_value != 'no'):
        #render page shit
        #fetch all items from database
        #put relevant shit in context and pass to html
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM product')
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
    if(cookie_value != 'no'):
        if request.method == 'POST':
            #if theres already stuff to update
            data_received = request.POST

            #update
            ''' #customer data why did i do this nigesh?
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM customer WHERE customer_email = %s', (cookie_value,))
                sql_customer = cursor.fetchall()'''
            print(data_received)
            #fetch and then delete and then insert
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM cart, product WHERE customer_email = %s and cart.product_id = product.product_id and cart.product_id = %s', (cookie_value, data_received['field1'][0],))
                sql_cart_data = cursor.fetchall()
            
            print(sql_cart_data)
            
            if(len(sql_cart_data) == 1):
                currQty = sql_cart_data[0][0]
                
                currQty += 1

                #print(data_received, sql_customer)
                print(int(data_received['field1'][0]))

                with connection.cursor() as cursor:
                    cursor.execute('DELETE FROM cart WHERE customer_email = %s and cart.product_id = %s', (cookie_value, data_received['field1'][0],))
                    cursor.execute('INSERT INTO cart (quantity, customer_email, product_id) VALUES (%s, %s, %s)', (str(currQty), cookie_value, data_received['field1'][0]))             
            else:
                 with connection.cursor() as cursor:
                    cursor.execute('INSERT INTO cart (quantity, customer_email, product_id) VALUES (1, %s, %s)', (cookie_value, data_received['field1'][0],))        

            #then fetch
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM cart, product WHERE customer_email = %s and cart.product_id = product.product_id', (cookie_value,))
                sql_data2 = cursor.fetchall()

            print(sql_data2)
            #then render
            return render(request, "cart.html", {'cart': sql_data2})
        else:
            #then fetch
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM cart, product WHERE customer_email = %s and cart.product_id = product.product_id', (cookie_value,))
                sql_data2 = cursor.fetchall()

            print(sql_data2)
            #then render
            return render(request, "cart.html", {'cart': sql_data2})

    else:
        return redirect('login')
