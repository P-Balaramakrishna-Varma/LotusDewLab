from websocket import create_connection, WebSocketConnectionClosedException
import json
import ssl as ssl
import pandas as pd


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

tickers = nifty_50('niffty50.csv')
payload = create_payload(tickers)

# Subscribe Tickers on Websocket 
ws.send(json.dumps(payload))








#map : symbol--> cur
def get_current_prices():
    pass


#
def order(cur_prices, bye_sell):
    pass


money = 0

buy = get_current_prices()
money -= order(buy, 'B')


sell = get_current_prices()
money += order(sell, 'S')

print(money)