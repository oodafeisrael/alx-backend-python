# Seed Script for ALX_prodev Database
- This project contains a Python script (seed.py) that automates the creation, setup, and data population of a MySQL database named ALX_prodev. The database contains a single table user_data, and the data is loaded from a .csv file using Python’s CSV and MySQL connector libraries. The script uses environment variables for secure configuration.

##  Project Structure
alx-backend-python/
└── python-generators-0x00/
    ├── seed.py
    ├── 0-main.py
    ├── user_data.csv
    └── README.md
⚙️## Features
Connects to MySQL server.

Creates a database ALX_prodev if it doesn't exist.

Connects to the created database.

Creates a table user_data with the following schema:

user_id (UUID, Primary Key, Indexed)

name (VARCHAR, NOT NULL)

email (VARCHAR, NOT NULL)

age (DECIMAL, NOT NULL)

Inserts data from user_data.csv into the table.

Prints sample output for verification.

## Environment Setup
Before running the script, create a .env file in the same directory with the following variables:
ini
DB_HOST=localhost
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
 Install required packages using:

pip install -r requirements.txt
mysql-connector-python
python-dotenv
Ensure MySQL server is running.

Activate your virtual environment if applicable.

Run the entry point script.

###  Sample Output

connection successful
Table user_data created successfully
Database ALX_prodev is present
[('uuid1', 'John Doe', 'john@example.com', 32), ...]
###  Notes
- The script uses UUIDs as primary keys for consistency and scalability.

- Indexing is applied to user_id for performance optimization.

- Basic error handling is implemented to avoid duplicate index creation issues.

### Author
- Developed for ALX Software Engineering Backend specialization by Israel Odafe
- Email: oodafeisrael@yahoo.com
