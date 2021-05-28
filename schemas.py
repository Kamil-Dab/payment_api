from pydantic import BaseMode


# Models of responses and requests
class PaymentMethodRq(BaseModel):
    pay_by_link: List[Dict]
    dp: List[Dict]
    card: List[Dict]


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
