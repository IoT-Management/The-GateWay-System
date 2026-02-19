#creating a template for data addition

from pydantic import BaseModel
from typing import Dict, Any

class DeviceBlueprint(BaseModel):

	node_id: str
	data: Dict[str,Any]
