# Investment Account Management System

Welcome to the Investment Account Management System, a Django-based application for managing investment accounts, transactions, and permissions. This project provides a RESTful API for managing investment accounts and transactions with advanced filtering and permissions.

## Features

- **Investment Account Management**: Create and manage investment accounts.
- **Transaction Tracking**: Record and view transactions associated with investment accounts.
- **User Permissions**: Manage account permissions to control access to accounts and transactions.
- **Admin Endpoints**: Special endpoints for admin users to view all transactions with filtering options.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Running Tests](#running-tests)
- [Contributing](#contributing)
- [License](#license)

## Installation

### Prerequisites

- Python 3.8 or later
- PostgreSQL (for production use)
- Git

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Dancunrandy/invest.git
   cd invest
   ```

2. **Set Up a Virtual Environment**

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install Dependencies**

   Ensure you have a `requirements.txt` file in your root directory. If not, create it with the following command:

   ```bash
   pip freeze > requirements.txt
   ```

   Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up the Database**

   Ensure PostgreSQL is running, and create a database named `test_db` with user `postgres` and password `postgres`.

5. **Apply Migrations**

   ```bash
   python manage.py migrate
   ```

6. **Create a Superuser**

   ```bash
   python manage.py createsuperuser
   ```

7. **Run the Development Server**

   ```bash
   python manage.py runserver
   ```

   Open your browser and navigate to `http://127.0.0.1:8000/`.

## Usage

### API Endpoints

- **Investment Accounts**
  - `GET /api/accounts/`: List all investment accounts
  - `POST /api/accounts/`: Create a new investment account
  - `GET /api/accounts/{id}/`: Retrieve a specific account
  - `PUT /api/accounts/{id}/`: Update a specific account
  - `DELETE /api/accounts/{id}/`: Delete a specific account

- **Transactions**
  - `GET /api/transactions/`: List all transactions
  - `POST /api/transactions/`: Create a new transaction
  - `GET /api/transactions/{id}/`: Retrieve a specific transaction
  - `PUT /api/transactions/{id}/`: Update a specific transaction
  - `DELETE /api/transactions/{id}/`: Delete a specific transaction

- **Admin Transactions**
  - `GET /api/admin-transactions/`: View all transactions with optional filters

## Running Tests

To run tests, use the following command:

```bash
python manage.py test
```

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature-branch`)
6. Create a new Pull Request

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


