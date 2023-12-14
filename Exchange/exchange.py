from websocket import create_connection, WebSocketConnectionClosedException
import json
import ssl as ssl
import pandas as pd
import time

# Check and Establish connection with websocket
ws = create_connection("wss://api.airalgo.com/socket/websocket", sslopt={"cert_reqs": ssl.CERT_NONE})

# Payload to authenticate with the websocket
conn = {
    "topic" : "api:join",
    "event" : "phx_join",
    "payload" :
        {
            "phone_no" : "8712318802" #"1234567890"
        },
    "ref" : ""
    }
# Authenticate with websocket
ws.send(json.dumps(conn))
print(ws.recv())

# Create Payload to subscribe Equity ltp 
# {"topic" : "api:join", "event" : "ltp_quote", "payload" : ["ACC", "ABB", "ADANIENT"], "ref" : ""}
def create_payload(tickers):
    payload = {
      "topic" : "api:join",
      "event" : "ltp_quote", 
      "payload" : tickers,
      "ref" : ""
      }
    return payload

def nifty_50(file_path):
  df = pd.read_csv(file_path)
  symbols = df['Symbol'].tolist()
  return symbols

tickers = nifty_50('../DataCollection/niffty50.csv')
payload = create_payload(tickers)

# Subscribe Tickers on Websocket 
ws.send(json.dumps(payload))








#map : symbol--> cur
def get_current_prices(ws):
    prices = {}
    for _ in range(100):
        # print("reading")
        data = json.loads(ws.recv())
        prices[data['payload'][0]['symbol']] = data['payload'][2]
    return prices


#ordering code
def create_playload(symbol, buy_sell, price, quantity):
    order = {
     "topic" : "api:join", 
     "event" : "order", 
     "payload" : {
        "phone_no" : "8712318802", 
        "symbol" : symbol, 
        "buy_sell" : buy_sell, 
        "quantity" : quantity, 
        "price" : price
        }, 
      "ref" : ""
      }
    return order

def order(recommondations, cur_prices, bye_sell, ws):
    cost = 0
    for recom in recommondations:
        if recom not in cur_prices:
            continue
        pay = create_playload(recom, bye_sell, cur_prices[recom], 1)
        ws.send(json.dumps(pay))
        if bye_sell == 'B':
            cost -= cur_prices[recom]
        else:
            cost += cur_prices[recom]
        print(cost)
    return cost





if __name__ == '__main__':
    recommondations = ['ASIANPAINT', 'LT', 'LTIM', 'DRREDDY', 'BAJFINANCE', 'INDUSINDBK', 'ULTRACEMCO', 'TCS', 'BAJAJFINSV', 'GRASIM', 'HEROMOTOCO', 'SBILIFE', 'APOLLOHOSP', 'TITAN', 'BRITANNIA', 'EICHERMOT', 'MARUTI', 'BAJAJ-AUTO', 'NESTLEIND', 'ADANIENT', 'DIVISLAB']
    money = 0

    buy = get_current_prices(ws)
    print(buy)
    money -= order(recommondations, buy, 'B', ws)

    time.sleep(3)

    sell = get_current_prices(ws)
    print(sell)
    money += order(recommondations, sell, 'S', ws)

    print(money)