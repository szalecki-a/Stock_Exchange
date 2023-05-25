from random import uniform
import bcrypt
import json
import sqlite3
import sys
from stocks import stocks_dict, display_stocks
from clases import User, Stock, stocks, users

#HEAD
def stock_exchange():
    initialize_stocks()
    greet()
    start_menu()

#GREETING
def greet():
  print("Welcome to the Hashira Exchange")
  print("This project allows you to simulate stock market actions.")

#MENU
def start_menu():
    while True:
        print("1. Create an account")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            user = create_account()
            if user is not None:
                logged_in(user)
            break
        elif choice == "2":
            user = login()
            if user is not None:
                logged_in(user)
            break
        elif choice == "3":
            print("Thanks for visiting Hashira Exchange!\n Hope we'll see you soon!")
            sys.exit()
        else:
            print("Invalid choice. Please try again.")

def create_account():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    name = input("Set your account name: (type 'exit' if you want to return to the main menu)  ")
    if name == "exit":
        start_menu()
    else:
        password = input("Set your account password: ")
        cursor.execute("SELECT name FROM users WHERE name=?", (name,))
        result = cursor.fetchone()
        if result is None and name != "":
            user = User(name, password)
            print("Account created successfully!")
            print("Account name:", user.name)
        else:
            print("This username is already in use or invalid. Please enter a different username.")
            connection.close()
            return create_account()
        connection.close()
        return user


def login():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    name = input("Enter your account name: (type 'exit' if you want to return to the main menu)  ")
    if name == "exit":
        start_menu()
    else:
        password = input("Enter your account password: ")
        cursor.execute("SELECT name, password, wallet, saldo, transactions, invested_money, withdrawal_money FROM users WHERE name=?", (name,))
        result = cursor.fetchone()
        connection.close()

        if result is not None and bcrypt.checkpw(password.encode(), result[1]):
            print("Login successful!")
            user = User(result[0], password, deposit=result[2])
            user.saldo = result[3]
            user.invested_money = result[5]
            user.withdrawal_money = result[6]
            
            user.wallet = json.loads(result[2])
            user.transactions = json.loads(result[4])
            
            return user
        else:
            print("Invalid username or password.")
            return login()

#USERS ACTIONS
def logged_in(user):
    user_choice = input("What do you want to do?\nPress 'M' to go to the market, 'A' to go to your account, or 'E' to exit: ")
    if user_choice.lower() == "m":
        market(user)
    elif user_choice.lower() == "a":
        moving_around_account(user)
    elif user_choice.lower() == "e":
        user.update_user_data()
        print("Thanks for visiting Hashira Exchange!\n Hope we'll see you soon!")
        sys.exit()


def logged_in(user):
    while True:
        print("Available options:")
        print("M: Go to the market")
        print("A: Go to your account")
        print("E: Exit")
        user_choice = input("What do you want to do? Enter your choice: ")

        if user_choice.lower() == "m":
            market(user)
            break
        elif user_choice.lower() == "a":
            moving_around_account(user)
            break
        elif user_choice.lower() == "e":
            user.update_user_data()
            print("Thanks for visiting Hashira Exchange!\nHope to see you again soon!")
            sys.exit()
        else:
            print("Invalid choice. Please try again.")

#MOVING AROUND ACCOUNT
def moving_around_account(user):
    while True:
        account_menu = input("Press 'W' to check your wallet, 'D' to make a deposit, 'P' to make a withdrawal, 'H' to check your transaction history, 'B' to check your balance, 'M' to go to the market, 'E' to exit\n")
        if account_menu.lower() == "w":
            user.check_wallet()
        elif account_menu.lower() == "d":
            amount = input("Specify the amount you wish to deposit: ")
            user.make_deposit(amount)
        elif account_menu.lower() == "p":
            amount = input("Specify the amount you wish to withdraw: ")
            user.make_withdrawal(amount)
        elif account_menu.lower() == "m":
            market(user)
        elif account_menu.lower() == "h":
            q = input("Do you want to see the history of purchases [p], sales [s], both [b], deposits [d], or withdrawals [w]? ")
            while q not in ["p", "s", "b", "d", "w"]:
                print("Oops, that isn't 'p', 's', 'b', 'd', or 'w'...")
                q = input("Press 'p' to view purchase history, 's' to view sales history, 'b' to view both, 'd' to view deposits, or 'w' for withdrawals: ")
            user.check_history(q)
        elif account_menu.lower() == "b":
            user.check_balance()
        elif account_menu.lower() == "e":
            user.update_user_data()
            print("Thanks for visiting Hashira Exchange!\nHope we'll see you soon!")
            sys.exit()


