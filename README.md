# Democrance Insurance Project

This project is a Django-based API for managing insurance customers, policies, and related operations.

**Workflow:**
-    Create a new customer
-    Create a new quote for a customer (Quote State: New)
-    Once presented to customer update quote status (Quote State: Quoted)
-    Once customer accepts the quote, update quote status (Quote State: Accepted)
-    Once customer pays for the quote, update quote status (Quote State: Bound)
-    Once the policy is in effect and coverage is provided. Update policy status (Policy State: Active)
-    Find Customer by name, policy type, dob
-    Get all policies for a customer
-    Get policy details
-    Get policy status history


## Setup

1. Make commands to setup, install, migrate and run the django server. This will also install the dependencies required to run the project.
   ```
   make all
   ```

2. To run the tests:
   ```
   make test
   ```



## API Endpoints

    To interact with the API endpoints, one can use tools like cURL, Postman, or any HTTP client or the below django rest client.
    ```
    http://127.0.0.1:8000/api/v1/
    ```

### Customer

- **Create Customer**
  - URL: `http://127.0.0.1:8000/api/v1/customer/`
  - Method: POST
  - Body: 
    ```json
    {
      "first_name": "Hello",
      "last_name": "World",
      "dob": "1989-02-14"
    }
    ```
  - Response   :
    ```json
    {
        "id": 3,
        "first_name": "Hello",
        "last_name": "World",
        "dob": "1989-02-14"
    }
    ```
    
- **Get Customer**
  - URL: `http://127.0.0.1:8000/api/v1/customer/3/`
  - Method: POST
  - Response   :
    ```json
    {
        "id": 3,
        "first_name": "Hello",
        "last_name": "World",
        "dob": "1989-02-14"
    }
    ```

- **Search Customer**
  - URL: `http://127.0.0.1:8000/api/v1/customer/search/?policy_type=life` or 
  `http://127.0.0.1:8000/api/v1/customer/search/?name=Ben&dob=08-02-2000&policy_type=Life`
  - Method: GET
  - Query Parameters:
    - `name`: Search by customer name
    - `dob`: Search by date of birth (format: dd-mm-yyyy)
    - `policy_type`: Search by policy type
  - Response:
    ```json
    [
        {
            "id": 2,
            "first_name": "Ben",
            "last_name": "Stoke",
            "dob": "2000-02-08"
        },
        {
            "id": 3,
            "first_name": "Hello",
            "last_name": "World",
            "dob": "1989-02-14"
        }
    ]
    ```



### Policy

- **Create Quote**
  - URL: `http://127.0.0.1:8000/api/v1/quote/`
  - Method: POST
  - Body:
    ```json
    {
      "customer_id": 3,
      "policy_type": "home"
    }
    ```
   - Response:
    ```
    {
        "id": 5,
        "customer": "Hello World 1989-02-14",
        "policy_type": "home",
        "premium": "300.00",
        "cover": "200000.00",
        "state": "new",
        "created_at": "2024-10-06T19:55:36.835106Z",
        "updated_at": "2024-10-06T19:55:36.835684Z"
    }
    ```

- **Accept Quote**
  - URL: `http://127.0.0.1:8000/api/v1/quote/5/`
  - Method: PATCH
  - Body:
    ```json
    {
        "id": 5,
        "state": "accepted"
    }
    ```
  - Response:
    ```
    {
        "id": 5,
        "customer": "Hello World 1989-02-14",
        "policy_type": "home",
        "premium": "300.00",
        "cover": "200000.00",
        "state": "accepted",
        "created_at": "2024-10-06T19:55:36.835106Z",
        "updated_at": "2024-10-06T20:01:16.556492Z"
    }
    ```


- **Pay for Quote**
  - URL: `/api/v1/quote/{policy_id}/pay/`
  - Method: PUT
  - Body:
    ```json
    {
      "id" : 5,  
      "payment_method": "Stripe"
    }
    ```
  - Response:
    ```
    {
        "message": "Payment is successfully processed"
    }
    ```

- **List Policies for Customer**
  - URL: `http://127.0.0.1:8000/api/v1/policies/?customer_id=3`
  - Method: GET
  - Query Parameters:
    - `customer_id`: ID of the customer
  - Response:
    ```
    [
        {
            "id": 5,
            "customer": "Hello World 1989-02-14",
            "policy_type": "home",
            "premium": "300.00",
            "cover": "200000.00",
            "state": "active",
            "created_at": "2024-10-06T19:55:36.835106Z",
            "updated_at": "2024-10-06T20:05:52.904553Z"
        },
        {
            "id": 6,
            "customer": "Hello World 1989-02-14",
            "policy_type": "life",
            "premium": "300.00",
            "cover": "200000.00",
            "state": "new",
            "created_at": "2024-10-06T20:07:50.071446Z",
            "updated_at": "2024-10-06T20:07:50.071780Z"
        }
    ]
    ```


- **Get Policy History**
  - URL: `http://127.0.0.1:8000/api/v1/policies/7/history/`
  - Method: GET
  - Response:
    ```
    [
        {
            "id": 11,
            "policy": 7,
            "state": "active",
            "updated_at": "2024-10-06T20:18:59.818216Z"
        },
        {
            "id": 10,
            "policy": 7,
            "state": "bound",
            "updated_at": "2024-10-06T20:18:39.803732Z"
        },
        {
            "id": 9,
            "policy": 7,
            "state": "accepted",
            "updated_at": "2024-10-06T20:18:18.815596Z"
        },
        {
            "id": 8,
            "policy": 7,
            "state": "quoted",
            "updated_at": "2024-10-06T20:18:08.724127Z"
        },
        {
            "id": 7,
            "policy": 7,
            "state": "new",
            "updated_at": "2024-10-06T20:17:07.810532Z"
        }
    ]
    ```
  

