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

'''
@csrf_protect
def mainSignUp(request):
    if request.method == 'POST':
        data_received = request.POST
        sql_data = []
        with connection.cursor() as cursor:
            cursor.execute('SELECT customer_email FROM customer where customer_email = \'%s\'', data_received['email'])
            sql_data = cursor.fetchall()
        print(sql_data, data_received)
        
        #Trigger 1
        if len(data_received) == 0:
            #no duplicates
                #post the db, update the main with the guys name
                with connection.cursor() as cursor:
                    #insert the data into table
                    second_name = ''
                    temp = data_received['txt'].split()
                    if len(data_received['txt'].split()) == 1:
                        second_name = ''
                    else:
                        second_name = temp[1]
                    cursor.execute('INSERT INTO customer (customer_email, customer_password, first_name, last_name, phone_number, date_of_birth, gender, membership, address_line, pincode) VALUES (\'%s\', \'%s\', \'%s\', \'%s\', %d, \'%s\', \'%s\', \'%s\', \'%s\', %d)', 
                                   data_received['email'], data_received['pswd'], data_received['txt'].split()[0], second_name, data_received['phone'], data_received['dob'], 'M', 'N', data_received['pincode'])
                #if fail
                #else with context
                #context name
                return render(request, 'main.html')
        else:
            context = {'my_list': 'The given email is already in use!'}
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
'''

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

            #update
            #customer data
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM customer WHERE customer_email = %s', (cookie_value,))
                sql_data1 = cursor.fetchall()

            data_received = request.POST
            print(data_received, sql_data1)
            print(int(data_received['field1'][0]))
            with connection.cursor() as cursor:
                cursor.execute('INSERT INTO cart (quantity, customer_email, product_id) VALUES (1, %s, %s)', (cookie_value, data_received['field1'][0]))               

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
