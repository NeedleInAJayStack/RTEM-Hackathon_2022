import pandas
from onboard.client import RtemClient
from onboard.client.dataframes import points_df_from_streaming_timeseries
from onboard.client.models import PointSelector, TimeseriesQuery, PointData
from datetime import datetime, timezone
from dateutil.parser import isoparse
import os
from dotenv import load_dotenv

load_dotenv()
key = os.getenv('API_KEY')
api = RtemClient(api_key=key)

def readHistory(pointIDs, start=None, end=None):
  query = PointSelector()
  # query.point_types     = ['Electric Consumption'] # can list multiple point
  # query.equipment_types = ['meter', 'site', 'panel', 'virtual']              # types, equipment types,
  # query.buildings       = [275]       # buildings, etc.
  query.point_ids = pointIDs

  selection = api.select_points(query)

  points = api.get_points_by_ids(selection['points'])
  if points.count == 0:
    raise ValueError("No points found for time period")
  points_df = pandas.DataFrame.from_records(points)

  if start == None: 
    start = datetime.fromtimestamp(points_df["first_updated"].agg('min') / 1000, tz=timezone.utc) # provided timestamp is in milliseconds
  if end == None:
    end = datetime.fromtimestamp(points_df["last_updated"].agg('max') / 1000, tz=timezone.utc)
  # start = datetime.fromisoformat("2019-11-02T00:00:00+00:00")
  # end = start + timedelta(days=2)

  timeseries_query = TimeseriesQuery(point_ids = selection['points'], start = start, end = end)
  history = points_df_from_streaming_timeseries(api.stream_point_timeseries(timeseries_query))

  if history.size == 0:
    return history
    # raise ValueError("No histories found for time period")

  # Make index 'timestamp' in datetime format
  history['timestamp'] = [isoparse(i) for i in history['timestamp']]
  history = history.set_index('timestamp').astype(float).ffill()

  renameColMap = {}
  for point in points:
    renameColMap[point['id']] = f"{point['id']} - {point['description']}"
  history = history.rename(columns = renameColMap)

  return history

