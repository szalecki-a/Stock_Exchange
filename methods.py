from random import uniform
from stocks import stocks_dict, display_stocks
from clases import User, stocks, user_names

def courses_update(stocks_dict):
    for key, value in stocks_dict.items():
        stocks_dict[key]['price'] = stocks_dict[key]['price'] * uniform(0.9, 1.1)
    print("The prices on the exchange have been updated!")
    display_stocks(stocks_dict)
    for stock in stocks.values():
        stock.update_course()

#GREETING
def greet():
  print("Welcome to the Hashira Exchange")
  print("This project allows you to simulate stock market actions.")


#ACCOUNT CREATING
def create_account():
    name = input("Set your account name: ")
    if name not in user_names and name != "":
        user = User(name)
    else:
        name2 = input("This username is already in use. Please enter a different username: ")
        return create_account(name2)
    if user is not None:
        print("Account created successfully!")
        print("Account name:", user.name)
    else:
        print("Account creation failed.")
    return user

#MENU
def start_menu(user):
    q1 = input("What do you want to do? \nPress 'M' to go on market, press 'A' to go on your account, press 'E' to exit\n")
    if q1.lower() == "m":
        market(user)
    elif q1.lower() == "a":
        moving_around_account(user)
    elif q1.lower() == "e":
        print("Thanks for visiting Hashira Exchange!\n Hope we'll see you soon!")



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
            print("Thanks for visiting Hashira Exchange!\nHope we'll see you soon!")
            break


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
            print("Thanks for visiting Hashira Exchange!\nHope we'll see you soon!")
            break


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
        user.buy_shares(stocks[q1], amount_of_shares)


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
        if qshares_to_check.lower() == "x":
            break
    if shares_to_check.lower() != "x":
        c_stock = stocks[shares_to_check]
        print(c_stock)
        print()
        print("Purchasing ratio: " + str(c_stock.purchasing_ratio))
        print("Sales ratio: " + str(c_stock.sales_ratio))
        print(c_stock.generate_plot)
        print()
        next_step = input("Do you want to check other actions [press 'O'] or return to the menu ['press anything else']? ")
        if next_step.lower() == "o":
            check_share(user)