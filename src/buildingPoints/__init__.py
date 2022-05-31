import pandas

energyPoints = pandas.read_csv("data/electric-consumption.csv")
buildingIds = energyPoints["building_id"].unique()

def pointsForBuilding(buildingId: int):
  """
  Returns an integer list of point ids from the `electric-consumption.csv` file that have a `building_id`
  column matching the input.
  """
  pointIds = energyPoints.query(f"building_id == {buildingId}")["id"].values
  return list(pointIds.astype(float)) # For some reason we have to do this to make it JSON Serializable... See https://stackoverflow.com/questions/57269741/typeerror-object-of-type-ndarray-is-not-json-serializable
  