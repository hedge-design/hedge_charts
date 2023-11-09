import os
from datetime import datetime, timedelta

import plotly.graph_objs as go
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Mapping from string to Alpaca TimeFrame
TIMEFRAME_MAPPING = {
    "1Min": TimeFrame.Minute,
    # "5Min": TimeFrame.FiveMinutes,
    # "15Min": TimeFrame.FifteenMinutes,
    "1D": TimeFrame.Day,
    # "1W": TimeFrame.Week,
    # Add more mappings if needed
}


# Function to create a Plotly figure for the stock chart
def generate_stock_chart(
    stock_symbol: str,
    days: int = 90,
    timeframe_str: str = "1D",
    dark_mode: bool = True,
    candlestick: bool = False,
    show_after_hours: bool = False,
):
    # Convert the string timeframe to a TimeFrame object
    timeframe = TIMEFRAME_MAPPING.get(timeframe_str, TimeFrame.Day)

    # Instantiate the Alpaca historical data client
    alpaca_client = StockHistoricalDataClient(
        api_key=os.getenv("ALPACA_KEY"),
        secret_key=os.getenv("ALPACA_SECRET"),
        raw_data=False,
    )

    # Define the time period for the stock data
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    # Create a request for historical stock data
    request_params = StockBarsRequest(
        symbol_or_symbols=stock_symbol,
        timeframe=timeframe,
        start=start_date.isoformat(),
        end=end_date.isoformat(),
    )

    # Fetch the historical stock data
    bars = alpaca_client.get_stock_bars(request_params)
    # Extract the data for plotting
    df = bars.df
    df = df.reset_index(level="symbol", drop=True)
    # Create a Plotly graph object

    # fig = go.Figure(data=[go.Scatter(x=df.index, y=df.close)])
    if candlestick:
        fig = go.Figure(
            data=[
                go.Candlestick(
                    x=df.index, open=df.open, high=df.high, low=df.low, close=df.close
                )
            ]
        )
    else:
        fig = go.Figure(data=[go.Scatter(x=df.index, y=df.close)])

    if not show_after_hours:
        fig.update_xaxes(
            rangebreaks=[
                dict(bounds=["sat", "mon"]),  # hide weekends
                dict(
                    bounds=[16, 9.5], pattern="hour"
                ),  # hide hours outside of 9.5am-4pm
            ]
        )

    last_price = df.close[-1].round(2)
    fig.update_layout(
        title=f"{stock_symbol} ${last_price}",  # Set the title
        # yaxis_title="Price (USD)",
        xaxis=dict(
            fixedrange=True,
            rangeslider=dict(visible=False),  # This disables the rangeslider
            # title="Date",
            type="date",  # Ensure the x-axis is treated as a date
        ),
        yaxis=dict(
            fixedrange=True,
        ),
    )
    if dark_mode:
        fig.update_layout(template="plotly_dark")

    return fig


# Function to save the Plotly figure as a PNG file
def generate_stock_chart_png(
    stock_symbol: str, days: int = 90, timeframe_str: str = "1D"
):
    # Generate the stock chart figure
    fig = generate_stock_chart(stock_symbol, days, timeframe_str)

    # Save the figure as a PNG file
    png_filename = f"{stock_symbol}_chart_{timeframe_str}_{days}.png"
    png_filename = "/tmp/" + png_filename
    fig.write_image(png_filename)

    return png_filename


# Example usage:
# generate_stock_chart_png('AAPL', 90, '1D')
