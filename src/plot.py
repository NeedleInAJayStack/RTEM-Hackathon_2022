import pandas
from api import readHistory
from energy import normalize, removeOutliers, clusterAnalyze
from buildingPoints import pointsForBuilding
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

pointIds = pointsForBuilding(420)

# QUERY
history = readHistory(pointIds)

# QUERY (BY SPECIFIC START/END)
# start = datetime.fromisoformat("2018-10-01T00:00:00+00:00")
# end = start + timedelta(days=30)
# history = readHistory(pointIds, start, end)

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

# fig = kpiHistory["highUsageTimeFactor"].plot(figsize=(15,8), fontsize = 12)
# fig.set_ylabel('Value',fontdict={'fontsize':15})
# fig.set_xlabel('Time',fontdict={'fontsize':15})
# plt.show()

fig = clusterHistory.plot(figsize=(15,8), fontsize = 12)
fig.set_ylabel('Value',fontdict={'fontsize':15})
fig.set_xlabel('Time',fontdict={'fontsize':15})
plt.show()

