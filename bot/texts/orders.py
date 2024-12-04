
class OrdersTexts:
    MENU = """<b>Order Creation</b>
    
<blockquote>Use the buttons below to set up your order. Please note that you choose how many tokens you want to receive.</blockquote>
"""
    SETUP_TOKEN = """<b>Choose action</b>"""

    ENTER_AMOUNT = "<b>Enter amount</b>"

    AMOUNT_INCORRECT = "<b>Amount incorrect, try again</b>"

    SLIPPAGE = """<b>Select slippage</b>"""

    SELECT_RECEIVE_TOKEN = """<b>Paste CA of token</b>"""

    CONFIRMATION = """<b>Confirmation</b>

<blockquote>Send: <b>{send_amount} {send_token_symbol} (${send_token_rate})</b>

Receive: <b>{receive_amount} {receive_token_symbol} (${receive_token_rate})</b>

Slippage: {slippage}%
Min. receive: {minimum_to_receive_amount} {receive_token_symbol}
Provider: DeDust.io</blockquote>

Profit: <b>{profit_in_usd}$ ({profit_percent})</b>
"""

    CREATED = "🚀 <b>Order Created!</b>"

    TOKEN_NOT_FOUND = """<b>Token not found, try again</b>"""

    VIEW = """<b>Orders</b>

<blockquote>Here are your active limit orders, you can delete or view detailed information</blockquote>
"""

    SPECIFIC = """<b>Order #{order_id}</b>
"""
