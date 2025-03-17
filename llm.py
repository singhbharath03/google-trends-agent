import json

from groq import AsyncGroq
from config import get_settings
from serpa_api import get_google_trends_data
from tools.dictionary import get_from_dict
from trade.constants import ATTENTION_MARKETS_TOTAL_SUPPLY
from trade.token_account import get_user_token_balance
from trade.trader import buy, sell

MODEL = "deepseek-r1-distill-llama-70b"
AGENT_SYSTEM_PROMPT = """
You are a trader agent whose goal is to profit from trading attention tokens. 
"""


client = AsyncGroq(
    api_key=get_settings().groq_api_key,
)


async def get_completion(messages: list):
    tools = [
        {
            "type": "function",
            "function": {
                "name": "make_trade",
                "description": "Make a trade",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": ["BUY", "SELL", "DO_NOTHING"],
                            "description": "The action to take",
                        },
                        "amount": {
                            "type": "number",
                            "description": "The amount of the token to trade",
                        },
                    },
                    "required": ["action", "amount"],
                },
                "returns": {
                    "type": "string",
                    "description": "The result of the trade",
                },
            },
        },
    ]

    chat_completion_obj = await client.chat.completions.create(
        messages=messages,
        model=MODEL,
        tools=tools,
        tool_choice="auto",
    )

    response = chat_completion_obj.choices[0].message.to_dict()

    return response


async def process_agent_action_for_market(
    slug: str, token_mint: str, wallet_address: str
):
    google_trends_data = get_google_trends_data(slug)

    user_token_balance = await get_user_token_balance(wallet_address, token_mint)
    print("slug ", slug)
    print("user_token_balance ", user_token_balance)

    messages = [
        {"role": "system", "content": AGENT_SYSTEM_PROMPT},
        {
            "role": "user",
            "content": f"""
The google trends data for {slug} is {google_trends_data}. 
The total supply of the token is {ATTENTION_MARKETS_TOTAL_SUPPLY} and user token balance is {user_token_balance}. 
Make a trade action based on the data.
""",
        },
    ]

    response = await get_completion(messages)

    # Handle tool calls if present
    if response.get("tool_calls"):
        tools_responses = []
        for tool_call in response.get("tool_calls"):
            try:
                function_name = get_from_dict(tool_call, ["function", "name"])
                fn_args = json.loads(
                    get_from_dict(tool_call, ["function", "arguments"])
                )

                # Call the appropriate function
                if function_name == "make_trade":
                    print("action requested by LLM ", fn_args)

                    if fn_args["action"] == "BUY":
                        result = await buy(
                            wallet_address,
                            token_mint,
                            fn_args["amount"],
                        )
                    elif fn_args["action"] == "SELL":
                        result = await sell(
                            wallet_address,
                            token_mint,
                            fn_args["amount"],
                        )
                else:
                    result = f"Error: Unknown function '{function_name}'"

                # Add the function response to messages
                tools_responses.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call["id"],
                        "name": function_name,
                        "content": str(result),
                    }
                )
            except Exception as e:
                # Add error response for failed tool calls
                import traceback

                print(f"Error executing tool call: {traceback.format_exc()}")
                tools_responses.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call["id"],
                        "name": function_name,
                        "content": f"Error executing {function_name}: {str(e)}",
                    }
                )

        messages.extend(tools_responses)

    return None
