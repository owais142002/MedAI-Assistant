from langchain.tools import BaseTool
from typing import Any, Dict, Optional
from app.utils import get_data_from_fibbit, simplify_heart_rate_data
from datetime import datetime, timedelta

class HeartRateAnalyzerAgent(BaseTool):
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
            "HeartRateAnalyzerAgent_Tool does not support sync")    
        
    async def _arun(self, input, run_manager) -> str:
        heartRateData = get_data_from_fibbit(
            start_date=(datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'),
            end_date= datetime.now().strftime('%Y-%m-%d'),
            access_token= run_manager.tags[2],
            get_random_sample = True)
        
        heartRateData = simplify_heart_rate_data(heartRateData)
        return heartRateData