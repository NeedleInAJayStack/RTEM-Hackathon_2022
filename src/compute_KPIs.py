import pandas
from api import readHistory
from energy import normalize, removeOutliers, clusterAnalyze
from buildingPoints import buildingIds, pointsForBuilding

def computeBuildingKPIs(buildingId: int):
  # QUERY
  pointIds = pointsForBuilding(buildingId)
  history = readHistory(pointIds)

  if history.size == 0:
    return {
      "building_id": buildingId
    }

  # CLEAN
  history = normalize(history, toFreq="15min")
  history = removeOutliers(history, maxIqrsFromMean=10)

  # Sum columns & name result 'energy'
  history = pandas.DataFrame(history.sum(axis=1, min_count=1), columns=['energy']).dropna()

  # ANALYZE
  clusterResult = clusterAnalyze(history)
  kpiHistory = clusterResult.kpiHistory
  clusterHistory = clusterResult.clusterHistory

  kpiValues = kpiHistory.mean()
  return {
    "building_id": buildingId,
    "start_date": kpiHistory.index.min(),
    "end_date": kpiHistory.index.max(),
    "low_cluster_avg": kpiValues["low_usage"],
    "high_cluster_avg": kpiValues["high_usage"],
    "unoccupied_turndown_factor_avg": kpiValues["unoccupied_turndown_factor"],
    "occupied_duration_factor_avg": kpiValues["occupied_duration_factor"],
  }

kpiRows = []
index = 0
for buildingId in buildingIds:
  # Record progress
  print(f"{index/buildingIds.size*100}% - Building: {buildingId}")

  kpiRow = computeBuildingKPIs(buildingId)
  kpiRows.append(kpiRow)
  index = index + 1

kpis = pandas.DataFrame.from_records(kpiRows)
kpis.to_csv("data/kpis.csv")