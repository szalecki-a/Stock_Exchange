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
        return


#MOVING AROUND ACCOUNT
def moving_around_account(user):
    user.update_wallet()
    a1 = input("Press 'W' to check your wallet, 'M' to go on market, 'H' to check your transaction history, 'B' to check your balance, 'E' to exit\n")
    if a1.lower() == "w":
        user.check_wallet()
        print("\n")
    elif a1.lower() == "m":
        market(user)
    elif a1.lower() == "h":
        q = input("Do you want to see the history of purchases [p], sales [s], both [b], deposits [d] or withdrawals [w]?")
        while q not in ["p", "s", "b", "d", "w"]:
            print("Oops, that isn't 'p', 's', or 'b'...")
            q = input("Press 'p' to view purchase history, 's' to view sales history or 'b' to view both, 'd' to view depostis or 'w' for withdrawals.")
        user.check_history(q)
        return moving_around_account(user)
    elif a1.lower() == "b":
        user.check_balance()
        print("\n")
        return moving_around_account(user)
    elif a1.lower() == "e":
        print("Thanks for visiting Hashira Exchange!\n Hope we'll see you soon!")
        return


#MOVING AROUND MARKET
def market(user):
    q = input("What do you want to do? Enter 'B' to buy shares, 'S' to sell shares, 'C' to check shares, 'A' to check your account or press 'E' to exit\n")
    if q.lower() == "b":
        again = input("Would you like to see the shares and prices? Enter y/n: ")
        if again.lower() == "y":
            display_stocks(stocks_dict)
        print()
        buy_shares(user)
        print()
        market(user)
    elif q.lower() == "s":
        user.update_wallet()
        again = input("Would you like to see the shares and prices? Enter y/n: ")
        if again.lower() == "y":
            display_stocks(stocks_dict)
        print()
        sell_shares(user)
        print()
        market(user)
    elif q.lower() == "c":
        check_share(user)
    elif q.lower() == "a":
        moving_around_account(user)
    elif q.lower() == "e":
        print("Thanks for visiting Hashira Exchange!\n Hope we'll see you soon!")
        return
    else:
      market(user)


#BUY SHARES
def buy_shares(user):
    print("Which shares would you like to buy and in what quantity?")
    q1 = input("Enter the symbol of the shares you wish to buy\n")
    while q1 not in stocks:
        q1 = input("Enter a valid symbol or 'X' to exit shopping\n")
        if q1.lower() == "x":
            market(user)
            break
    q2 = input("Enter the number of shares you wish to buy:\n")
    user.buy_shares(stocks[q1], q2)


#SELL SHARES
def sell_shares(user):
    preview = input("Would you like to see your wallet? Enter y/n: ")
    if preview.lower() == "y":
        user.check_wallet()
    print("Which shares would you like to sell and in what quantity?")
    q1 = input("Enter the symbol of the shares you wish to sell\n")
    while q1 not in stocks:
        q1 = input("Enter a valid symbol or 'X' to exit shopping\n")
        if q1.lower() == "x":
            market(user)
            break
    q2 = input("Enter the number of shares you wish to sell:\n")
    user.sell_shares(stocks[q1], q2)

#CHECK SHARES
def check_share(user):
    again = input("Would you like to see the shares and prices? Enter y/n: ")
    if again.lower() == "y":
        display_stocks(stocks_dict)
    q1 = input("Enter the symbol of the action you wish to check.\n")
    while q1 not in stocks:
        q1 = input("Enter a valid symbol or 'X' to exit checking")
        if q1.lower() == "x":
            market(user)
            break
    c_stock = stocks[q1]
    print(c_stock)
    print()
    print("Purchasing ratio: " + str(c_stock.purchasing_ratio))
    print("Sales ratio: " + str(c_stock.sales_ratio))
    print(c_stock.generate_plot)
    print()
    q2 = input("Do you want to check other actions [press 'O'] or return to the menu ['press anything else']?")
    if q2.lower() == "o":
        check_share(user)
    market(user)