from bs4 import BeautifulSoup
from .common import URLFetch, ParseTables
import datetime

months = ["Unknown",
          "January",
          "Febuary",
          "March",
          "April",
          "May",
          "June",
          "July",
          "August",
          "September",
          "October",
          "November",
          "December"]

headers = {'Accept': '*/*',
           'Accept-Encoding': 'gzip, deflate, sdch, br',
           'Accept-Language': 'en-GB,en-US;q=0.8,en;q=0.6',
           'Connection': 'keep-alive',
           'Host': 'www1.nseindia.com',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
           'X-Requested-With': 'XMLHttpRequest'}

option_chain_url = URLFetch(url='https://www1.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?segmentLink=17&symbol=%s&instrument=%s&date=%s', headers=headers)
option_chain_referer = "https://www1.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?symbolCode=-9999&symbol=NIFTY&symbol=BANKNIFTY&instrument=OPTIDX&date=-&segmentLink=17&segmentLink=17"
OPTIONS_CHAIN_SCHEMA = [str, int, int, int, float, float, float, int, float, float, int, float,int, float, float, int, float, float, float, int, int, int, str]
OPTIONS_CHAIN_HEADERS = ["Call Chart", "Call OI", "Call Chng in OI", "Call Volume", "Call IV", "Call LTP", "Call Net Chng", "Call Bid Qty", "Call Bid Price", "Call Ask Price", "Call Ask Qty","Strike Price","Put Bid Qty", "Put Bid Price", "Put Ask Price", "Put Ask Qty", "Put Net Chng", "Put LTP", "Put IV", "Put Volume", "Put Chng in OI", "Put OI", "Put Chart"]
OPTIONS_CHAIN_INDEX = "Strike Price"

def get_option_chain(symbol, instrument=None, expiry=None):

    if expiry:
        expiry_str = "%02d%s%d" % (
            expiry.day, months[expiry.month][0:3].upper(), expiry.year)
    else:
        expiry_str = "-"
    option_chain_url.session.headers.update({'Referer': option_chain_referer})
    r = option_chain_url(symbol, instrument, expiry_str)

    return r


def get_option_chain_table(symbol, instrument=None, expiry=None):
    optchainscrape = get_option_chain(symbol, instrument, expiry)
    html_soup = BeautifulSoup(optchainscrape.text, 'html.parser')
    abc = html_soup.find("table")
    abc = abc.findAll("div")[1]    
    index_val = float(abc.find("b").text.replace("NIFTY ", ""))  
    abc = abc.findAll("span")[1].text
    abc = abc.replace("As on ", "")
    index_datetime = abc.replace(" IST", "")    
    index_datetime = index_datetime.replace(",", "")
    index_datetime = index_datetime.replace(" ", "").upper()
    index_datetime = datetime.datetime.strptime(index_datetime,"%b%m%Y%H:%M:%S")    
    sptable = html_soup.find("table", {"id": "octable"})
    tp = ParseTables(soup=sptable,
                     schema=OPTIONS_CHAIN_SCHEMA,
                     headers=OPTIONS_CHAIN_HEADERS, index=OPTIONS_CHAIN_INDEX)
    temp = tp.get_df()        
    return temp, index_val, index_datetime
