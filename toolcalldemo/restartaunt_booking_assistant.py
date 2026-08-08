from typing import Annotated
from typing_extensions import TypedDict

from langchain_core.messages import AnyMessage, SystemMessage
from langchain_core.tools import tool
from langchain_ollama import ChatOllama

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode


class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


# -----------------------------------
# Tools
# -----------------------------------

@tool
def check_restaurant_availability(
    restaurant: str,
    date: str,
    time: str,
    guests: int
):
    """Check whether a restaurant has availability."""

    # Dummy availability logic
    if restaurant.lower() == "tantris" and time == "19:00":
        return {
            "available": False,
            "alternative_times": ["18:00", "20:30"]
        }

    return {
        "available": True,
        "restaurant": restaurant,
        "date": date,
        "time": time,
        "guests": guests
    }


@tool
def create_restaurant_booking(
    restaurant: str,
    date: str,
    time: str,
    guests: int,
    customer_name: str
):
    """Create a restaurant reservation."""

    return {
        "status": "confirmed",
        "booking_id": "RES-12345",
        "restaurant": restaurant,
        "date": date,
        "time": time,
        "guests": guests,
        "customer_name": customer_name
    }


tools = [
    check_restaurant_availability,
    create_restaurant_booking
]


# -----------------------------------
# Model
# -----------------------------------

llm = ChatOllama(
    model="qwen3:4b",
    temperature=0
)

model = llm.bind_tools(tools)


# -----------------------------------
# System prompt
# -----------------------------------

SYSTEM_PROMPT = """
You are a restaurant booking assistant.

Your role is to act like a professional restaurant receptionist.

You help customers make restaurant reservations.

Before checking availability, collect:

- restaurant name
- date
- time
- number of guests

Before creating the final reservation, also collect:

- customer name

Rules:

1. Ask only for information that is missing.
2. Never invent booking information.
3. Use check_restaurant_availability before confirming a booking.
4. If the requested time is unavailable, offer the alternative times.
5. Do not create the booking until the customer agrees to an available time.
6. Once the customer agrees, call create_restaurant_booking.
7. After booking, give the customer the booking ID and reservation details.
8. Be friendly and concise.
"""


# -----------------------------------
# Agent node
# -----------------------------------

def call_model(state: State):

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        *state["messages"]
    ]

    response = model.invoke(messages)

    return {
        "messages": [response]
    }


# -----------------------------------
# Router
# -----------------------------------

def should_call_tool(state: State):

    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tools"

    return END


# -----------------------------------
# Graph
# -----------------------------------

graph = StateGraph(State)

graph.add_node(
    "call_model",
    call_model
)

graph.add_node(
    "tools",
    ToolNode(tools)
)

graph.add_edge(
    START,
    "call_model"
)

graph.add_conditional_edges(
    "call_model",
    should_call_tool,
    {
        "tools": "tools",
        END: END
    }
)

graph.add_edge(
    "tools",
    "call_model"
)

app = graph.compile()

from langchain_core.messages import HumanMessage


if __name__ == "__main__":

    state = {
        "messages": []
    }

    print("🍽️ Restaurant Booking Assistant")
    print("Type 'exit' to quit.\n")

    while True:

        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        # Add user's message
        state["messages"].append(
            HumanMessage(content=user_input)
        )

        # Run LangGraph
        result = app.invoke(state)

        # Save updated conversation
        state = result

        # Get final AI response
        final_message = result["messages"][-1]

        print("\nAgent:", final_message.content)
        print()