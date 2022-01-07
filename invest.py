import os
import rasa
import nest_asyncio
from rasa.cli.scaffold import create_initial_project
from rasa.jupyter import chat


nest_asyncio.apply()
print('Event loop ready !')

project = "investement-chatbot"
create_initial_project(project)

os.chdir(project)
print(os.listdir("."))

% % writefile data/nlu.md

# intent:trade
- i want to trade
- live trading stock
- stock trading
- trade right now
- stock investment
- invest in the market
# intent:buy
- i want to buy some stocks
- buy some stocks
- buying side
- buy
- buy some company stock
# intent:buy_details
- buy 200 stock of AAPL company
- buy 15 stock of GOOGL company
- get 56 stock of COKE company
- get 6 stock of FB company
- FB company stock and buy 10 stock of it
- AMZN company stock and buy 25 stock
- TSLA company stock and buy 14 stock
- MSFT company stock and 5 stock
- 15 stock of JNJ company
- 5 stock of GOOGL company
- intent: order_type_market
- i want to submit order as market order types.
- submit my order as market order type
- order as market order
- market order
- market order types
# intent:order_type_limit
- submit my order as limit order type
- order as limit order
- limit order
- i want to submit order as limit order types
- limit order types
# intent:limit_price
- limit price is $ 125
- $ 3600 is my limit price
- 123
- 256.03
- 85 dollar
- 25.63 dollar
- $ 98 dollar
- USD[63] dollar
- 98758.23 USD
- $ 0.25 dollar
## intent: portfolio
- i want to know portfolio details
- portfolio details
- portfolio
- give information about my porfolio details
- portfolio details please
## intent: last_trans
- I want to last few transaction details
- last 5 transaction details
- last transaction detail
- transaction details please
- transaction history
# intent:greet
- hey
- hello
- hi
- good morning
- good evening
- hey there
# intent:goodbye
- bye
- goodbye
- see you around
- see you later
# intent:affirm
- yes
- indeed
- of course
- that sounds good
- correct
# intent:deny
- no
- never
- I don't think so
- don't like that
- no way
- not really
# intent:mood_great
- perfect
- very good
- great
- amazing
- wonderful
- I am feeling very good
- I am great
- I'm good
# intent:mood_unhappy
- sad
- very sad
- unhappy
- bad
- very bad
- awful
- terrible
- not very good
- extremely sad
- so sad
# intent:bot_challenge
- are you a bot?
- are you a human?
- am I talking to a bot?
- am I talking to a human?

% % writefile domain.yml

intents:
    - greet
    - goodbye
    - affirm
    - deny
    - mood_great
    - mood_unhappy
    - bot_challenge
    - portfolio
    - last_trans
    - trade
    - buy
    - buy_details
    - order_type_market
    - order_type_limit
    - limit_price

slots:
    quantity:
        type: unfeaturized
    ticker:
        type: unfeaturized
    types:
        type: unfeaturized
    price:
        type: unfeaturized
    last_price:
        type: unfeaturized

actions:
    - action_portfolio
    - action_last_trans
    - action_buy
    - action_slots

responses:
    utter_details:
    - text: "Ok!!! Great... Wait for a moment your order is submitting in the market..."

    utter_limit_price:
    - text: "Current price of {ticker} stock is ${last_price}, what is your limit price?"

    utter_order_type:
    - text: "what type of order you want to submit as:- Market order or, Limit order?"

    utter_buy_details:
    - text: "which company stock are you invest in it and what is the quantity?"

    utter_trade:
    - text: "Great!,So are you Going to Buy or, Sell the Stocks?"

    utter_greet:
    - text: "Hey! How may i help you?"

    utter_end_greet:
    - text: "Anything else, In which I help You?"

    utter_cheer_up:
    - text: "Here is something to cheer you up:"
    image: "https://i.imgur.com/nGF1K8f.jpg"

    utter_did_that_help:
    - text: "Did that help you?"

    utter_happy:
    - text: "Great, carry on!"

    utter_goodbye:
    - text: "Bye"

    utter_iamabot:
    - text: "I am a bot, powered by Rasa."

entities:
    - quantity
    - ticker
    - types
    - price

session_config:
    session_expiration_time: 60
    carry_over_slots_to_new_session: true


% % writefile data/stories.md

# portfolio
* greet
- utter_greet
* portfolio
- action_portfolio
- utter_end_greet

# transaction details
* greet
- utter_greet
* last_trans
- action_last_trans
- utter_end_greet

# buy market
* greet
- utter_greet
* trade
- utter_trade
* buy
- utter_buy_details
* buy_details
- utter_order_type
* order_type_market
- utter_details
- action_buy
- utter_end_greet

# buy limit
* greet
- utter_greet
* trade
- utter_trade
* buy
- utter_buy_details
* buy_details
- utter_order_type
* order_type_limit
- action_slots
- utter_limit_price
* limit_price
- utter_details
- action_buy
- utter_end_greet

# happy path
* greet
- utter_greet
* mood_great
- utter_happy

# sad path 1
* greet
- utter_greet
* mood_unhappy
- utter_cheer_up
- utter_did_that_help
* affirm
- utter_happy

# sad path 2
* greet
- utter_greet
* mood_unhappy
- utter_cheer_up
- utter_did_that_help
* deny
- utter_goodbye

# say goodbye
* goodbye
- utter_goodbye

# bot challenge
* bot_challenge
- utter_iamabot


config = "config.yml"
domain = "domain.yml"
training_files = "data/"
output = "models/"

model_path = rasa.train(domain, config, [training_files], output)
print(model_path)


endpoints = "endpoints.yml"
chat(model_path, endpoints)
