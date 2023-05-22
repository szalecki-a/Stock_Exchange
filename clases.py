from datetime import datetime
import matplotlib.pyplot as plt
from stocks import stocks_dict
stocks = {}
user_names = []

class User:
    def __init__(self, name, deposit=10000):
        self.name = name
        self.wallet = {"USD": deposit}
        self.saldo = 0
        self.transactions = [[datetime.now(), "USD", deposit, deposit, "D"]]
        self.invested_money = deposit
        self.withdrawal_money = 0
        user_names.append(self)

    def caltuale_saldo(self):
        self.saldo = 0
        for stock_symbol, number_of_shares in self.wallet.items():
            if stock_symbol != "USD":
                self.saldo += number_of_shares * stocks_dict[stock_symbol]["price"]
        self.saldo += self.wallet["USD"]
    
    def update_wallet(self):
        to_del = [stock_symbol for stock_symbol, number_of_shares in self.wallet.items()
                if number_of_shares == 0 and stock_symbol != "USD"]
        for stock_to_del in to_del:
            self.wallet.pop(stock_to_del, None)

    
    def buy_shares(self, stock, number_of_shares):
        number_of_shares = int(number_of_shares)
        stock_info = stocks_dict[stock.short_name]
        
        total_cost = number_of_shares * stock_info["price"]
        if total_cost > self.wallet["USD"]:
            print("You don't have enough money to buy that many shares")
        else:
            timestamp = datetime.now()
            self.transactions.append([timestamp, stock.short_name, number_of_shares, total_cost, "P"])
            self.wallet[stock.short_name] = self.wallet.get(stock.short_name, 0) + number_of_shares
            self.wallet["USD"] -= total_cost
            stock.purchased(number_of_shares, stock_info["price"])
            message = f"You bought {number_of_shares} shares of company {stock_info['company_name']} at {stock_info['price']} price"
            print(message)


    def sell_shares(self, stock, number_of_shares):
        number_of_shares = int(number_of_shares)
        stock_info = stocks_dict[stock.short_name]

        if stock.short_name not in self.wallet or self.wallet[stock.short_name] == 0:
            print("You cannot sell shares you do not own")
        elif number_of_shares > self.wallet[stock.short_name]:
            print("You do not have enough shares.")
        else:
            timestamp = datetime.now()
            selling_price = number_of_shares * stock_info["price"]
            self.transactions.append([timestamp, stock.short_name, number_of_shares, selling_price, "S"])
            self.wallet[stock.short_name] = self.wallet.get(stock.short_name, 0) - number_of_shares
            self.wallet["USD"] += selling_price
            stock.sold(number_of_shares, stock_info["price"])

            message = f"You sold {number_of_shares} shares in the company {stock_info['company_name']} at {stock_info['price']} price"
            print(message)


    def check_wallet(self):
        self.caltuale_saldo()
        self.update_wallet()
        number_of_shares = len(self.wallet) - 1 # Substract 1 to exclude "USD" from the count
        if number_of_shares == 0:
            print(f"You have ${self.wallet['USD']} in your portfolio and no shares.")
        else:
            print(f"In your portfolio you have ${self.wallet['USD']} and shares in {number_of_shares} companies:")
            for stock_symbol, number_of_shares in self.wallet.items():
                if stock_symbol != "USD":
                    stock_info = stocks_dict[stock_symbol]
                    company_name = stock_info['company_name']
                    stock_price = stock_info['price']
                    stock_value = stock_price * number_of_shares
                    print(f"Company Name: {company_name} ({stock_symbol})")
                    print(f"Number of shares: {number_of_shares} | Value: {stock_value}")
                    print()
                    print(f"The total value of your wallet is ${self.saldo}.")
    

    def check_history(self, symbol):
        if symbol == "p":
            value_of_purchases = 0
            print("Your purchase history:")
            for transaction in self.transactions:
                if transaction[4] == "P":
                    date, stock_symbol, num_shares, total_cost, _ = transaction
                    value_of_purchases += total_cost
                    print(f"{date}    Company: {stock_symbol}   Number of shares: {num_shares} for the sum of ${total_cost}")
            print(f"The total value of purchases is: {value_of_purchases}")
        
        elif symbol == "s":
            value_of_sales = 0
            print("Your sales history:")
            for transaction in self.transactions:
                if transaction[4] == "S":
                    date, stock_symbol, num_shares, total_cost, _ = transaction
                    value_of_sales += total_cost
                    print(f"{date}    Company: {stock_symbol}   Number of shares: {num_shares} for the sum of ${total_cost}")
            print(f"The total value of sales is: {value_of_sales}")
        
        elif symbol == "b":
            value_of_purchases = 0
            value_of_sales = 0
            print("Your transactions history:")
            for transaction in self.transactions:
                date, stock_symbol, num_shares, total_cost, trans_type = transaction
                if trans_type == "P":
                    value_of_purchases += total_cost
                    print(f"PURCHASE: {date}    Company: {stock_symbol}   Number of shares: {num_shares} for the sum of ${total_cost}")
                elif trans_type == "S":
                    value_of_sales += total_cost
                    print(f"SALES: {date}    Company: {stock_symbol}   Number of shares: {num_shares} for the sum of ${total_cost}")
            print(f"The total value of purchases is: {value_of_purchases} and the total value of sales is: {value_of_sales}")

        elif symbol == "d":
            print("Your deposits history:")
            for transaction in self.transactions:
                if transaction[4] == "D":
                    date, _, deposit, _, _ = transaction
                    print(f"DEPOSIT: {date}    USD: {deposit}")
            print(f"You have paid a total of ${self.invested_money} into your account.")

        elif symbol == "w":
            print("Your withdrawals history:")
            for transaction in self.transactions:
                if transaction[4] == "W":
                    date, _, withdrawal, _, _ = transaction
                    print(f"WITHDRAWAL: {date}    USD: -{withdrawal}")
            print(f"You have withdrawn a total of ${self.withdrawal_money} from your account.")
    
    
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
