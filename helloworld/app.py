import stripe
from chalice import Chalice
import json
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute
import os
import openai


app = Chalice(app_name='helloworld')


# Define user model
class User(Model):
    class Meta:
        table_name = 'users_table'
        region = 'us-east-1'

    username = UnicodeAttribute(hash_key=True)
    age = NumberAttribute()


if not User.exists():
    User.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)


# Customer Portal Route
@app.route("/customerportal", methods=["GET"])
def costumer_portal():
    stripe.api_key = os.environ["STRIPE_APIKEY"]

    print(stripe.billing_portal.Session.create(
        customer=os.environ["CUSTOMER"],
        return_url="https://google.com",
    ))


# Checkout Portal Route
@app.route("/checkout", methods=["GET"])
def checkout():
    stripe.api_key = os.environ["STRIPE_APIKEY"]

    return stripe.checkout.Session.create(
        success_url="https://google.com",
        line_items=[
            {
                "price": os.environ["PRICE"],
                "quantity": 1,
            },
        ],
        customer_email=os.environ["CUSTOMER_EMAIL"],
        mode="subscription",
    )


# Execution Portal Route
@app.route("/execution", methods=["POST"])
def execution():
    stripe.api_key = os.environ["STRIPE_APIKEY"]

    openai.api_key = os.environ["OPENAI_APIKEY"]
    body = app.current_request.json_body

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "You are a content manager from a blog, you are gonna edit the provided content based on an action and a condition"},
            {"role": "system",
             "content": "if the evaluated condition is False, you will return only 'False' and no more text or explanations"},
            {"role": "system",
             "content": "if the evaluated condition is True, you will perform the requested action into the provided content"},
            {"role": "user", "content": f"""
                condition: {body['condition']}
            """
            },
            {"role": "user", "content": f"""
                    action: {body['action']} 
                """
             },
            {"role": "user", "content": f"""
                content: {body['content']}
                """
             },

        ]
    )

    print(completion.choices[0].message)
    print(app.current_request.json_body)
    return completion.choices[0].message
