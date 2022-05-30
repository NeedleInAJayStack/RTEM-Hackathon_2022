import pandas
from onboard.client.models import PointSelector
from energy import normalize, removeOutliers, clusterAnalyze
from api import api, readHistory
from buildingPoints import pointsForBuilding
from datetime import datetime, timedelta
import matplotlib.pyplot as plt


start = datetime.fromisoformat("2020-03-01T00:00:00+00:00")
end = start + timedelta(days=7)

history275 = readHistory(pointsForBuilding(275), start, end)
history275 = removeOutliers(normalize(history275, toFreq="15min"), maxIqrsFromMean=10)
history275 = pandas.DataFrame(history275.sum(axis=1, min_count=1), columns=['Building 275']).dropna()

history393 = readHistory(pointsForBuilding(393), start, end)
history393 = removeOutliers(normalize(history393, toFreq="15min"), maxIqrsFromMean=10)
history393 = pandas.DataFrame(history393.sum(axis=1, min_count=1), columns=['Building 393']).dropna()

history = history275.join(history393, how="outer").interpolate(method="time")

# PLOT
fig = history.plot(figsize=(15,8), fontsize = 12)
fig.set_ylabel('Energy (kWh)',fontdict={'fontsize':15})
fig.set_xlabel('Time',fontdict={'fontsize':15})
plt.show()
