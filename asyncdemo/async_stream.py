from typing import Optional
from langgraph.graph import START, END, StateGraph
from pydantic import BaseModel, Field
from util.langgraph_util import display
from langgraph.types import StreamWriter
class HelloWorldState(BaseModel):
    message: str = Field(min_length=1)
    id:Optional[int]=None
def hello(state: HelloWorldState):
    print(f"Hello  {state.message}")
    # writer({"custome_keys":"satvir"})
    return {'message': f"Hello {state.message} again!"}
def goodbye(state: HelloWorldState):
    print(f"Goodbye ! {state.message}")
    return {'message': f"Goodbye {state.message} again!"}



graph = StateGraph(HelloWorldState)
graph.add_node("hello",hello)
graph.add_node("bye", goodbye)

graph.add_edge(START,"hello")
graph.add_edge("hello","bye")
graph.add_edge("bye",END)
runnable = graph.compile()
display(runnable)
for chunk in runnable.stream({"message":"satvir"},stream_mode="debug"):
    print(chunk)

#stream_mode="values"
#stream_mode="updates"
#stream_mode="custom"
#stream_mode="messages"
#stream_mode="debug"