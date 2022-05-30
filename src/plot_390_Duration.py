import pandas
from api import readHistory
from energy import normalize, removeOutliers, clusterAnalyze
from buildingPoints import pointsForBuilding
from datetime import datetime, timedelta
import matplotlib.pyplot as plt


# QUERY
pointIds = pointsForBuilding(390)
start = datetime.fromisoformat("2019-07-01T04:00:00+00:00")
end = start + timedelta(days=6)
history = readHistory(pointIds, start, end)

# CLEAN
history = normalize(history, toFreq="15min")
history = removeOutliers(history, maxIqrsFromMean=10)

# Sum columns & name result 'energy'
history = pandas.DataFrame(history.sum(axis=1, min_count=1), columns=['energy']).dropna()

# ANALYZE
clusterResult = clusterAnalyze(history)
kpiHistory = clusterResult.kpiHistory
clusterHistory = clusterResult.clusterHistory

clusterHistory = clusterHistory.rename(columns={"energy": "Actual Energy Consumption", "cluster": "Clustered Consumption Estimate"})

clusterHistory = clusterHistory.shift(periods=-4, freq="h")

# PLOT

fig = clusterHistory.plot(figsize=(15,8), fontsize = 12, ylim=[0,25])
fig.set_ylabel('Electric Consumption (kWh)',fontdict={'fontsize':15})
fig.set_xlabel('Time',fontdict={'fontsize':15})
plt.show()

