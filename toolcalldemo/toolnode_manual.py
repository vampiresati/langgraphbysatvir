from typing import Annotated
from typing_extensions import TypedDict
from util.langgraph_util import display
from langchain_core.messages import AnyMessage
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition


class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


@tool
def get_restaurant_recommendations(location: str):
    """Provides restaurant recommendations for a given location."""
    recommendations = {
        "munich": ["Hofbräuhaus", "Augustiner-Keller", "Tantris"],
        "new york": ["Le Bernardin", "Eleven Madison Park", "Joe's Pizza"],
        "paris": ["Le Meurice", "L'Ambroisie", "Bistrot Paul Bert"],
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

llm_with_tools = llm.bind_tools(tools)


def chatbot(state: State):
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}


builder = StateGraph(State)

builder.add_node("chatbot", chatbot)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "chatbot")
builder.add_edge("tools", "chatbot")

builder.add_conditional_edges("chatbot",tools_condition,{"tools": "tools",END: END,},)


graph = builder.compile()
display(graph)

result = graph.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Recommend some restaurants in Paris.",
            }
        ]
    }
)

print(result["messages"][-1].content)