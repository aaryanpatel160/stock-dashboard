import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
from stocknews import StockNews

# Title of the Dashboard
st.title('Stock Dashboard')

# Sidebar Inputs
ticker = st.sidebar.text_input('Ticker')
tickerData = yf.Ticker(ticker)
start_date = st.sidebar.date_input('Start Date')
end_date = st.sidebar.date_input('End Date')

# Validate if the ticker and dates are provided correctly
if ticker and start_date and end_date:
    try:
        # Download the stock data
        data = yf.download(ticker, start=start_date, end=end_date)

        # Check if data is returned
        if not data.empty:
            # Plotting the adjusted close price
            fig = px.line(data, x=data.index, y='Adj Close', title=ticker)
            st.plotly_chart(fig)

            # Tabs for different types of data
            pricing_data, fundamental_data, news = st.tabs(['Pricing Data', 'Fundamental Data', 'Top 10 News'])

            with pricing_data:
                st.header('Price Movements')
                data2 = data.copy()
                data2['% Change'] = data['Adj Close'] / data['Adj Close'].shift(1) - 1
                data2.dropna(inplace=True)

                if not data2.empty:
                    st.write(data2)
                    annual_return = data2['% Change'].mean() * 252 * 100
                    st.write('Annual Return is ', annual_return, '%')
                    stdev = np.std(data2['% Change']) * np.sqrt(252)
                    st.write('Standard Deviation is ', stdev * 100, '%')
                    st.write('Risk Adj. Return is ', annual_return / (stdev * 100))
                else:
                    st.warning("Not enough data to calculate price movements.")

            with fundamental_data:
                st.header('Fundamental Data')
                try:
                    st.write('Forward Earnings Per Share (EPS): ', tickerData.info.get('forwardEps', 'N/A'))
                    st.write('Trailing Earnings Per Share (EPS): ', tickerData.info.get('trailingEps', 'N/A'))
                    st.write('Forward Price-to-Earnings Ratio (P/E Ratio): ', tickerData.info.get('forwardPE', 'N/A'))
                    st.write('Trailing Price-to-Earnings Ratio (P/E Ratio): ', tickerData.info.get('trailingPE', 'N/A'))
                    st.write('Total Revenue: ', tickerData.info.get('totalRevenue', 'N/A'))
                    st.write('Revenue Growth: ', tickerData.info.get('revenueGrowth', 'N/A'))
                    st.write('Revenue per Share (RPS): ', tickerData.info.get('revenuePerShare', 'N/A'))
                    st.write('Net Profit Margin: ', tickerData.info.get('profitMargins', 'N/A'))
                    st.write('Return on Assets (ROA): ', tickerData.info.get('returnOnAssets', 'N/A'))
                    st.write('Return on Equity (ROE): ', tickerData.info.get('returnOnEquity', 'N/A'))
                    st.write('Price-to-Book Ratio (P/B Ratio): ', tickerData.info.get('priceToBook', 'N/A'))
                    st.write('Enterprise Value (EV) / EBITDA: ', tickerData.info.get('ebitda', 'N/A'))
                    st.write('Debt-to-Equity Ratio: ', tickerData.info.get('debtToEquity', 'N/A'))
                    st.write('Earnings Quarterly Growth Rate: ', tickerData.info.get('earningsQuarterlyGrowth', 'N/A'))
                    st.write('Dividend Yield: ', tickerData.info.get('dividendYield', 'N/A'))
                    st.write('Price-to-Sales Ratio (P/S Ratio): ', tickerData.info.get('priceToSalesTrailing12Months', 'N/A'))
                    st.write('Free Cash Flow (FCF): ', tickerData.info.get('freeCashflow', 'N/A'))
                    st.write('Operating Cash Flow (OCF): ', tickerData.info.get('operatingCashflow', 'N/A'))
                    st.subheader('Balance Sheet')
                    st.write(tickerData.balance_sheet)
                except Exception as e:
                    st.error(f"An error occurred while fetching fundamental data: {e}")

            with news:
                st.header(f'News of {ticker}')
                sn = StockNews(ticker, save_news=False)
                df_news = sn.read_rss()
                
                if not df_news.empty:
                    for i in range(min(10, len(df_news))):
                        st.subheader(f'News {i+1}')
                        st.write(df_news['published'][i])
                        st.write(df_news['title'][i])
                        st.write(df_news['summary'][i])
                        title_sentiment = df_news['sentiment_title'][i]
                        st.write(f'Title Sentiment: {title_sentiment}')
                        news_sentiment = df_news['sentiment_summary'][i]
                        st.write(f'News Sentiment: {news_sentiment}')
                else:
                    st.warning("No news available for this ticker.")
        else:
            st.warning("No data found for the selected ticker and date range. Please try again with different parameters.")
    except Exception as e:
        st.error(f"An error occurred while fetching the data: {e}")
else:
    st.info("Please enter a ticker symbol and select a date range.")
