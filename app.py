import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message, send_image_message

load_dotenv()


machine = TocMachine(
    states = ["user", "achievement", "furniture", "divination_1", "divination_2", "forbidden_forest_1", "forbidden_forest_2", "forbidden_forest_3", 
              "always", "limited", "hidden", "level_1", "level_2", "level_3", "level_4", "level_5", "menu", 
              "centaur", "potion", "unicorn", "dog", "daniel", "galleon", "graphorn", "thunder", "seeker"], 
    transitions = [
        {
            "trigger": "advance",
            "source": "user",
            "dest": "achievement",
            "conditions": "is_going_to_achievement",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "furniture",
            "conditions": "is_going_to_furniture",
        },
        {
            "trigger": "advance",
            "source": "furniture",
            "dest": "always",
            "conditions": "is_going_to_always",
        },
        {
            "trigger": "advance",
            "source": "furniture",
            "dest": "limited",
            "conditions": "is_going_to_limited",
        },
        {
            "trigger": "advance",
            "source": "furniture",
            "dest": "hidden",
            "conditions": "is_going_to_hidden",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "divination_1",
            "conditions": "is_going_to_divination_1",
        },
        {
            "trigger": "advance",
            "source": "divination_1",
            "dest": "level_1",
            "conditions": "is_going_to_level_1",
        },
        {
            "trigger": "advance",
            "source": "divination_1",
            "dest": "level_2",
            "conditions": "is_going_to_level_2",
        },
        {
            "trigger": "advance",
            "source": "divination_1",
            "dest": "level_3",
            "conditions": "is_going_to_level_3",
        },
        {
            "trigger": "advance",
            "source": "divination_1",
            "dest": "divination_2",
            "conditions": "is_going_to_divination_2",
        },
        {
            "trigger": "advance",
            "source": "divination_2",
            "dest": "level_4",
            "conditions": "is_going_to_level_4",
        },
        {
            "trigger": "advance",
            "source": "divination_2",
            "dest": "level_5",
            "conditions": "is_going_to_level_5",
        },
        {
            "trigger": "advance",
            "source": "divination_2",
            "dest": "divination_1",
            "conditions": "is_going_to_divination_1",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "forbidden_forest_1",
            "conditions": "is_going_to_forbidden_forest_1",
        },
        {
            "trigger": "advance",
            "source": "forbidden_forest_1",
            "dest": "centaur",
            "conditions": "is_going_to_centaur",
        },
        {
            "trigger": "advance",
            "source": "forbidden_forest_1",
            "dest": "potion",
            "conditions": "is_going_to_potion",
        },
        {
            "trigger": "advance",
            "source": "forbidden_forest_1",
            "dest": "unicorn",
            "conditions": "is_going_to_unicorn",
        },
        {
            "trigger": "advance",
            "source": "forbidden_forest_1",
            "dest": "forbidden_forest_2", 
            "conditions": "is_going_to_forbidden_forest_2",
        },
        {
            "trigger": "advance",
            "source": "forbidden_forest_2",
            "dest": "dog",
            "conditions": "is_going_to_dog",
        },
        {
            "trigger": "advance",
            "source": "forbidden_forest_2",
            "dest": "daniel",
            "conditions": "is_going_to_daniel",
        },
        {
            "trigger": "advance",
            "source": "forbidden_forest_2",
            "dest": "galleon",
            "conditions": "is_going_to_galleon",
        },
        {
            "trigger": "advance",
            "source": "forbidden_forest_2",
            "dest": "forbidden_forest_3",
            "conditions": "is_going_to_forbidden_forest_3",
        },
        {
            "trigger": "advance",
            "source": "forbidden_forest_3",
            "dest": "graphorn",
            "conditions": "is_going_to_graphorn",
        },
        {
            "trigger": "advance",
            "source": "forbidden_forest_3",
            "dest": "thunder",
            "conditions": "is_going_to_thunder",
        },
        {
            "trigger": "advance",
            "source": "forbidden_forest_3",
            "dest": "seeker",
            "conditions": "is_going_to_seeker",
        },
        {
            "trigger": "advance",
            "source": "forbidden_forest_3",
            "dest": "forbidden_forest_1",
            "conditions": "is_going_to_forbidden_forest_1",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "menu",
            "conditions": "is_going_to_menu",
        },
        {
            "trigger": "advance",
            "source": "achievement",
            "dest": "menu",
            "conditions": "is_going_to_menu",
        },
        {
            "trigger": "advance",
            "source": "furniture",
            "dest": "menu",
            "conditions": "is_going_to_menu",
        },
        {
            "trigger": "advance",
            "source": "divination_1",
            "dest": "menu",
            "conditions": "is_going_to_menu",
        },
        {
            "trigger": "advance",
            "source": "divination_2",
            "dest": "menu",
            "conditions": "is_going_to_menu",
        },
        {
            "trigger": "advance",
            "source": "forbidden_forest_1",
            "dest": "menu",
            "conditions": "is_going_to_menu",
        },
        {
            "trigger": "advance",
            "source": "forbidden_forest_2",
            "dest": "menu",
            "conditions": "is_going_to_menu",
        },
        {
            "trigger": "advance",
            "source": "forbidden_forest_3",
            "dest": "menu",
            "conditions": "is_going_to_menu",
        },
        {"trigger": "go_back", "source": ["always", "limited", "hidden"], "dest": "furniture"},
        {"trigger": "go_back", "source": ["level_1", "level_2", "level_3"], "dest": "divination_1"},
        {"trigger": "go_back", "source": ["level_4", "level_5"], "dest": "divination_2"},
        {"trigger": "go_back", "source": ["centaur", "potion", "unicorn"], "dest": "forbidden_forest_1"},
        {"trigger": "go_back", "source": ["dog", "daniel", "galleon"], "dest": "forbidden_forest_2"},
        {"trigger": "go_back", "source": ["graphorn", "thunder", "seeker"], "dest": "forbidden_forest_3"},
        {"trigger": "go_back", "source": "menu", "dest": "user"},
    ],
    initial = "user",
    auto_transitions = False,
    show_conditions = True,
)

app = Flask(__name__, static_url_path = "")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


"""
@app.route("/callback", methods = ["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text = True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text = event.message.text)
        )

    return "OK"
"""


@app.route("/webhook", methods = ["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text = True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")

        response = machine.advance(event)

        if response == False:
            if event.message.text.lower() == 'fsm':
                # send_image_message(event.reply_token, "https://f74086153.herokuapp.com/show-fsm")
                send_image_message(event.reply_token, "https://c351-36-237-107-170.ngrok.io/show-fsm")
            else:
                send_text_message(event.reply_token, "請輸入正確單詞")

    return "OK"


@app.route("/show-fsm", methods = ["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog = "dot", format = "png")
    return send_file("fsm.png", mimetype = "image/png")


if __name__ == "__main__":
    # port = os.environ["PORT"]
    port = os.environ.get("PORT", 8000)
    app.run(host = "0.0.0.0", port = port, debug = True)
