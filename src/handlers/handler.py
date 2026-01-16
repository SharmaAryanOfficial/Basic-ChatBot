from src.agents.chat_agent.graph import create_chat_agent_graph
from langchain.messages import HumanMessage
from src.agents.chat_agent.states.chat_agent_state import ChatAgentState

graph = create_chat_agent_graph()

def chat_agent_handler(thread_id: str, message : str) -> ChatAgentState:
    """
    """
    return graph.invoke(
        input = {
            'messages': [HumanMessage(content = message)]
        },
        config={
            'configurable':{
                'thread_id': thread_id
                }
        }
    ) #{'messages': answer from AI}



def get_all_threads_handler() ->list[str | None]:
    """
    Docstring for get_all_threads_handler
    """
    all_checkpoints =  graph.checkpointer.list(config={})

    threads = set()

    for checkpoint in all_checkpoints:
        threads.add(checkpoint.config['configurable']['thread_id'])

    return list (threads)

def chat_history_handler(thread_id: str) -> ChatAgentState | dict[None, None]:
    """
    Docstring for chat_history_handler
    """
    return graph.get_state(config={
        'configurable': {
            'thread_id': thread_id
        }
    })[0]