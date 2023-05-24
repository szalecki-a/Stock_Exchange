import bcrypt
import sqlite3
import json
from datetime import datetime
import matplotlib.pyplot as plt
from stocks import stocks_dict
stocks = {}
users = {}

class User:
    def __init__(self, name, password, deposit=10000):
        self.name = name
        self.password = self._hash_password(password)
        self.wallet = {"USD": deposit}
        self.saldo = 0
        self.transactions = [[datetime.now().isoformat(), "USD", deposit, deposit, "D"]]
        self.invested_money = deposit
        self.withdrawal_money = 0
        self.update_user_data()
        users[self.name] = self
    
    def _hash_password(self, password):
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        return hashed_password

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode(), self.password)


    def calculate_saldo(self):
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
        self.update_wallet()
        self.calculate_saldo()
        number_of_shares = int(number_of_shares)
        stock_info = stocks_dict[stock.short_name]
        
        total_cost = number_of_shares * stock_info["price"]
        if total_cost > self.wallet["USD"]:
            print("You don't have enough money to buy that many shares")
        else:
            timestamp = datetime.now().isoformat()
            self.transactions.append([timestamp, stock.short_name, number_of_shares, total_cost, "P"])
            self.wallet[stock.short_name] = self.wallet.get(stock.short_name, 0) + number_of_shares
            self.wallet["USD"] -= total_cost
            stock.purchased(number_of_shares, stock_info["price"])
            message = f"You bought {number_of_shares} shares of company {stock_info['company_name']} at {stock_info['price']} price"
            print(message)


    def sell_shares(self, stock, number_of_shares):
        self.update_wallet()
        self.calculate_saldo()
        number_of_shares = int(number_of_shares)
        stock_info = stocks_dict[stock.short_name]

        if stock.short_name not in self.wallet or self.wallet[stock.short_name] == 0:
            print("You cannot sell shares you do not own")
        elif number_of_shares > self.wallet[stock.short_name]:
            print("You do not have enough shares.")
        else:
            timestamp = datetime.now().isoformat()
            selling_price = number_of_shares * stock_info["price"]
            self.transactions.append([timestamp, stock.short_name, number_of_shares, selling_price, "S"])
            self.wallet[stock.short_name] = self.wallet.get(stock.short_name, 0) - number_of_shares
            self.wallet["USD"] += selling_price
            stock.sold(number_of_shares, stock_info["price"])

            message = f"You sold {number_of_shares} shares in the company {stock_info['company_name']} at {stock_info['price']} price"
            print(message)


    def check_wallet(self):
        self.update_wallet()
        self.calculate_saldo()
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
                    print(f"The total value of your wallet is ${self.saldo}.")


    def make_deposit(self, amount):
        amount = int(amount)
        self.wallet["USD"] += (amount)
        self.invested_money += amount
        self.transactions.append([datetime.now().isoformat(), "USD", amount, amount, "D"])
        print(f"You have deposited ${amount} into your account")
    

    def make_withdrawal(self, amount):
        self.update_wallet()
        amount = int(amount)
        if  self.wallet["USD"] < amount:
            print(f"You cannot withdraw more money from your wallet than you have (${self.wallet['USD']})")
        else:
            self.wallet["USD"] -= amount
            self.withdrawal_money += amount
            self.transactions.append([datetime.now().isoformat(), "USD", amount, amount, "W"])
            print(f"You have withdrawn ${amount} from your account")
    

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
        self.calculate_saldo()
        balance = self.invested_money - self.withdrawal_money - self.saldo
        print(f"The value of your portfolio is ${self.saldo}.")
        if balance < 0:
            print(f"In total, you have lost ${balance} on the tranzactions (Money deposited: {self.invested_money}, Money paid out: {self.withdrawal_money}), Value of portfolio: {self.saldo}.")
        elif balance > 0:
            print(f"In total, you have earned ${balance} on the tranzactions! (Money deposited: {self.invested_money}, Money paid out: {self.withdrawal_money}), Value of portfolio: {self.saldo}.")
        else:
            print(f"In total, you have a balance of zero on the tranzactions (Money deposited: {self.invested_money}, Money paid out: {self.withdrawal_money}, Value of portfolio: {self.saldo}).")


    def update_user_data(self):
        transactions_json = json.dumps(self.transactions)
        wallet_json = json.dumps(self.wallet)

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        user_data = (self.name, self.password, wallet_json, self.saldo,
                     transactions_json, self.invested_money, self.withdrawal_money)
        cursor.execute('UPDATE users SET password=?, wallet=?, saldo=?, transactions=?, invested_money=?, withdrawal_money=? WHERE name=?', user_data)
        connection.commit()
        connection.close()


