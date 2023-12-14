from websocket import create_connection, WebSocketConnectionClosedException
import json, logging
import pandas as pd
import ssl as ssl
# from websocket_connect import get_api_key



# logging
def setup_logger(log_file):
    """ Set up the logger configuration. """
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(message)s')

def log_json_record(record):
    """ Log a JSON record to the specified log file. """
    logger = logging.getLogger()
    json_record = json.dumps(record)
    logger.info(json_record)

log_file = 'stock_values1.log'
setup_logger(log_file)


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



while True:
  data = json.loads(ws.recv())
  log_json_record(data)
  print(data)