# Simple Crypto coins Exchange Server 

## 📖 Introduction 

This is an example of a Service that converts a specific amount of cryptocurrencies into US Dollars in automated fashion I wrote to use FastAPI. 
The service uses the [coingecko API](https://www.coingecko.com/en/api/documentation) to fetch the current value in US Dollars of each cryptocurrency.
This service exposes a web Server that satisfies the following:

-  The endpoint `/exchange`  is reachable via a HTTP GET request
-  This endpoint should take two URL parameters (e.g. `/exchange?coin=btc&amount=10`):
  - `coin`: The coin to exchange. The only valid inputs supported are: "btc", "eth", "xrp". Any combination of upper/lower case characters.
  - `amount`: The amount to exchange into dollars. The only valid input should be a decimal number above 0 but below 10000 
- The endpoint  makes a HTTP GET request to CoinGecko.com to obtain an up-to-date exchange rate for the desired `coin`. 
 

- The HTTP server should respond with a JSON Response in the format of: `{"usd_amount": 12342}`. 
The exchange rates frequently fluctuate, and the API has a limit on the number of requests it can handle. 
Therefore, it is crucial to avoid making multiple requests to the same API for each query. Data is cached for a minimum of 2 minutes before being updated. 
A simple cache is used but its implementation is open to be changed.

- For any malformed input or other errors, return a JSON string response with a useful message in an `error` field. Example: `{"error": "Invalid Amount."}`


### Supported Crypto Coins and how to add new ones.

By default, the services is configured to support 3 crypto coins , bitcoin, ripple and ethereum and to return their
prices in USD.
Each supported coin is configured as a dict , `{"symbol":{"id": "coin id", "name": "coin official name"}`
For example:

```
{"btc": {"id": "bitcoin", "name": "Bitcoin"}
```

The supported coins are specified in the `.env` file in `SUPPORTED_COINS`. To add a new coin, builds a new dict and
append it.
For example,

```
{ "ada":{"id": "cardano","name": "Cardano"}
```

### 💵 Currency 

By default, prices will be provided in USD. IF you want to change it, edit the `DEFAULT_CURRENCY` in the `.env` and
replace `usd` with `eur` for example. 
The response format  will be also change to reflect the selected currency.
The maximum amount to request is limited by a value set in `MAX_AMOUNT`. Change it if you want to increase or decrease the upperbound.


### ⚙️ Cache System 

The service comes with a Cache to limit the number of request. The default `TTL` is 180 seconds. To change it, edit the `CACHE_TTL_IN_SECS` value in the `.env`


# 🚀 How to run 

- RUN `poetry install` to install the dependencies
- RUN ` uvicorn app.main:app` to run the API server that will listen to the default port `8000`. If you want to customize the port use `--port number of port`

# 🔎 How to run tests 
- RUN `poetry install` to install the dependencies
- RUN `./run_test.sh`

# 🏗️ How to build and run a Docker container 
- RUN `docker build -t crypto-exchange .`
- RUN `docker run --name crypto-exchange -p 8000:8000 crypto-exchange`

# 🚧 ToDo 

1. Validate the `SUPPORTED_COINS` format 
2. Support more than one currency at the same time