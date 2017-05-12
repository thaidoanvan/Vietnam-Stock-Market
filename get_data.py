
import urllib.request
import xml.etree.ElementTree as ET
from lxml import etree
import pandas as pd
import datetime


def xml2df(xml_data):
    tree = ET.parse(xml_data)
    root = tree.getroot()
    all_records = []
    headers = []
    for i, child in enumerate(root):
        record = []
        for subchild in child:
            record.append(subchild.text)
            if subchild.tag not in headers:
                headers.append(subchild.tag)
        all_records.append(record)
    return pd.DataFrame(all_records, columns=headers)

def get_data(stock, timeFrom):
    tdate = pd.to_datetime(datetime.datetime.today())
    fdate = pd.to_datetime(timeFrom, dayfirst = True)
    url = "http://finance.vietstock.vn/Controls/TradingResult/Matching_Hose_Result.aspx?scode={}&lcol=TKLGD%2CTGTGD%2CVHTT%2CGD3%2CTGG%2CTGPTG%2CBQM%2CBQB%2CKLGDKL%2CGTGDKL%2C&sort=Time&dir=desc&page=1&psize=0&fdate={}%2F{}%2F{}&tdate={}%2F{}%2F{}&exp=xml".format(stock, fdate.month, fdate.day, fdate.year%100, tdate.month, tdate.day, tdate.year%100)
    data = urllib.request.urlretrieve(url)[0]
    data = xml2df(data)
    return data
