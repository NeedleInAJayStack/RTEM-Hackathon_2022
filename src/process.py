import pandas
from api import readHistory
from energy import normalize, removeOutliers, clusterAnalyze
from buildingPoints import buildingIds, pointsForBuilding

def processBuilding(buildingId: int):
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
    "startDate": kpiHistory.index.min(),
    "endDate": kpiHistory.index.max(),
    "lowUsage": kpiValues["lowUsage"],
    "highUsage": kpiValues["highUsage"],
    "turndown": kpiValues["turndown"],
    "highUsageTimeFactor": kpiValues["highUsageTimeFactor"],
  }

kpiRows = []
index = 0
for buildingId in buildingIds:
  # Record progress
  print(f"{index/buildingIds.size*100}% - Building: {buildingId}")

  kpiRow = processBuilding(buildingId)
  kpiRows.append(kpiRow)
  index = index + 1

kpis = pandas.DataFrame.from_records(kpiRows)
kpis.to_csv("data/kpis.csv")