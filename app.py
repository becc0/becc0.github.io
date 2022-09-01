import os

from cs50 import sql

from flask import Flask, redirect, render_template
from flask_session import Session
import requests

# configure application
app = Flask(__name__)

# set api key and make sure exist
from dotenv import load_dotenv
load_dotenv()
#os.environ["API_KEY"]
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

# set session to filesystem and add time limit to session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

url = "https://api.coinranking.com/v2/coins/"

querystring = {"referenceCurrencyUuid":"yhjMzLPhuIDl","timePeriod":"24h","tiers[0]":"1","orderBy":"marketCap","orderDirection":"desc","limit":"1","offset":"0"}

headers = {
	"X-access-token": os.environ["API_KEY"]
}

response = requests.get(url, headers=headers, params=querystring)

quote = response.json()

data = []
coinqty=len(quote['data']["coins"])

for i in range(coinqty):
    data.append({
        "name":quote['data']["coins"][i]["name"],
        "symbol":quote['data']["coins"][i]["symbol"],
        "iconUrl":quote['data']["coins"][i]["iconUrl"],
        "price":quote['data']["coins"][i]["price"],
        "marketCap":quote['data']["coins"][i]["marketCap"],
        "rank":quote['data']["coins"][i]["rank"],
        "24hVolume":quote['data']["coins"][i]["24hVolume"],
        "coinrankingUrl":quote['data']["coins"][i]["coinrankingUrl"],
    })

#print(data)
#print(quote)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/coins")
def coins():
    return render_template("coins.html")
