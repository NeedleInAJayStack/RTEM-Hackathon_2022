import pandas
from onboard.client import RtemClient
from onboard.client.dataframes import points_df_from_streaming_timeseries
from onboard.client.models import TimeseriesQuery
from datetime import datetime, timezone
from dateutil.parser import isoparse
import os
from dotenv import load_dotenv

load_dotenv()
key = os.getenv('API_KEY')
api = RtemClient(api_key=key)

def readHistory(pointIDs, start=None, end=None):
  """
  Returns a DataFrame containing historical values for the provided point IDs. The DataFrame has a correctly
  formatted datetime index named `timestamp`. If no start or end is provided, it uses the first or last value 
  from the provided points
  """
  points = api.get_points_by_ids(pointIDs)
  if points.count == 0:
    raise ValueError("No points found for time period")
  points_df = pandas.DataFrame.from_records(points)

  if start == None: 
    start = datetime.fromtimestamp(points_df["first_updated"].agg('min') / 1000, tz=timezone.utc) # provided timestamp is in milliseconds
  if end == None:
    end = datetime.fromtimestamp(points_df["last_updated"].agg('max') / 1000, tz=timezone.utc)

  timeseries_query = TimeseriesQuery(point_ids = pointIDs, start = start, end = end)
  history = points_df_from_streaming_timeseries(api.stream_point_timeseries(timeseries_query))

  if history.size == 0:
    return history

  # Make index 'timestamp' in datetime format
  history['timestamp'] = [isoparse(i) for i in history['timestamp']]
  history = history.set_index('timestamp').astype(float).ffill()

  renameColMap = {}
  for point in points:
    renameColMap[point['id']] = f"{point['id']} - {point['description']}"
  history = history.rename(columns = renameColMap)

  return history

