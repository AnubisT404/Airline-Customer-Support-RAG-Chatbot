import uuid
from agentic_system.build_graph import AgenticGraph
from utils.load_config import LoadConfig
from utils.utilities import _print_event
from typing import List, Tuple

CFG = LoadConfig.load()

graph_instance = AgenticGraph()
graph = graph_instance.Compile_graph()
thread_id = str(uuid.uuid4())
print("thread_id:", thread_id)
print("=======================")

config = {
    "configurable": {
        "passenger_id": "3442 587242",
        "thread_id": thread_id,
        "recursion_limit": 50
    }
}

chatbot_history = []

class ChatBot:
    @staticmethod
    def respond(chatbot: List, message: str) -> Tuple:
        try:
            print("chatbot_history:", chatbot_history)
            _printed = set()
            events = graph.stream(
                {"messages": ("user", message)}, config, stream_mode="values"
            )

            for event in events:
                _print_event(event, _printed)

            snapshot = graph.get_state(config)
            while snapshot.next:
                result = graph.invoke(None, config)
                snapshot = graph.get_state(config)

            # Checking the response
            if snapshot and "messages" in snapshot[0] and snapshot[0]["messages"]:
                last_message = snapshot[0]["messages"][-1].content
                chatbot_history.append((message, last_message))
                return last_message, chatbot_history, None
            else:
                print("Error: Snapshot content is not as expected.")
                return "", chatbot_history, "Something went wrong while processing your request."
        
        except Exception as e:
            print(f"Error in ChatBot.respond: {e}")
            return "", chatbot_history, "Something went wrong while processing your request."