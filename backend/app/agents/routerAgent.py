from app.agents.heartrateAnalyzerAgent.agent import HeartRateAnalyzerAgent
from app.agents.prescriptionAnalyzerAgent.agent import PrescriptionAnalyzerAgent
from app.agents.medicineSearchAgent.agent import MedicineSearchAgent
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_community.chat_message_histories.sql import SQLChatMessageHistory
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
import GlobalConstants
from app.utils import getPromptTemplate

agents = {
    HeartRateAnalyzerAgent : {
        "name": "Heart_Rate_Analyzer",
        "description": "This agent fetches the heart rate data of the user of last 7 days."
    },
    PrescriptionAnalyzerAgent : {
        "name": "Prescription_Analyzer",
        "description": "This agent extracts the medicines names along with all the meaningful things from an computer generated prescription image given by user."
    },
    MedicineSearchAgent: {
        "name": "Medicine_Search_Agent",
        "description": "This agent extracts all information a medicine if the PrescriptionAnalyzerAgent can not retrive info about that medicine."
    }
}

def getMemory(userId):
    message_history = SQLChatMessageHistory(
        connection_string="mysql+pymysql://root:owaisahmed123@localhost:3306/medbot_db",
        session_id=userId,
        table_name="chat_history",
    )

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        chat_memory=message_history,
        return_messages=True,
        output_key="output",
    )
    return memory


def getLLM():
    llm = ChatOpenAI(
            temperature=0,
            model=GlobalConstants.LLM_MODEL,
            openai_api_key=GlobalConstants.LLM_API_KEY,
            streaming=True,
            top_p= 0.01
        )    

    return llm


def createRouterAgent(userId):
    subAgents = []
    for agent in agents:
        subAgents.append(agent(agentJson=agents[agent], userId=userId))
    print(subAgents)
    memory = getMemory(userId=userId)
    prompt = getPromptTemplate(GlobalConstants.MAIN_AGENT_SYSTEM_MESSAGE)
    llm = getLLM()    
    agent = create_openai_tools_agent(llm=llm, tools=subAgents, prompt=prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=subAgents,
        verbose=GlobalConstants.IS_DEBUG_MODE,
        memory=memory,
        max_iterations=GlobalConstants.MAX_AGENT_ITERATIONS
    )
    return agent_executor    