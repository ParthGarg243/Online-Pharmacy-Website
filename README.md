# Online Pharmacy Website
An online pharmacy website made as a part of the course project for CSE202: Fundamentals of Database Management Systems course conducted in Winter 2024.

## Features

### 1. Sign Up or Sign In
To access the features of our application, users need to sign up if they are new or sign in if they already have an account. You can find the sign-up and sign-in options on the homepage.
![alt text](<.readme_files/5.gif>)

### 2. Homepage Redirect
After signing in or signing up, users will be redirected to the homepage of our website. From there, they can browse and purchase products available in our inventory.

![alt text](.readme_files/1.gif)

### 3. Update Profile
Once signed in, users can update their profile details such as name, phone number, address, etc., from the profile section. Simply navigate to the profile section for this.

![alt text](<.readme_files/3.gif>)

### 4. View Order History
From the profile section, users can view their order history to track their previous purchases. This helps in keeping a record of all transactions made on the platform.

![alt text](<.readme_files/4.gif>)

### 5. Admin Dashboard for Pharmacists
Pharmacists have access to the admin dashboard, where they can analyze product sales, monitor stock levels, and manage order approvals.
![alt text](<.readme_files/2.gif>)

## Quick Start Guide

### Launching the Development Server
1. Install Django and other pre-requisites:
   ```bash
   pip install django mysqlclient
   ```

2. Provide database credentials in 'pharmacy/settings.py' at line 81:
![alt text](<.readme_files/db.png>)

3. Run 'coreDB/setup.sql' in your database software.

4. Run the Django development server:
   ```bash
   python manage.py runserver
   ```

5. Open your web browser and navigate to:
   ```
   http://localhost:8000/web/login/
   ``` 
