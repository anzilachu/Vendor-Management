Vendor Management System

This is a Vendor Management System built using Django and Django REST Framework. It allows you to manage vendor profiles, track purchase orders, and evaluate vendor performance metrics.



SetUp :-

1. git clone https://github.com/your-username/vendor-management-system.git

2. cd vendor_management_system

3. pip install -r requirements.txt

4. python manage.py migrate

5. python manage.py runserver



API Endpoints :-

1. User Registration
    Endpoint: /api/register/
    Method: POST
    Description: Register a new user.

2. User Login
    Endpoint: /api/login/
    Method: POST
    Description: Log in with username and password to obtain an authentication token.

3. User Logout
    Endpoint: /api/logout/
    Method: POST
    Description: Log out and invalidate the authentication token.

4. Vendors
    Endpoint: /api/vendors/
    Method: GET, POST
    Description: List all vendors or create a new vendor.
    Endpoint: /api/vendors/{vendor_id}/
    Method: GET, PUT, DELETE
    Description: Retrieve, update, or delete a specific vendor by ID.

5. Purchase Orders
    Endpoint: /api/purchase_orders/
    Method: GET, POST
    Description: List all purchase orders or create a new purchase order.
    Endpoint: /api/purchase_orders/{po_id}/
    Method: GET, PUT, DELETE
    Description: Retrieve, update, or delete a specific purchase order by ID.
   
6. Vendor Performance Metrics
    Endpoint: /api/vendors/{vendor_id}/performance/
    Method: GET
    Description: Retrieve performance metrics for a specific vendor.
    Acknowledge Purchase Order
    Endpoint: /api/purchase_orders/{po_id}/acknowledge/
    Method: POST
    Description: Acknowledge a purchase order and trigger recalculation of metrics.
