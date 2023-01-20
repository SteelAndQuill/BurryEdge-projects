import pandas as pd
from datetime import datetime
import os
import dotenv
import json
import certifi
from urllib.request import urlopen

# What? You thought I would just hardcode the API Key?
dotenv.load_dotenv()
API = str(os.getenv("FMP_API"))

def get_jsonparsed_data(url):
    """
    Receive the content of ``url``, parse it as JSON and return the object.

    Parameters
    ----------
    url : str

    Returns
    -------
    dict
    """
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")
    return json.loads(data)

def stock_quote(symbol:str):
    """
    Request stock quote from FMP

    Parameters
    ----------
    symbol : str

    Returns
    -------
    list[dict]
    """
    base = "https://financialmodelingprep.com/api/v3/quote/"
    appx = "?apikey=" + API
    url = base + symbol + appx
    quote = get_jsonparsed_data(url)
    return quote

def biz_metrics(symbol:str):
    """
    Request TTM metrics from FMP

    Parameters
    ----------
    symbol : str

    Returns
    -------
    list[dict]
    """
    base = "https://financialmodelingprep.com/api/v3/key-metrics-ttm/"
    appx = "?limit=40&apikey=" + API
    url = base + symbol + appx
    metrics = get_jsonparsed_data(url)
    return metrics

def profile(symbol:str):
    """
    Request company profile from FMP

    Parameters
    ----------
    symbol : str

    Returns
    -------
    list[dict]
    """
    base = "https://financialmodelingprep.com/api/v3/profile/"
    appx = "?apikey=" + API
    url = base + symbol + appx
    quote = get_jsonparsed_data(url)
    return quote
