# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/11/12 14:51
contact: jindaxiang@163.com
desc: 修大成主页-Risk Lab-Realized Volatility; Oxford-Man Institute of Quantitative Finance Realized Library
"""
import json

import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def article_oman_rv(symbol="FTSE", index="rk_th2", plot=True):
    """
    获取 Oxford-Man Institute of Quantitative Finance Realized Library 的数据
    :param symbol: str ['AEX', 'AORD', 'BFX', 'BSESN', 'BVLG', 'BVSP', 'DJI', 'FCHI', 'FTMIB', 'FTSE', 'GDAXI', 'GSPTSE', 'HSI', 'IBEX', 'IXIC', 'KS11', 'KSE', 'MXX', 'N225', 'NSEI', 'OMXC20', 'OMXHPI', 'OMXSPI', 'OSEAX', 'RUT', 'SMSI', 'SPX', 'SSEC', 'SSMI', 'STI', 'STOXX50E']
    :param index: str 指标 ['medrv', 'rk_twoscale', 'bv', 'rv10', 'rv5', 'rk_th2', 'rv10_ss', 'rsv', 'rv5_ss', 'bv_ss', 'rk_parzen', 'rsv_ss']
    :param plot: Bool 是否画图
    :return: pandas.DataFrame
    The Oxford-Man Institute's "realised library" contains daily non-parametric measures of how volatility financial assets or indexes were in the past. Each day's volatility measure depends solely on financial data from that day. They are driven by the use of the latest innovations in econometric modelling and theory to design them, while we draw our high frequency data from the Thomson Reuters DataScope Tick History database. Realised measures are not volatility forecasts. However, some researchers use these measures as an input into forecasting models. The aim of this line of research is to make financial markets more transparent by exposing how volatility changes through time.

    This Library is used as the basis of some of our own research, which effects its scope, and is made available here to encourage the more widespread exploitation of these methods. It is given 'as is' and solely for informational purposes, please read the disclaimer.

    The volatility data can be visually explored. We make the complete up-to-date dataset available for download. Lists of assets covered and realized measures available are also available.
    """
    url = "https://realized.oxford-man.ox.ac.uk/theme/js/visualization-data.js?20191111113154"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "lxml")
    soup_text = soup.find("p").get_text()
    data_json = json.loads(soup_text[soup_text.find("{"): soup_text.rfind("};")+1])
    date_list = data_json[f".{symbol}"]["dates"]
    title_fore = data_json[f".{symbol}"][index]["name"]
    title_last = data_json[f".{symbol}"][index]["measure"]
    title_list = title_fore + "-" + title_last
    temp_df = pd.DataFrame([date_list, data_json[f".{symbol}"][index]["data"]]).T
    temp_df.index = pd.to_datetime(temp_df.iloc[:, 0], unit='ms')
    temp_df = temp_df.iloc[:, 1]
    temp_df.index.name = "date"
    temp_df.name = f"{symbol}-{index}"
    if plot:
        temp_df.plot()
        plt.title(title_list)
        plt.legend()
        plt.show()
        return temp_df
    else:
        return temp_df


def article_oman_rv_short(symbol="FTSE", plot=True):
    """
    获取 Oxford-Man Institute of Quantitative Finance Realized Library 的数据
    :param symbol: str FTSE: FTSE 100, GDAXI: DAX, RUT: Russel 2000, SPX: S&P 500 Index, STOXX50E: EURO STOXX 50, SSEC: Shanghai Composite Index, N225: Nikkei 225
    :param plot: Bool 是否画图
    :return: pandas.DataFrame
    The Oxford-Man Institute's "realised library" contains daily non-parametric measures of how volatility financial assets or indexes were in the past. Each day's volatility measure depends solely on financial data from that day. They are driven by the use of the latest innovations in econometric modelling and theory to design them, while we draw our high frequency data from the Thomson Reuters DataScope Tick History database. Realised measures are not volatility forecasts. However, some researchers use these measures as an input into forecasting models. The aim of this line of research is to make financial markets more transparent by exposing how volatility changes through time.

    This Library is used as the basis of some of our own research, which effects its scope, and is made available here to encourage the more widespread exploitation of these methods. It is given 'as is' and solely for informational purposes, please read the disclaimer.

    The volatility data can be visually explored. We make the complete up-to-date dataset available for download. Lists of assets covered and realized measures available are also available.
    """
    url = "https://realized.oxford-man.ox.ac.uk/theme/js/front-page-chart.js"
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Host": "realized.oxford-man.ox.ac.uk",
        "Pragma": "no-cache",
        "Referer": "https://realized.oxford-man.ox.ac.uk/?from=groupmessage&isappinstalled=0",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"
    }

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "lxml")
    soup_text = soup.find("p").get_text()
    data_json = json.loads(soup_text[soup_text.find("{"): soup_text.rfind("}")+1])
    title_fore = data_json[f".{symbol}"]["name"]
    title_last = data_json[f".{symbol}"]["measure"]
    title_list = title_fore + "-" + title_last
    temp_df = pd.DataFrame(data_json[f".{symbol}"]["data"])
    temp_df.index = pd.to_datetime(temp_df.iloc[:, 0], unit='ms')
    temp_df = temp_df.iloc[:, 1]
    temp_df.index.name = "date"
    temp_df.name = f"{symbol}"
    if plot:
        temp_df.plot()
        plt.title(title_list)
        plt.legend()
        plt.show()
        return temp_df
    else:
        return temp_df


def article_rlab_rv(symbol="39693", plot=True):
    """
    获取修大成主页-Risk Lab-Realized Volatility
    :param symbol: str 股票代码
    :param plot: Bool 是否绘图
    :return: pandas.DataFrame
    1996-01-02    0.000000
    1996-01-04    0.000000
    1996-01-05    0.000000
    1996-01-09    0.000000
    1996-01-10    0.000000
                    ...
    2019-11-04    0.175107
    2019-11-05    0.185112
    2019-11-06    0.210373
    2019-11-07    0.240808
    2019-11-08    0.199549
    Name: RV, Length: 5810, dtype: float64


    Website:
    https://dachxiu.chicagobooth.edu/

    Objective
    We provide up-to-date daily annualized realized volatilities for individual stocks, ETFs, and future contracts, which are estimated from high-frequency data. We are in the process of incorporating equities from global markets.

    Data
    We collect trades at their highest frequencies available (up to every millisecond for US equities after 2007), and clean them using the prevalent national best bid and offer (NBBO) that are available up to every second. The mid-quotes are calculated based on the NBBOs, so their highest sampling frequencies are also up to every second.

    Methodology
    We provide quasi-maximum likelihood estimates of volatility (QMLE) based on moving-average models MA(q), using non-zero returns of transaction prices (or mid-quotes if available) sampled up to their highest frequency available, for days with at least 12 observations. We select the best model (q) using Akaike Information Criterion (AIC). For comparison, we report realized volatility (RV) estimates using 5-minute and 15-minute subsampled returns.

    References
    1. “When Moving-Average Models Meet High-Frequency Data: Uniform Inference on Volatility”, by Rui Da and Dacheng Xiu. 2017.
    2. “Quasi-Maximum Likelihood Estimation of Volatility with High Frequency Data”, by Dacheng Xiu. Journal of Econometrics, 159 (2010), 235-250.
    3. “How Often to Sample A Continuous-time Process in the Presence of Market Microstructure Noise”, by Yacine Aït-Sahalia, Per Mykland, and Lan Zhang. Review of Financial Studies, 18 (2005), 351–416.
    4. “The Distribution of Exchange Rate Volatility”, by Torben Andersen, Tim Bollerslev, Francis X. Diebold, and Paul Labys. Journal of the American Statistical Association, 96 (2001), 42-55.
    5. “Econometric Analysis of Realized Volatility and Its Use in Estimating Stochastic Volatility Models”, by Ole E Barndorff‐Nielsen and Neil Shephard. Journal of the Royal Statistical Society: Series B, 64 (2002), 253-280.

    """
    print("由于服务器在国外, 请稍后, 如果访问失败, 请使用代理工具")
    url = "https://dachxiu.chicagobooth.edu/data.php"
    payload = {"ticker": symbol}
    res = requests.get(url, params=payload, verify=False)
    soup = BeautifulSoup(res.text, "lxml")
    title_fore = pd.DataFrame(soup.find("p").get_text().split(symbol)).iloc[0, 0].strip()
    title_list = pd.DataFrame(soup.find("p").get_text().split(symbol)).iloc[1, 0].strip().split("\n")
    title_list.insert(0, title_fore)
    temp_df = pd.DataFrame(soup.find("p").get_text().split(symbol)).iloc[2:, :]
    temp_df = temp_df.iloc[:, 0].str.split(" ", expand=True)
    temp_df = temp_df.iloc[:, 1:]
    temp_df.iloc[:, -1] = temp_df.iloc[:, -1].str.replace(r"\n", "")
    temp_df.reset_index(inplace=True)
    temp_df.index = pd.to_datetime(temp_df.iloc[:, 1], format="%Y%m%d", errors="coerce")
    temp_df = temp_df.iloc[:, 1:]
    data_se = temp_df.iloc[:, 1]
    data_se.name = "RV"
    temp_df = data_se.astype("float", errors="ignore")
    temp_df.index.name = "date"
    if plot:
        temp_df.plot()
        plt.title("-".join(title_list))
        plt.legend()
        plt.show()
        return temp_df
    else:
        return temp_df


if __name__ == "__main__":
    df = article_rlab_rv(symbol="39693")
    print(df)
    help(article_rlab_rv)

    df = article_oman_rv_short(symbol="FTSE")
    print(df)
    help(article_rlab_rv)

    df = article_oman_rv(symbol="FTSE", index="rk_th2")
    print(df)
    help(article_rlab_rv)