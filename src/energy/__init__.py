from collections import namedtuple
import pandas
import math
from datetime import datetime, timezone
from sklearn.cluster import KMeans

def normalize(input: pandas.DataFrame, toFreq: str):
  """
  Given a dataframe representing historical energy usage, this cleans it in the following ways:
  1. It adjusts the input dataframe to the specified time interval
  2. It fills gaps correctly by apportioning subsequent read values over previous intervals
  3. If data is aggregated, it disaggregates and removes rollover events
  
  It is able to handle multi-column dataframes.
  """

  history = input

  start = history.index.min()
  end = history.index.max()

  for column in list(history.columns):
    # Diff the values to determine if we should disaggregate. Disaggregate needed if >90% of points have a positive differential
    avgIncreasingValues = history[column].diff().map(lambda x: 0 if x < 0 else 1).mean()
    if avgIncreasingValues > 0.9:
      newRows = []

      prevTime = history.index.min()
      prevVal = float("nan")
      prevValDiff = float("nan")
      prevTimeDiff = float("nan")
      cumSum = float("nan")

      # Sum the values. If a rollover is observed, just apply an NaN and start a new aggregation calc.
      # This is because we don't know when in the interval the rollover occurred.
      for index in history[column].index:
        val = history[column][index]
        timeDiff = index - prevTime
        if not math.isnan(prevVal):
          if val < prevVal:
            # If it goes down, just use the previous diff because we could have an incomplete value.
            # Scale the previous diff by the length of time that covered, and extend it to this time diff (inconsistent timestamps during rollovers were observed)
            # Don't set prevValDiff here, just reuse the previous one
            cumSum = cumSum + (prevValDiff / prevTimeDiff.total_seconds()) * timeDiff.total_seconds()
          else:
            valDiff = val - prevVal
            if math.isnan(cumSum):
              cumSum = valDiff
            else:
              cumSum = cumSum + valDiff
            prevValDiff = valDiff
            prevTimeDiff = timeDiff
        prevVal = val
        prevTime = index

        row = {"ts": index, column: cumSum}
        newRows.append(row)
      newHis = pandas.DataFrame.from_records(newRows, index="ts")
      history[column] = newHis[column]
    else:
      history[column] = history[column].cumsum()

  # Fill any NA gaps in the original dataset
  history = history.interpolate(method="time")

  # Interpolate time intervals to expected values. Reindex to include exact frequency intervals, interpolate, and then remove extraneous in-between values.
  normalizedIndex = pandas.date_range(start=start, end=end, freq=toFreq, tz=timezone.utc)
  history = history.reindex(history.index.union(normalizedIndex)).interpolate(method='time').reindex(normalizedIndex)

  # Diff the result to get to aggregate usage for each period
  history = history.diff()

  return history

def removeOutliers(input: pandas.DataFrame, maxIqrsFromMean: float):
  """
  This removes outliers based on the input maximum distance from mean in terms of Inter-Quartile Ranges.
  It also removes any values that are zero or smaller.
  All removed values are set to NaN
  """
  
  history = input

  # Filter values way outside the norm (>10 z-score)
  for column in list(history.columns):
    series = history[column]
    iqr = series.quantile(0.75) - series.quantile(0.25)
    median = series.median()
    history[column] = series.map(lambda x: float("nan") if x<=0 or abs((x - median)/iqr) > maxIqrsFromMean else x)

  return history

def clusterAnalyze(input: pandas.DataFrame):
  """
  Performs a 2-node cluster analysis on the input dataframe. It returns a named tuple that
  includes the following:
  - clusterHistory: Dataframe. This is the input history with the cluster values applied as a column named "cluster"
  - kpiHistory: DataFrame. This is a historical representation of weekly KPIs with the following columns:
     - date: The start date of the week over which the KPIs were computed
     - low_usage: The low-use cluster value
     - high_usage: The high-use cluster value
     - unoccupied_turndown_factor: The high-use cluster value divided by the low use. 
        This indicates how effective the unoccupied energy reduction strategies are. Scaled from 0 to 1.
     - occupied_duration_factor: The duration that the building was in a high-use state. 
        This measures how often unoccupied energy reduction strategies are used. Scaled from 0 to 1.
  """

  history = input
  groupKpis = []
  groupHistories = []

  # for date, groupHistory in history.groupby(lambda ts: ts.date()): # Slice by day
  for date, groupHistory in history.groupby( # Slice by week
    lambda ts: datetime.fromisocalendar(ts.isocalendar().year, ts.isocalendar().week, 1).astimezone(tz=timezone.utc)
  ):
    if groupHistory.size < 2:
      continue

    # 2-center k-means clustering
    kmeans = KMeans(n_clusters = 2, random_state = 0)
    clusters = kmeans.fit_predict(groupHistory)
    centers = kmeans.cluster_centers_

    # Compute unoccupied_turndown_factor
    maxCenter = max(centers)[0]
    minCenter = min(centers)[0]

    low = minCenter
    high = maxCenter
    if maxCenter != 0:
      unoccupied_turndown_factor = minCenter / maxCenter
    else:
      unoccupied_turndown_factor = float("nan")

    # Create KPI history
    kmeanValues = [centers[x][0] for x in clusters]
    groupHistory["cluster"] = kmeanValues

    # Compute high-energy duration
    highDuration = pandas.Timedelta(seconds=0)
    lowDuration = pandas.Timedelta(seconds=0)
    prevTs = date
    for ts in groupHistory.index:
      val = groupHistory["cluster"][ts]
      timeDelta = ts - prevTs
      if val == maxCenter:
        highDuration = highDuration + timeDelta
      else:
        lowDuration = lowDuration + timeDelta
      prevTs = ts
    occupied_duration_factor = highDuration.total_seconds() / (highDuration.total_seconds() + lowDuration.total_seconds())

    # Create KPIs record
    groupKpi = {
      "date": date,
      "low_usage": low,
      "high_usage": high,
      "unoccupied_turndown_factor": unoccupied_turndown_factor,
      "occupied_duration_factor": occupied_duration_factor
    }
    groupKpis.append(groupKpi)
    groupHistories.append(groupHistory)

  kpiHistory = pandas.DataFrame.from_records(groupKpis, index="date")
  clusterHistory = pandas.concat(groupHistories)

  ClusterResult = namedtuple('ClusterResult', ['kpiHistory', 'clusterHistory'])
  return ClusterResult(kpiHistory, clusterHistory)
