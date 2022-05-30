import pandas
from onboard.client.models import PointSelector
from api import api, readHistory
from buildingPoints import pointsForBuilding
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

query = PointSelector()
query.point_ids = [200632, 202744] 
selection = api.select_points(query)
pointIds = selection['points']

# QUERY (BY SPECIFIC START/END)
start = datetime.fromisoformat("2019-06-01T00:00:00+00:00")
end = start + timedelta(days=7)
history = readHistory(pointIds, start, end).rename(columns = {"200632 - Main Power": "Building 165", "202744 - Main Power": "Building 188"})

# PLOT
fig = history.plot(figsize=(15,8), fontsize = 12)
fig.set_ylabel('Energy (kWh)',fontdict={'fontsize':15})
fig.set_xlabel('Time',fontdict={'fontsize':15})
plt.show()
