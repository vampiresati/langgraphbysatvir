from langgraph.graph import START, END, StateGraph
from util.langgraph_util import display
from typing import TypedDict, Annotated
from operator import add

from langchain_core.messages import AnyMessage
from langchain_core.messages import AIMessage, HumanMessage


class ChatbotState(TypedDict):
    message: Annotated[list[AnyMessage], add]
    discount: Annotated[int, add]


def connect_to_sale(state: ChatbotState):
    return {
        "message": [AIMessage(content="connect to sale")],
        "discount": 10
    }


def sale_team_response(state: ChatbotState):
    return {
        "message": [AIMessage(content="offer for you")],
        "discount": 20
    }


graph = StateGraph(ChatbotState)

graph.add_node("connect_to_sale", connect_to_sale)
graph.add_node("sale_team_response", sale_team_response)

graph.add_edge(START, "connect_to_sale")
graph.add_edge("connect_to_sale", "sale_team_response")
graph.add_edge("sale_team_response", END)

chatbot = graph.compile()

display(chatbot)

result = chatbot.invoke({
    "message": [HumanMessage(content="i want to buy product")],
    "discount": 0
})

for m in result["message"]:
    print(f"message -> {m.content}")

print(f"total discount is {result['discount']}")