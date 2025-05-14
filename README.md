# Bank Score API

A Flask-based REST API for calculating and retrieving user credit scores and related banking data. The API aggregates data from multiple MySQL databases to provide a composite "iscore" and detailed user information.

## Features

- Calculate a user's credit score (`iscore`) based on payment history, debt, account history, and credit mix.
- Retrieve detailed user data including last payment and current debt.
- CORS enabled for cross-origin requests.
- Ready for deployment with Gunicorn and a Procfile.

## Requirements

- Python 3.7+
- MySQL server
- pip (Python package manager)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ahmednasser111/bank-score-api.git
   cd bank-score-api
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up MySQL databases:**
   - Create the databases and tables by running the SQL script:
     ```bash
     mysql -u root -p < Databases
     ```
   - (Optional) Insert sample data using the `insert` file.

4. **Configure database credentials:**
   - By default, the API connects to MySQL at `localhost` with user `root` and no password. Update `database/mmm.py` if your setup differs.

## Running the API

### Development

```bash
python app.py
```

### Production (with Gunicorn)

```bash
gunicorn app:app
```

Or use the provided `Procfile` with a platform like Heroku.

## API Endpoints

### Get User Credit Score

- **Endpoint:** `/get_iscore`
- **Method:** `GET`
- **Query Parameter:** `user` (user ID)
- **Example:**
  ```
  GET /get_iscore?user=1
  ```
- **Response:**
  ```json
  {
    "paymentScore": 1.0,
    "debtScore": 0.25,
    "historyScore": 0.2,
    "mixScore": 0.2,
    "iscore": 0.395
  }
  ```

### Get User Data

- **Endpoint:** `/get_user_data`
- **Method:** `GET`
- **Query Parameter:** `user` (user ID)
- **Example:**
  ```
  GET /get_user_data?user=1
  ```
- **Response:**  
  Returns user data, scores, last payment, and current debt.

## Project Structure

```
bank-score-api/
├── app.py
├── requirements.txt
├── Procfile
├── Databases
├── insert
├── database/
│   └── mmm.py
└── .gitignore
```
