# Online Pharmacy Website

An online pharmacy website made as a part of the course project for CSE202: Fundamentals of Database Management Systems course conducted in Winter 2024.

## Features

### 1. Sign Up or Sign In
To access the features of our application, users need to sign up if they are new or sign in if they already have an account. You can find the sign-up and sign-in options on the homepage.

### 2. Homepage Redirect
After signing in or signing up, users will be redirected to the homepage of our website. From there, they can browse and purchase products available in our inventory.

### 3. Update Profile
Once signed in, users can update their profile details such as name, phone number, address, etc., from the profile section. Simply navigate to the profile section for this.

### 4. View Order History
From the profile section, users can view their order history to track their previous purchases. This helps in keeping a record of all transactions made on the platform.

### 5. Update Cart Items and Quantity
Users can update their cart items by navigating to the cart section. Here, they can remove or update the quantity of products they wish to purchase before proceeding to checkout.

### 6. Approval Request for Orders
Whenever a user places an order, an approval request will be automatically sent to the pharmacist. The order will only be processed and delivered after approval from the pharmacist.

### 7. Sign Out
Users can sign out of their account by accessing the profile section and selecting the "Sign Out" option.

### 8. Admin Dashboard for Pharmacists
Pharmacists have access to the admin dashboard, where they can analyze product sales, monitor stock levels, and manage order approvals.

### 9. Approve Orders from Dashboard
Pharmacists can approve pending orders directly from the admin dashboard. Upon reviewing the order details, they can approve or reject orders.

### 10. Update Stock
Pharmacists have the authority to update stock levels whenever an item runs out of stock. They can replenish stock quantities through the admin dashboard to ensure continuous availability of products for users.

## Quick Start Guide

### Launching the Development Server

1. Activate the virtual environment:
   ```bash
   pipenv shell
   ```

2. Run the Django development server:
   ```bash
   python manage.py runserver
   ```

3. Open your web browser and navigate to:
   ```
   http://localhost:8000/web/login/
   ```
