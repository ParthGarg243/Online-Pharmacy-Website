# DBMS_Project
मेडिकल स्टोर

pipenv shell

python manage.py runserver

http://localhost:8000/web/login/

Outstanding issues:

fix images to blob rather than path
Rider part
more buttons for shipped in pharmacist
support
adding profile pic
adding new product
can fix cart update into ajax and profile update as well and add to new menu
infact everything so as to avoid form submission re error
broker trigger - manually updating stock items
Fix update details check data
fix signup error js

CONFLICT 1
[9:16 AM, 4/21/2024] Rayyan Hussain: if a user is trying to checkout(read stock value) when the manager is trying to update stock, manager acquires lock
            #check for lock
            with connection.cursor() as cursor:
                cursor.execute('SELECT w FROM lock_stock WHERE id = %s', (0,))
                write = cursor.fetchall()
            
            if write[0][0] != 0: #if someones updating the stock w-w case
                redirect('main')
            else:
                #acquire lock
                with connection.cursor() as cursor:
                    cursor.execute('UPDATE lock_stock SET w = 1 WHERE id = %s', (0,))
                #perform read
                #check for out of stock and remove that from cart and redirect back
                for i in range(len(pids)):
                    with connection.cursor() as cursor:
                        cursor.execute('BEGIN TRANSACTION;')
                        cursor.execute('SELECT stock FROM product WHERE product_id = %s;', (pids[i],))
                        cursor.execute('COMMIT;')
                        stock_data = cursor.fetchall()

            
                errTuple = []
                err = False
                print(stock_data)
                if int(qtys[i]) > int(stock_data[0][0]):
                    #remove from cart
                    err = True
                    with connection.cursor() as cursor:
                        cursor.execute('DELETE FROM cart WHERE customer_email = %s and product_id = %s', (cookie_value, pids[i]))
                    errTuple.append(pids[i])   
                
                #leave lock
                    with connection.cursor() as cursor:
                        cursor.execute('UPDATE lock_stock SET w = 0 WHERE id = %s', (0,))
[9:20 AM, 4/21/2024] Rayyan Hussain: Manager acquiring lock
[9:20 AM, 4/21/2024] Rayyan Hussain: for key in data_received:
                if key != 'csrfmiddlewaretoken':
                    #acquire lock
                    with connection.cursor() as cursor:
                        cursor.execute('UPDATE lock_stock SET w = 1 WHERE id = %s', (0))
                    #do this
                    with connection.cursor() as cursor:
                        cursor.execute('SELECT stock FROM product WHERE product_id = %s', (key,))
                        curr_stock = cursor.fetchall()
                        print(curr_stock[0][0])
                        cursor.execute('UPDATE product SET stock = %s WHERE product_id = %s', (curr_stock[0][0] + int(data_received[key]), key))
                    #release lock
                        with connection.cursor() as cursor:
                            cursor.execute('UPDATE lock_stock SET w = 0 WHERE id = %s', (0))

CONFLICT 2:
