from datetime import datetime
from random import uniform
import matplotlib.pyplot as plt
from stocks import stocks_dict
stocks = {}
user_names = []

def display_stocks(stocks_dict):
    print("Available stocks:")
    for key, value in stocks_dict.items():
        print(f"Company Name: {value['company_name']}")
        print(f"Symbol: {key} | Price: {value['price']}")
        print()

class User:
    def __init__(self, name):
        self.name = name
        self.wallet = {}
        self.saldo = 0
        self.transactions = []
        self.invested_money = 0
        self.withdrawal_money = 0

    def caltuale_saldo(self):
        self.saldo = 0
        for stock_symbol, number_of_shares in self.wallet.items():
            self.saldo += number_of_shares * stocks_dict[stock_symbol]["price"]
    
    def update_wallet(self):
        to_del = []
        for stock_symbol, number_of_shares in self.wallet.items():
            if number_of_shares == 0:
                to_del.append(stock_symbol)
        for stock_to_del in to_del:
            self.wallet.pop(stock_to_del)
    
    def buy_shares(self, stock, number_of_shares):
        self.transactions.append([datetime.now(), stock.short_name, int(number_of_shares), int(number_of_shares) * stocks_dict[stock.short_name]["price"], "P"])
        self.wallet[stock.short_name] = self.wallet.get(stock.short_name, 0) + int(number_of_shares)
        self.invested_money += int(number_of_shares) * stocks_dict[stock.short_name]["price"]
        self.caltuale_saldo()
        stock.purchased(int(number_of_shares), stocks_dict[stock.short_name]["price"])
        print("You bought {} shares of company {} at {} price".format(int(number_of_shares), stocks_dict[stock.short_name]['company_name'], stocks_dict[stock.short_name]['price']))

    def sell_shares(self, stock, number_of_shares):
        if stock.short_name not in self.wallet or self.wallet[stock.short_name] == 0:
            print("You cannot sell shares you do not own")
        elif int(number_of_shares) > self.wallet[stock.short_name]:
            print("You do not have enough shares.")
        else:
            self.transactions.append([datetime.now(), stock.short_name, int(number_of_shares), int(number_of_shares) * stocks_dict[stock.short_name]["price"], "S"])
            self.wallet[stock.short_name] = self.wallet.get(stock.short_name) - int(number_of_shares)
            self.withdrawal_money += int(number_of_shares) * stocks_dict[stock.short_name]["price"]
            self.caltuale_saldo()
            stock.sold(int(number_of_shares), stocks_dict[stock.short_name]["price"])
            print("You sold {} shares in the company {} at {} price".format(int(number_of_shares), stocks_dict[stock.short_name]['company_name'], stocks_dict[stock.short_name]['price']))

    def check_wallet(self):
        self.caltuale_saldo()
        number_of_shares = len(self.wallet)
        if number_of_shares == 0:
            print("You do not currently hold any shares")
        else:
            print(f"You currently own shares in {number_of_shares} companies:")
            for stock_symbol, number_of_shares in self.wallet.items():
                print(f"Company Name: {stocks_dict[stock_symbol]['company_name']} ({stock_symbol})")
                print(f"number of shares: {number_of_shares} | value: {stocks_dict[stock_symbol]['price'] * number_of_shares}")
                print()
            print(f"The total value of your shares is ${self.saldo}.")
    
    def check_history(self, symbol):
        if len(self.transactions) == 0:
            print("Your transactions history is empty\n")
        elif symbol == "p":
            print("Your purchase history:")
            for transaction in self.transactions:
                if transaction[4] == "P":
                    print(f"{transaction[0]}    Company: {transaction[1]}   Number of shares: {transaction[2]} for the sum of ${transaction[3]}")
            print(f"In total, you have invested ${self.invested_money} in shares")
        elif symbol == "s":
            print("Your sales history:")
            for transaction in self.transactions:
                if transaction[4] == "S":
                    print(f"{transaction[0]}    Company: {transaction[1]}   Number of shares: {transaction[2]} for the sum of ${transaction[3]}")
            print(f"In total, you have paid out ${self.withdrawal_money} in shares")
        else:
            print("Your transactions history:")
            for transaction in self.transactions:
                if transaction[4] == "P":
                    print(f"PURCHASE: {transaction[0]}    Company: {transaction[1]}   Number of shares: {transaction[2]} for the sum of ${transaction[3]}")
                else:
                    print(f"SALES: {transaction[0]}    Company: {transaction[1]}   Number of shares: {transaction[2]} for the sum of ${transaction[3]}")
            print(f"In total, you have invested ${self.invested_money} and paid out ${self.withdrawal_money} in shares")
    
    def check_balance(self):
        self.caltuale_saldo()
        if self.invested_money > self.withdrawal_money + self.saldo:
            print(f"Your current balance is ${self.saldo} in shares.")
            print(f"In total, you have lost ${self.invested_money - self.withdrawal_money - self.saldo} on the tranzactions.")
        elif self.invested_money < self.withdrawal_money + self.saldo:
            print(f"Your current balance is ${self.saldo} in shares.")
            print(f"In total, you have earned ${self.invested_money - self.withdrawal_money - self.saldo} on the tranzactions!")
        else:
            print(f"Your current balance is ${self.saldo} in shares.")
            print(f"In total, you have a balance of zero on the tranzactions.")


class Stock:
    def __init__(self, name):
        self.short_name = name
        self.company_name = stocks_dict[name]['company_name']
        self.current_price = stocks_dict[name]['price']
        self.cours_history = [[datetime.now(), self.current_price]]
        stocks[self.short_name] = self
        self.transactions = []
        self.purchasing_amount = [self.current_price, 1]
        self.sales_amount = [self.current_price, 1]
        self.purchasing_ratio = self.purchasing_amount[0] / self.purchasing_amount[1]
        self.sales_ratio = self.sales_amount[0] / self.sales_amount[1]

    def __repr__(self):
        return "Company {} ({}) shares. The current price is ${}.".format(self.company_name, self.short_name, self.current_price)
    
    def update_course(self):
        self.current_price = stocks_dict[self.short_name]['price']
        self.cours_history.append([datetime.now(), self.current_price])

    def purchased(self, amount, price):
        self.transactions.append([amount, price, "P"])
        self.purchasing_amount[0] += amount * price
        self.purchasing_amount[1] += amount

    def sold(self, amount, price):
        self.transactions.append([amount, price, "S"])
        self.sales_amount[0] += amount * price
        self.sales_amount[1] += amount

    def generate_plot(self):
    # Separation of dates and prices from cours_history
        dates = [entry[0] for entry in self.cours_history]
        prices = [entry[1] for entry in self.cours_history]
        # Generation of a graph
        plt.plot(dates, prices)
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.title(f'{self.company_name} share chart')
        plt.xticks(rotation=45)
        plt.show()


def courses_update(stocks_dict):
    for key, value in stocks_dict.items():
        stocks_dict[key]['price'] = stocks_dict[key]['price'] * uniform(0.9, 1.1)
    print("The prices on the exchange have been updated!")
    display_stocks(stocks_dict)
    for stock in stocks.values():
        stock.update_course()


def greet():
  print("Welcome to the Hashira Exchange")
  print("This project allows you to simulate stock market actions.")

def create_account(name):
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



def moving_around_account(user):
    user.update_wallet()
    a1 = input("Press 'W' to check your wallet, 'M' to go on market, 'H' to check your transaction history, 'B' to check your balance, 'E' to exit\n")
    if a1.lower() == "w":
        user.check_wallet()
        print("\n")
    elif a1.lower() == "m":
        market(user)
    elif a1.lower() == "h":
        q = input("Do you want to see purchase [p] history, sales [s] history or both [b]?")
        while q not in ["p", "s", "b"]:
            print("Oops, that isn't 'p', 's', or 'b'...")
            q = input("Press 'p' to view purchase history, 's' to view sales history or 'b' to view all transactions.")
        user.check_history(q)
    elif a1.lower() == "b":
        user.check_balance()
        print("\n")
    elif a1.lower() == "e":
        print("Thanks for visiting Hashira Exchange!\n Hope we'll see you soon!")
        return
    return moving_around_account(user)
    

def stock_exchange():
    greet()
    name = input("Set your account name: ")
    user = create_account(name)
    q1 = input("What do you want to do? \nPress 'M' to go on market, press 'A' to go on your account, press 'E' to exit\n")
    if q1.lower() == "m":
        market(user)
    elif q1.lower() == "a":
        moving_around_account(user)
    elif q1.lower() == "e":
        print("Thanks for visiting Hashira Exchange!\n Hope we'll see you soon!")
        return

AAPL = Stock("AAPL")
GOOG = Stock("GOOG")
TSLA = Stock("TSLA")
MSFT = Stock("MSFT")
AMZN = Stock("AMZN")
FB = Stock("FB")
JPM = Stock("JPM")
JNJ = Stock("JNJ")
V = Stock("V")
PG = Stock("PG")
WMT = Stock("WMT")
BAC = Stock("BAC")
MA = Stock("MA")
KO = Stock("KO")
DIS = Stock("DIS")
VZ = Stock("VZ")
CSCO = Stock("CSCO")
INTC = Stock("INTC")
NFLX = Stock("NFLX")
IBM = Stock("IBM")

#courses_update(stocks_dict)


stock_exchange()
