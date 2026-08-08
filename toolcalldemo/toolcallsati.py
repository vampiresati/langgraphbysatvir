from pathlib import Path
import sys

from langchain_core.messages import AnyMessage
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from typing import Annotated
from typing_extensions import TypedDict

# Allow direct execution via `python toolcalldemo/toolcallsati.py`.
sys.path.append(str(Path(__file__).resolve().parents[1]))

from util.langgraph_util import display

class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

@tool
def get_restaurant_recommendations(location: str):
    """Provides restaurant recommendations for a given location."""
    recommendations = {
        "munich": ["Hofbräuhaus", "Augustiner-Keller", "Tantris"],
        "new york": ["Le Bernardin", "Eleven Madison Park", "Joe's Pizza"],
        "paris": ["Le Meurice", "L'Ambroisie", "Bistrot Paul Bert"],
        "sirhind": ["aam khas bhag", "sidhu restaurant", "rana heritage"],
        "gobindgarh": ["soya hut", "khas bhavan"],
    }

    return recommendations.get(
        location.lower(),
        ["No recommendations available for this location."]
    )

tools = [get_restaurant_recommendations]

llm = ChatOllama(
    model="qwen3:4b",
    temperature=0,
)
model = llm.bind_tools(tools)
toolnode = ToolNode(tools)

def call_model(state: State):
    response = model.invoke(state["messages"])
    return {"messages": [response]}


def my_tool_condition(state: State):
    last_message = state["messages"][-1]
    if getattr(last_message, "tool_calls", None):
        return "tools"
    return END


graph = StateGraph(State)
graph.add_node("call_model", call_model)
graph.add_node("tools", toolnode)

graph.add_edge(START, "call_model")
graph.add_edge("tools", "call_model")
graph.add_conditional_edges("call_model",my_tool_condition,{"tools": "tools",END: END,})


runnable = graph.compile()

try:
    display(runnable)
except Exception as exc:
    print(f"Unable to render graph image: {exc}")


result = runnable.invoke(
      {
          "messages": [
              {
                  "role": "user",
                  "content": "Recommend some restaurants in Sirhind.",
              }
          ]
      }
  )

print(result["messages"][-1].content)
