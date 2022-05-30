import pandas
from onboard.client.models import PointSelector
from api import api, readHistory
from buildingPoints import pointsForBuilding
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

query = PointSelector()
query.point_types     = ["Electric Consumption"]# ["Zone Heating Temperature Setpoint", "Zone Cooling Temperature Setpoint"]
query.equipment_types = ["ahu"]
query.buildings       = [165, 188]
# query.point_ids = [200632, 202744] 
selection = api.select_points(query)
pointIds = selection['points']
print(pointIds)

# QUERY
# history = readHistory(pointIds)

# QUERY (BY SPECIFIC START/END)
start = datetime.fromisoformat("2019-06-01T00:00:00+00:00")
end = start + timedelta(days=7)
history = readHistory(pointIds, start, end)

# PLOT
fig = history.plot(figsize=(15,8), fontsize = 12)
fig.set_ylabel('Value',fontdict={'fontsize':15})
fig.set_xlabel('Time',fontdict={'fontsize':15})
plt.show()
