from langgraph.graph import START,END,StateGraph
from util.langgraph_util import display
from pydantic import BaseModel,Field
from typing import Optional
class HelloWorldState(BaseModel):
    message: str = Field(min_length=1)
    id:Optional[int]=None
def hello(state: HelloWorldState):
    print(f"Hello  {state.message}")
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
out=runnable.invoke({"message":"b"})
print(out)