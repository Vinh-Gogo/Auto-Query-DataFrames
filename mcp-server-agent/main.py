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
    "arstechnica": "https://arstechnica.com" # đọc thông tin từ web site
}

@mcp.tool() # example tool
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
        except httpx.RequestError as e:
            return f"Request error: {e}"

@mcp.tool()        
async def read_data_csv(file_path: str):
    """Reads a CSV file and returns the data as a pandas DataFrame."""
    try:
        data = pd.read_csv(file_path, encoding='utf-8').reset_index(drop=True)
        return data
    except FileNotFoundError:
        return "File not found"

@mcp.tool()
async def get_walls_data(df: pd.DataFrame, column_name: str = 'category'):
    """Returns the data of the walls in the database."""
    category_column = [col for col in df.columns if column_name.lower() in col.lower()]

    walls = [wall for wall in df[category_column[0]] if 'revit walls' in wall.lower()]
    return walls


@mcp.tool()
async def get_all_keys():
    """
    Fetches all the keys in the data.

    Returns:
    A list of all the keys in the data.
    [dbId, external_id, ElementId, Name, Category, CategoryId, Family Name, Workset, Outdoor Air per Area, Air Changes per Hour, Outdoor Air Method, Heating Set Point, Latent Heat Gain per person, Humidification Set Point, Cooling Set Point, Export to IFC, Specified Lighting Load per area, Specified Power Load per area, Infiltration Airflow per area, Plenum Lighting Contribution, Occupancy Schedule, Lighting Schedule, Power Schedule, Outdoor Air per Person, Dehumidification Set Point, Area per Person, Sensible Heat Gain per person, IfcGUID, Cost, Color, Description, Glow, Shininess, Smoothness, Transparency, Behavior, Class]
    """
    file_path = "data.csv"
    df = await read_data_csv(file_path)
    return df.columns.tolist()

@mcp.tool()
async def classification_value_in_column(column: str):
    """
    Fetches the unique values in the specified column.

    Args:
    column (str): The name of the column to fetch unique values from.
    Returns:
    A list of unique values in the specified column.
    """
    file_path = "data.csv"
    df = await read_data_csv(file_path)
    
    if column not in df.columns:
        return f"Column '{column}' not found in the data."
    unique_values = df[column].unique()
    return unique_values.tolist()

@mcp.tool()
async def get_walls_data_from_csv():
    """
    Fetches the walls data from the CSV file.

    Returns:
    A list of walls data.
    """
    file_path = "data.csv"
    df = await read_data_csv(file_path)
    walls = await get_walls_data(df, column_name='Category')
    if not walls:
        return "No walls found in the data."
    # Convert the list of walls to a DataFrame
    return walls

@mcp.tool() # đang bị lỗi
async def search_different_components_in_columns(column_name='Category', component_name='Revit Walls'):
    """
    Searches for different components in the specified column.
    Args:
    column_name (str): The name of the column to search in.
    component_name (str): The name of the component to search for.
    Returns:
    A list of unique components found in the specified column.
    """
   
    file_path = "data.csv"
    df = await read_data_csv(file_path)
    wall_columns = [column_name]

    # Initialize a counter for walls
    wall_count = 0

    # # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        # Check if any of the wall columns contain the word 'wall'
        if any(word in str(row[column]).lower() for column in wall_columns for word in [component_name]):
            wall_count += 1
    return wall_count

if __name__ == "__main__":
    mcp.run(transport="stdio")