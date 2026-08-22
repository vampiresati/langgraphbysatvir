from langchain_core.tools import tool
from langgraph.graph import START,END,StateGraph
from util.langgraph_util import display
from typing import TypedDict

@tool
def add(a:int,b:int):
    """adds two numbers
    Args:
        a (int): first number
        b (int): second number
    """
    return a+b
@tool
def minus(a:int ,b:int):
    """
    Subtracts two integers and returns the result.

    This function takes two integer inputs and calculates their difference.
    It does not perform any form of validation for the inputs as it assumes
    that valid integers are always provided.

    :param a: The first integer operand of the subtraction.
    :type a: int
    :param b: The second integer operand of the subtraction (to be subtracted
        from the first integer operand).
    :type b: int
    :return: The resulting integer after subtracting the second operand
        from the first operand.
    :rtype: int
    """
    return a-b

