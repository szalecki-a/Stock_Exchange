## Hashira Exchange

Hashira Exchange is an application that allows you to simulate stock market actions and manage a virtual account. It enables you to simulate buying and selling stocks, make deposits and withdrawals, and provides various account management features. The application stores data in an SQLite3 database and is deployed on a multi-threaded TCP server with new extensions.

### Prerequisites

- Python 3.6 or higher

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/szalecki-a/Stock_Exchange
   ```

2. Navigate to the project directory:
   ```bash
   cd repo_name
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

1. Import the necessary modules:
   ```python
   from datetime import datetime
   from random import uniform
   import matplotlib.pyplot as plt
   import sqlite3
   from stocks import stocks_dict
   ```

2. Initialize the required variables:
   ```python
   stocks = {}
   user_names = []
   ```

3. Define the necessary classes and functions (see code).

4. Run the program on your local terminal:
   ```bash
   python main.py
   ```

### User Guide

1. Fork the repository on GitHub.
2. Clone the forked repository to your local machine.
3. Install the required dependencies.
4. Open a terminal and navigate to the project directory.
5. Run the program using the command mentioned above.
6. Follow the instructions on the terminal to interact with the stock market simulation and manage your virtual account, including buying and selling stocks, making deposits and withdrawals, and performing various account-related actions.
7. Utilize the provided functions to view transaction history, check account balance, and perform other account-related operations.
8. Enjoy simulating stock market actions and effectively managing your virtual account!

### License

This project is licensed under the [MIT License](LICENSE).

**Note:** This project is for educational purposes only and does not involve real financial transactions.

### Updated Dependencies

- bcrypt==4.0.1
- contourpy==1.0.7
- cycler==0.11.0
- fonttools==4.39.4
- kiwisolver==1.4.4
- matplotlib==3.7.1
- numpy==1.24.3
- packaging==23.1
- pandas==2.0.1
- Pillow==9.5.0
- pyparsing==3.0.9
- python-dateutil==2.8.2
- pytz==2023.3
- six==1.16.0
- tzdata==2023.3
