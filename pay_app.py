from fastapi.exceptions import RequestValidationError
from fastapi import FastAPI, Request, Response
from pydantic import BaseModel
from typing import Dict, List
from math import floor
import dateutil.parser
import requests
import datetime

app = FastAPI()

app.payment_method = list()
app.payment_customer_method = list()
app.database = dict()


# validation handler - catches all requestValidationErrors
# return - Bad Response 400
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return Response(status_code=400)


# helpers functions
# checks if date is valid (with timezone)
# input: date as string
# returns: bool if is valid
def validate_iso(sval):
    try:
        valid_datetime = dateutil.parser.parse(sval)
        return True
    except ValueError:
        return False


# adds last transaction to database
# input: customer id as int
#       CustomerPaymentMethodResp
#       date as string
# returns: -
def add_to_database(customer_number, payment_customer_method, date):
    valid_datetime = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z")
    if customer_number in app.database:
        if valid_datetime > app.database[customer_number][0]:
            app.database[customer_number] = (valid_datetime, payment_customer_method)
    else:
        app.database[customer_number] = (valid_datetime, payment_customer_method)


# exchanges money
# input: currency_exchange as string
# returns: response from NBP
def exchange(currency_exchange):
    path_nbp = "http://api.nbp.pl/api/exchangerates/rates/a/"
    if currency_exchange.lower() == "pln":
        response = 1
    elif currency_exchange.lower() == "gbp" or currency_exchange.lower() == "usd" or currency_exchange.lower() == "eur":
        response = requests.get(path_nbp + currency_exchange + "/").json()['rates'][0]['mid']
    else:
        response = None
    return response


# masks card number
# input: card number as string
# returns: masked card number as string
def masked_card_number(card_number):
    if len(card_number) == 16:
        new_card_number = card_number[0:4] + "*" * 8 + card_number[12:16]
        return new_card_number


# creates valid payment mean
# input: payment method as string
#       parameters from request as JSON
# returns: payment mean as string
# throws KeyError when we have unknown payment method - we will catch it in request processing and return 400 response
def get_payment_mean(payment_method, numbers_dict):
    if payment_method == "pay_by_link":
        return numbers_dict["bank"]
    elif payment_method == "dp":
        return numbers_dict["iban"]
    elif payment_method == "card":
        return numbers_dict["cardholder_name"] + ' ' + numbers_dict["cardholde_surname"] + ' ' + masked_card_number(
            numbers_dict["card_number"])
    else:
        raise KeyError


class PaymentMethodRq(BaseModel):
    pay_by_link: List[Dict]
    dp: List[Dict]
    card: List[Dict]


# Models of responses and requests
class PaymentMethodResp(BaseModel):
    date: str
    type: str
    payment_mean: str
    description: str
    currency: str
    amount: int
    amount_in_pln: int


class CustomerPaymentMethodRq(BaseModel):
    customer_id: int
    pay_by_link: List[Dict]
    dp: List[Dict]
    card: List[Dict]


class CustomerPaymentMethodResp(BaseModel):
    customer_id: int
    date: str
    type: str
    payment_mean: str
    description: str
    currency: str
    amount: int
    amount_in_pln: int


# POST methods
@app.post('/report', response_model=List[PaymentMethodResp])
def payment_report(request: PaymentMethodRq):
    try:
        for key, value in request.dict().items():
            for numbers_dict in value:
                currency_exchange = exchange(numbers_dict["currency"])
                is_date = validate_iso(numbers_dict["created_at"])
                if currency_exchange is None or is_date is False:
                    return Response(status_code=400)
                app.payment_method.append(
                    PaymentMethodResp(date=numbers_dict["created_at"],
                                      type=key,
                                      payment_mean=get_payment_mean(key, numbers_dict),
                                      description=numbers_dict["description"],
                                      currency=numbers_dict["currency"],
                                      amount=numbers_dict["amount"],
                                      amount_in_pln=floor(numbers_dict["amount"] * currency_exchange)))
    except KeyError:
        return Response(status_code=400)
    return app.payment_method


@app.post('/customer-report', response_model=List[CustomerPaymentMethodResp])
def payment_customer_report(request: CustomerPaymentMethodRq):
    try:
        customer_number = request.dict()["customer_id"]
        for key, value in request.dict().items():
            if key == "customer_id":
                continue
            for numbers_dict in value:
                currency_exchange = exchange(numbers_dict["currency"])
                is_date = validate_iso(numbers_dict["created_at"])
                if currency_exchange is None or is_date is False:
                    return Response(status_code=400)
                payment_customer_method = CustomerPaymentMethodResp(customer_id=customer_number,
                                                                    date=numbers_dict["created_at"],
                                                                    type=key,
                                                                    payment_mean=get_payment_mean(key, numbers_dict),
                                                                    description=numbers_dict["description"],
                                                                    currency=numbers_dict["currency"],
                                                                    amount=numbers_dict["amount"],
                                                                    amount_in_pln=floor(
                                                                        numbers_dict["amount"] * currency_exchange))
                app.payment_customer_method.append(payment_customer_method)
                add_to_database(customer_number, payment_customer_method, numbers_dict["created_at"])
    except KeyError:
        return Response(status_code=400)
    return app.payment_customer_method


# GET methods
@app.get('/customer-report/{customer_identification}')
def number_customer_payment(customer_identification: int):
    if customer_identification in app.database:
        return app.database[customer_identification][1]
    else:
        return Response(status_code=204)