#MOVING AROUND MARKET
def market(user):
    while True:
        market_menu = input("What do you want to do? Enter 'B' to buy shares, 'S' to sell shares, 'C' to check shares, 'A' to go to your account, or 'E' to exit\n")
        if market_menu.lower() == "b":
            again = input("Would you like to see the shares and prices? Enter y/n: ")
            if again.lower() == "y":
                display_stocks(stocks_dict)
            buy_shares(user)
        elif market_menu.lower() == "s":
            user.update_wallet()
            again = input("Would you like to see your wallet? Enter y/n: ")
            if again.lower() == "y":
                user.check_wallet()
            sell_shares(user)
        elif market_menu.lower() == "c":
            check_share(user)
        elif market_menu.lower() == "a":
            moving_around_account(user)
        elif market_menu.lower() == "e":
            user.update_user_data()
            print("Thanks for visiting Hashira Exchange!\nHope we'll see you soon!")
            sys.exit()


#BUY SHARES
def buy_shares(user):
    print("Which shares would you like to buy and in what quantity?")
    shares_to_buy= input("Enter the symbol of the shares you wish to buy: ")
    while shares_to_buy not in stocks:
        shares_to_buy = input("Enter a valid symbol or 'X' to exit shopping: ")
        if shares_to_buy.lower() == "x":
            break
    if shares_to_buy.lower() != "x":
        amount_of_shares = input("Enter the number of shares you wish to buy: ")
        user.buy_shares(stocks[shares_to_buy], amount_of_shares)


#SELL SHARES
def sell_shares(user):
    preview = input("Would you like to see your wallet? Enter y/n: ")
    if preview.lower() == "y":
        user.check_wallet()
    print("Which shares would you like to sell and in what quantity?")
    shares_to_sell = input("Enter the symbol of the shares you wish to sell: ")
    while shares_to_sell not in stocks:
        shares_to_sell = input("Enter a valid symbol or 'X' to exit shopping: ")
        if shares_to_sell.lower() == "x":
            break
    if shares_to_sell.lower() != "x":
        amount_of_shares = input("Enter the number of shares you wish to sell: ")
        user.sell_shares(stocks[shares_to_sell], amount_of_shares)


#CHECK SHARES
def check_share(user):
    again = input("Would you like to see the shares and prices? Enter y/n: ")
    if again.lower() == "y":
        display_stocks(stocks_dict)
    shares_to_check = input("Enter the symbol of the action you wish to check: ")
    while shares_to_check not in stocks:
        shares_to_check = input("Enter a valid symbol or 'X' to exit checking: ")
        if shares_to_check.lower() == "x":
            break
    if shares_to_check.lower() != "x":
        c_stock = stocks[shares_to_check]
        c_stock.restore_state()
        print(c_stock)
        print()
        print("Purchasing ratio: " + str(c_stock.purchasing_ratio))
        print("Sales ratio: " + str(c_stock.sales_ratio))
        print(c_stock.generate_plot)
        print()
        next_step = input("Do you want to check other actions [press 'O'] or return to the menu ['press anything else']? ")
        if next_step.lower() == "o":
            check_share(user)


def courses_update(stocks_dict):
    for key, value in stocks_dict.items():
        stocks_dict[key]['price'] = stocks_dict[key]['price'] * uniform(0.9, 1.1)
    print("The prices on the exchange have been updated!")
    display_stocks(stocks_dict)
    for stock in stocks.values():
        stock.update_course()


def initialize_stocks():
    connection = sqlite3.connect('database.db')
    
    with connection:
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS stocks
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            short_name TEXT NOT NULL UNIQUE,
                            company_name TEXT NOT NULL UNIQUE,
                            current_price REAL,
                            cours_history TEXT,
                            transactions TEXT,
                            purchasing_amount REAL,
                            purchasing_quantity INTEGER,
                            sales_amount REAL,
                            sales_quantity INTEGER,
                            purchasing_ratio REAL,
                            sales_ratio REAL)''')
        for name in stocks_dict:
            stock = Stock(name)
            stock.restore_state()
            stocks[name] = stock

    connection.close()



stock_exchange()