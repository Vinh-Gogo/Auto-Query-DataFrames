from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import httpx
import os
from bs4 import BeautifulSoup
import json
import pandas as pd
import numpy as np

# os.environ["ANTHROPIC_API_KEY"] = ""
# load_dotenv()

mcp = FastMCP("revit_query")
USER_AGENT = "news-app/1.0"

NEWS_SITES = {
    "arstechnica": "https://arstechnica.com"
}

async def read_data_csv(file_path: str):
    """Reads a CSV file and returns the data as a pandas DataFrame."""
    try:
        data = pd.read_csv(file_path, encoding='utf-8').reset_index(drop=True)
        return data
    except FileNotFoundError:
        return "File not found"

async def get_walls_data(df: pd.DataFrame):
    """Returns the data of the walls in the database."""
    category_column = [col for col in df.columns if 'category' in col.lower()]

    walls = [wall for wall in df[category_column[0]] if 'revit walls' in wall.lower()]
    return walls

@mcp.tool()
async def fetch_news(url: str):
    """It pulls and summarizes the latest news from the specified news site."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=30.0)
            soup = BeautifulSoup(response.text, "html.parser")
            paragraphs = soup.find_all("p")
            text = " ".join([p.get_text() for p in paragraphs[:5]]) 
            return text
        except httpx.TimeoutException:
            return "Timeout error"

@mcp.tool()
async def get_all_keys():
    """
    Fetches all the keys in the data.

    Returns:
    A list of all the keys in the data.
    """
    file_path = "data.csv"
    df = await read_data_csv(file_path)
    return df.columns.tolist()

@mcp.tool()
async def get_walls_count():
    """
    Fetches the number of Revit walls in the database.

    Returns:
    The number of Revit walls in the database.
    """
    file_path = "data.csv"
    df = await read_data_csv(file_path)
    wall_columns = ['Category']

    # Initialize a counter for walls
    wall_count = 0

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        # Check if any of the wall columns contain the word 'wall'
        if any(word in str(row[column]).lower() for column in wall_columns for word in ['wall', 'walls']):
            wall_count += 1
    return wall_count

if __name__ == "__main__":
    mcp.run(transport="stdio")
