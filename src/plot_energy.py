import pandas
from api import readHistory
from energy import normalize, removeOutliers, clusterAnalyze
from buildingPoints import pointsForBuilding
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

pointIds = pointsForBuilding(390)

# QUERY
# history = readHistory(pointIds)

# QUERY (BY SPECIFIC START/END)
start = datetime.fromisoformat("2019-07-01T00:00:00+00:00")
end = start + timedelta(days=7)
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

# PLOT
# fig = history.plot(figsize=(15,8), fontsize = 12)
# fig.set_ylabel('Value',fontdict={'fontsize':15})
# fig.set_xlabel('Time',fontdict={'fontsize':15})
# plt.show()

# fig = kpiHistory["occupied_duration_factor"].plot(figsize=(15,8), fontsize = 12)
# fig.set_ylabel('Value',fontdict={'fontsize':15})
# fig.set_xlabel('Time',fontdict={'fontsize':15})
# plt.show()

fig = clusterHistory.plot(figsize=(15,8), fontsize = 12)
fig.set_ylabel('Value',fontdict={'fontsize':15})
fig.set_xlabel('Time',fontdict={'fontsize':15})
plt.show()
