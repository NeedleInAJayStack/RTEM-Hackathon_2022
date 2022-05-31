# Generates 188v165_Turndown_HVAC.png

import pandas
from onboard.client.models import PointSelector
from api import api, readHistory
from datetime import datetime, timedelta
import matplotlib.pyplot as plt


start = datetime.fromisoformat("2019-06-01T05:00:00+00:00")
end = start + timedelta(days=7)

query = PointSelector()
query.point_types     = ["Electric Consumption"]
query.equipment_types = ["ahu"]
query.buildings       = [165]
selection = api.select_points(query)
pointIds = selection['points']
history165 = pandas.DataFrame(readHistory(pointIds, start, end).sum(axis=1, min_count=1), columns=['Building 165'])

query = PointSelector()
query.point_types     = ["Electric Consumption"]
query.equipment_types = ["ahu"]
query.buildings       = [188]
selection = api.select_points(query)
pointIds = selection['points']
history188 = pandas.DataFrame(readHistory(pointIds, start, end).sum(axis=1, min_count=1), columns=['Building 188'])

history = history165.join(history188).shift(periods=-5, freq="h")

# PLOT
fig = history.plot(figsize=(15,8), fontsize = 12)
fig.set_ylabel('HVAC Electric Consumption (kWh)',fontdict={'fontsize':15})
fig.set_xlabel('Time',fontdict={'fontsize':15})
plt.show()
