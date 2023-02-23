import pandas as pd
from datetime import datetime, date, timedelta
from pytz import timezone
import os
import dotenv
import json
import certifi
from urllib.request import urlopen
from iso3166 import ISO3166
from iso3166 import DISCORD_FLAGS
import log

logger = log.setup_logger(__name__)

# What? You thought I would just hardcode the API Key?
dotenv.load_dotenv()
FMP_API = str(os.getenv("FMP_API"))


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


def stock_quote(symbol: str):
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
    appx = "?apikey=" + FMP_API
    url = base + symbol + appx
    quote = get_jsonparsed_data(url)
    return quote


def biz_metrics(symbol: str):
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
    appx = "?limit=40&apikey=" + FMP_API
    url = base + symbol + appx
    metrics = get_jsonparsed_data(url)
    return metrics


def profile(symbol: str):
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
    appx = "?apikey=" + FMP_API
    url = base + symbol + appx
    quote = get_jsonparsed_data(url)
    return quote


def get_econs(day: str):
    """
    Request economic calendar from FMP

    Parameters
    ----------
    day: str ["Yesterday","Today","Tomorrow"]

    Returns
    -------
    list[str]
    """
    today = date.today()
    yesterday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)
    dayafter = today + timedelta(days=2)

    if day == "Yesterday":
        url = f"https://financialmodelingprep.com/api/v3/economic_calendar?from={yesterday}&to={today}&apikey={FMP_API}"
    elif day == "Today":
        url = f"https://financialmodelingprep.com/api/v3/economic_calendar?from={today}&to={tomorrow}&apikey={FMP_API}"
    elif day == "Tomorrow":
        url = f"https://financialmodelingprep.com/api/v3/economic_calendar?from={tomorrow}&to={dayafter}&apikey={FMP_API}"

    dictos = get_jsonparsed_data(url)
    dictos.reverse()
    # logger.info(calendar)
    reports = []
    for dicto in dictos:
        report = ""
        if dicto["impact"] == "High":
            keysList = list(dicto.keys())
            for key in keysList:
                if dicto[key] is not None:
                    if key == "impact":
                        pass
                    else:
                        stringx = f"{key}: "
                        if key == "country":
                            try:
                                stringy = f"{DISCORD_FLAGS[dicto[key]]} {ISO3166[dicto[key]]}\n"
                            except KeyError:
                                stringy = f"{dicto[key]}\n"
                        elif key == "date":
                            date_format = datetime.strptime(
                                dicto[key], "%Y-%m-%d %H:%M:%S"
                            )
                            aware = timezone("UTC").localize(date_format)
                            unix_time = int(round(datetime.timestamp(aware)))
                            stringy = f"<t:{unix_time}>\n"
                        elif key == "event":
                            stringy = f"**__{dicto[key]}__**\n"
                        else:
                            stringy = f"{dicto[key]}\n"
                        report = report + stringx + stringy
                else:
                    pass
            report = report + "\n"
            reports.append(report)

    if not reports:
        return ["No high-impact economics on this day.", "Try again tomorrow."]
    else:
        return reports


def get_13f_firms(name: str):
    fixstr = name.replace(" ", "%20")
    url = (
        f"https://financialmodelingprep.com/api/v3/cik-search/{fixstr}?apikey={FMP_API}"
    )
    namelist = get_jsonparsed_data(url)
    return namelist


def get_cik_name(cik: str):
    url = f"https://financialmodelingprep.com/api/v3/cik/{cik}?apikey={FMP_API}"
    data = get_jsonparsed_data(url)
    name = data[0]["name"]
    return name


def get_13f_dates(cik: str):
    url = f"https://financialmodelingprep.com/api/v3/form-thirteen-date/{cik}?apikey={FMP_API}"
    file_dates = get_jsonparsed_data(url)
    logger.info(file_dates)
    return file_dates


def get_13f_latest(cik: str, date: str):
    url = f"https://financialmodelingprep.com/api/v3/form-thirteen/{cik}?date={date}&apikey={FMP_API}"
    thirteen = get_jsonparsed_data(url)
    logger.info(thirteen)
    df13 = pd.DataFrame.from_dict(thirteen)
    total_port = df13["value"].sum()
    df13["percent"] = df13["value"] / total_port * 100
    df13["mark"] = df13["value"] / df13["shares"]
    df13sort = df13.sort_values(by=["value"], ascending=False)
    return df13sort
