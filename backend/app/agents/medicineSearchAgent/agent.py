from langchain.tools import BaseTool
from typing import Any, Dict, Optional, List
from app.utils import get_data_from_medicinedb
from datetime import datetime, timedelta

class MedicineSearchAgent(BaseTool):
    name = ""
    description = ""
    userId = ""

    def __init__(self, agentJson, userId):
        super().__init__()
        self.name = agentJson["name"]
        self.description = agentJson["description"]
        self.userId = userId 
        self.return_direct = False   

    def _run(self, input: Optional[str] = None) -> str:
        raise NotImplementedError(
            "Medicine Search Agent_Tool does not support sync")    
        
    async def _arun(self, input, run_manager) -> str:
        medicineData = get_data_from_medicinedb(input)
        return medicineData