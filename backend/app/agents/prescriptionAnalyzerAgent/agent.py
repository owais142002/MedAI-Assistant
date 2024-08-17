from langchain.tools import BaseTool
from typing import Any, Dict, Optional
from app.utils import get_data_from_image

class PrescriptionAnalyzerAgent(BaseTool):
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
            "PrescriptionAnalyzerAgent_Tool does not support sync")    
        
    async def _arun(self, input, run_manager) -> str:
        print(input)
        data = get_data_from_image(system_message="You are an helpful assistant that extracts medicine names along with all the important information from the given image.", image_url=input)
        print(data)
        return data