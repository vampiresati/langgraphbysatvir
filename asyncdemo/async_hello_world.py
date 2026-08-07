import asyncio
from typing import Optional

from langgraph.graph import START, END, StateGraph
from pydantic import BaseModel, Field

from util.langgraph_util import display


class HelloWorldState(BaseModel):
    message: str = Field(min_length=1)
    id:Optional[int]=None
async def hello(state: HelloWorldState):
    print(f"Hello  {state.message}")
    await asyncio.sleep(1)
    return {'message': f"Hello {state.message} again!"}
async def goodbye(state: HelloWorldState):
    print(f"Goodbye ! {state.message}")
    await asyncio.sleep(1)
    return {'message': f"Goodbye {state.message} again!"}



graph = StateGraph(HelloWorldState)
graph.add_node("hello",hello)
graph.add_node("bye", goodbye)

graph.add_edge(START,"hello")
graph.add_edge("hello","bye")
graph.add_edge("bye",END)
runnable = graph.compile()
display(runnable)
async def main():
    out= await runnable.ainvoke({"message":"satvir"})
    print(out)
asyncio.run(main())