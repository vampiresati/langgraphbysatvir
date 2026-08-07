from langgraph.graph import START,END,StateGraph
from util.langgraph_util import display
from typing import TypedDict

class SupportRequest(TypedDict):
    message: str
    priority: int

def standard_response(request: SupportRequest):
    print(f"standard {request}")
    return request
def urgent_response(request: SupportRequest):
    print(f"urgent {request}")
    return request
def conditional_response(request: SupportRequest):
    if request['priority']== 1 or 'urgent' in  request['message']:
        return urgent_response(request)
    return standard_response(request)

graph = StateGraph(SupportRequest)
graph.add_node("standard",standard_response)
graph.add_node("urgent",urgent_response)

graph.add_conditional_edges(START,conditional_response)
graph.add_edge("standard",END)
graph.add_edge("urgent",END)

runnable = graph.compile()
display(runnable)
runnable.invoke({"message":"My password is hacked","priority":1})
runnable.invoke({"message":"change my password please","priority":3})
runnable.invoke({"message":"My gmail is hacked it is urgent","priority":2})