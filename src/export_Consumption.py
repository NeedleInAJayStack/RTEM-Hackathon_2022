# Exports electric-consumption_orig.csv

from api import api
import pandas
from onboard.client.models import PointSelector

selector = PointSelector()
selector.point_types = ['Electric Consumption']
selector.equipment_types = ['meter', 'site', 'panel', 'virtual']
selection = api.select_points(selector)
points = api.get_points_by_ids(selection['points'])
frame = pandas.DataFrame(points)
frame.to_csv("./data/electric-consumption_orig.csv")