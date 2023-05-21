greet = '''Hello! Welcome to the stock market game simulator.

This project allows you to simulate stock market actions. Here are the features available in this simulator:

1. Displaying stock information:
   The `display_stocks` function shows the available stocks along with their symbols and current prices.

2. Buying and selling stocks:
   The `buy_stock` function allows you to buy stocks by providing the stock symbol and quantity you want to purchase.
   The `sell_stock` function enables you to sell stocks from your portfolio by specifying the stock symbol and quantity to sell.

3. Calculating portfolio value:
   The `calculate_portfolio_value` function computes the value of your portfolio based on the stocks you own and their current prices.

4. Displaying profits and losses:
   The `calculate_profit_loss` function calculates the profits and losses by comparing the current portfolio value with the cost of acquiring the stocks.

5. Plotting stock price changes:
   The `plot_stock_prices` function generates a chart showing the changes in stock prices over time using a plotting library such as matplotlib.

6. Transaction history:
   The `display_transaction_history` function keeps track of your transaction history and allows you to view it on demand.

7. Simple investment indicators:
   The project includes several basic investment indicators, such as the average purchase price of stocks or the percentage change in portfolio value.

8. Simple investment strategies:
   The project implements a few simple investment strategies, such as "buy when the price drops" or "sell when the price rises." You can receive recommendations based on these strategies.

9. User interaction:
   The simulator provides a simple user interface in the terminal, allowing you to perform operations, view information, and browse transaction history.

10. Error handling and exceptions:
    The project is designed to handle errors and exceptions, such as providing an invalid stock symbol or attempting to sell more stocks than you have in your portfolio.

I hope you have a great time exploring the stock market simulator!
'''

print(greet)