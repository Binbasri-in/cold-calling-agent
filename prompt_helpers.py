import os
from customizable_parameters import company_details, product_details, offers_available, additional_instructions
from dotenv import load_dotenv
from getpass import getpass
import requests

load_dotenv()

if "CLOUDFLARE_API_TOKEN" in os.environ:
    api_token = os.environ["CLOUDFLARE_API_TOKEN"]
else:
    api_token = getpass("Enter you Cloudflare API Token")
    
if "CLOUDFLARE_ACCOUNT_ID" in os.environ:
    account_id = os.environ["CLOUDFLARE_ACCOUNT_ID"]
else:
    account_id = getpass("Enter your account id")

model = "@cf/meta/llama-2-7b-chat-int8"


previous_response = ""
main_prompt = ""


def generate_greeting(customer_name):
    global main_prompt
    global previous_response

    # TODO: generate greeting using the OpenAI API
    greeting_prompt = f"""
    You are convincing salesperson named Sarah that will not take no for an answer. You are have just cold called a  potential customer. you are trying to sell them a product. 
    you are persuasive and you are very good at convincing people to buy your product. you are very good at making people feel comfortable and you are very good at
    making people feel like they can trust you.

    Here are the Company details: {company_details}
    Here are the Product details: {product_details}
    Here are the Offers available: {offers_available}
    Here are the Additional instructions: {additional_instructions}

    the customer name is: {customer_name}

    Here is a describtion of you and how you answer the phone:
    - Your name is Sarah
    - You are a salesperson
    - You are very persuasive
    - You are very good at convincing people to buy your product
    - Your Voice Tone is: sexy and confident
    
    Give me a greeting that you would say to the customer with a very short discription of the product and give them an offer that you think they would be interested in. make your speech 60 words. focus on the product and how to sell it to the customer.
    at the end of your speech you should ask the customer the question if we can schedule an appointmet to speak to a specialist.

    ---------------------------------------------
    customer: Hello
    ---------------------------------------------
    you:
    """

    # generate greeting
    response = requests.post(
        f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/{model}",
        headers={"Authorization": f"Bearer {api_token}"},
        json={"messages": [
            {"role": "system", "content": "follow the instructions and generate a text response to the prompt"},
            {"role": "user", "content": greeting_prompt}
        ]}
    )

    inference = response.json()
    text = inference["result"]["response"]
    previous_response = text
    main_prompt = greeting_prompt + previous_response + "\n---------------------------------------------\ncustomer:"

    print(text)
    return text


def understand_intent(user_input):
    # TODO: understand the user input using the OpenAI API
    intent_prompt = f"""
    I will give you a conversation and try to classify the customer intention into one of the following categories:
    1. continue_conversation
    2. time_to_say_goodbye
    Here is the conversation
    ---------------------------------------------
    you: {previous_response}
    ---------------------------------------------
    customer: {user_input}
    ---------------------------------------------

    make your prediction based on the conversation above for the customer intention of his last response:
    ---------------------------------------------
    <your-prediction>
    ---------------------------------------------
    """
 
    response = requests.post(
        f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/{model}",
        headers={"Authorization": f"Bearer {api_token}"},
        json={"messages": [
            {"role": "system", "content": "follow the instructions and generate a text response to the prompt"},
            {"role": "user", "content": intent_prompt}
        ]}
    )

    inference = response.json()
    text = inference["result"]["response"]
    print(text)
    return text


def continue_conversation(user_input, intention):
    global main_prompt
    global previous_response

    main_prompt += user_input + "\n---------------------------------------------\nyou:"

    response = requests.post(
        f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/{model}",
        headers={"Authorization": f"Bearer {api_token}"},
        json={"messages": [
            {"role": "system", "content": "follow the instructions and generate a text response to the prompt"},
            {"role": "user", "content": main_prompt}
        ]}
    )

    text = response.json()["result"]["response"]
    previous_response = text
    main_prompt += previous_response + "\n---------------------------------------------\ncustomer:"
    print(text)
    return text