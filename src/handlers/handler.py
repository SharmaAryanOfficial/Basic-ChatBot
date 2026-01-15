from src.agents.chat_agent.graph import create_chat_agent_graph
from langchain.messages import HumanMessage
from src.agents.chat_agent.states.chat_agent_state import ChatAgentState

graph = create_chat_agent_graph()

def chat_agent_handler(message : str) -> dict[str, str]:
    """
    """
    return graph.invoke(
        input = {
            'messages': [HumanMessage(content = message)]
        },
        config={
            'configurable':{
                'thread_id': '1'
                }
        }
    ) #{'messages': answer from AI}