#creating a template for data addition

from pydantic import BaseModel

class DeviceBlueprint(BaseModel):

	NodeID: str
	data: dict