class Stock:
    def __init__(self, name):
        self.short_name = name
        self.company_name = stocks_dict[name]['company_name']
        self.current_price = stocks_dict[name]['price']
        self.cours_history = [[datetime.now().isoformat(), self.current_price]]
        self.transactions = []
        self.purchasing_amount = [self.current_price, 1]
        self.sales_amount = [self.current_price, 1]
        self.purchasing_ratio = self.purchasing_amount[0] / self.purchasing_amount[1]
        self.sales_ratio = self.sales_amount[0] / self.sales_amount[1]

        self.connection = sqlite3.connect('database.db')
        self.restore_state()

        stocks[self.short_name] = self

    def __repr__(self):
        return "Company {} ({}) shares. The current price is ${}.".format(self.company_name, self.short_name, self.current_price)
    
    def restore_state(self):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM stocks WHERE short_name=?', (self.short_name,))
            stock_data = cursor.fetchone()

            if stock_data:
                transactions = json.loads(stock_data[5])
                cours_history = [[datetime.fromisoformat(entry[0]), entry[1]] for entry in json.loads(stock_data[4])]

                self.current_price = stock_data[3]
                self.cours_history = cours_history
                self.transactions = transactions
                self.purchasing_amount = [stock_data[6], stock_data[7]]
                self.sales_amount = [stock_data[8], stock_data[9]]
                self.purchasing_ratio = stock_data[10]
                self.sales_ratio = stock_data[11]

    def save_state(self):
        cours_history_json = json.dumps(self.cours_history)
        transactions_json = json.dumps(self.transactions)

        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute('INSERT OR REPLACE INTO stocks (short_name, company_name, current_price, cours_history, transactions, purchasing_amount, purchasing_quantity, sales_amount, sales_quantity, purchasing_ratio, sales_ratio) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                           (self.short_name, self.company_name, self.current_price, cours_history_json, transactions_json, self.purchasing_amount[0], self.purchasing_amount[1], self.sales_amount[0], self.sales_amount[1], self.purchasing_ratio, self.sales_ratio))

    def update_course(self):
        self.current_price = stocks_dict[self.short_name]['price']
        self.cours_history.append([datetime.now().isoformat(), self.current_price])

        cours_history_json = json.dumps(self.cours_history)

        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute('UPDATE stocks SET cours_history=? WHERE short_name=?',
                           (cours_history_json, self.short_name))

    def purchased(self, amount, price):
        self.transactions.append([amount, price, "P"])
        self.purchasing_amount[0] += amount * price
        self.purchasing_amount[1] += amount

        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute('UPDATE stocks SET purchasing_amount=?, purchasing_quantity=? WHERE short_name=?',
                           (self.purchasing_amount[0], self.purchasing_amount[1], self.short_name))

    def sold(self, amount, price):
        self.transactions.append([amount, price, "S"])
        self.sales_amount[0] += amount * price
        self.sales_amount[1] += amount

        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute('UPDATE stocks SET sales_amount=?, sales_quantity=? WHERE short_name=?',
                           (self.sales_amount[0], self.sales_amount[1], self.short_name))

    def generate_plot(self):
        dates = [entry[0] for entry in self.cours_history]
        prices = [entry[1] for entry in self.cours_history]

        plt.plot(dates, prices)
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.title(f'{self.company_name} share chart')
        plt.xticks(rotation=45)
        plt.show()