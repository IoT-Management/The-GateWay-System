#creating a template for data addition

from pydantic import BaseModel
from typing import Dict, Any

class DeviceBlueprint(BaseModel):

	node_id: str
	node_uid: str
	node_type: str
	firmware_ver: str
	location: str
	plugin: str
	data: Dict[str,Any]
