from openai import OpenAI
import os
from customizable_parameters import company_details, product_details, offers_available, additional_instructions
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(
    api_key= os.getenv("OPENAI_API_KEY")
)

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
    greeting = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=greeting_prompt,
        temperature=1,
        max_tokens=150,
        top_p=1,
    )

    previous_response = greeting.choices[0].text
    main_prompt = greeting_prompt + previous_response + "\n---------------------------------------------\ncustomer:"

    print(greeting.choices[0].text)
    return greeting.choices[0].text

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
 
    intention = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=intent_prompt,
        temperature=0.9,
        max_tokens=100,
        top_p=1,
    )

    print(intention.choices[0].text)
    return intention.choices[0].text

def continue_conversation(user_input, intention):
    global main_prompt
    global previous_response

    main_prompt += user_input + "\n---------------------------------------------\nyou:"

    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=main_prompt,
        temperature=0.9,
        max_tokens=100,
        top_p=1,
    )

    previous_response = response.choices[0].text
    main_prompt += previous_response + "\n---------------------------------------------\ncustomer:"
    print(response.choices[0].text)
    return response.choices[0].text