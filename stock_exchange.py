from clases import Stock, stocks, user_names
from methods import courses_update, greet, start_menu, create_account


def stock_exchange():
    greet()
    user = create_account()
    start_menu(user)

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


stock_exchange()