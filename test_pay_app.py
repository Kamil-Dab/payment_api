from fastapi.testclient import TestClient

from pay_app import app

client = TestClient(app)


def test_payment_report():
    response = client.post("/report", json={
        "pay_by_link": [
            {
                "created_at": "2021-05-13T01:01:43-08:00",
                "currency": "EUR",
                "amount": 3000,
                "description": "Abonament na siłownię",
                "bank": "mbank"
            }
        ],
        "dp": [
            {
                "created_at": "2021-05-14T08:27:09Z",
                "currency": "USD",
                "amount": 599,
                "description": "FastFood",
                "iban": "DE91100000000123456789"
            }
        ],
        "card": [
            {
                "created_at": "2021-05-13T09:00:05+02:00",
                "currency": "PLN",
                "amount": 2450,
                "description": "REF123457",
                "cardholder_name": "John",
                "cardholde_surname": "Doe",
                "card_number": "2222222222222222"
            },
            {
                "created_at": "2021-05-14T18:32:26Z",
                "currency": "GBP",
                "amount": 1000,
                "description": "REF123456",
                "cardholder_name": "John",
                "cardholde_surname": "Doe",
                "card_number": "1111111111111111"
            },
        ]
    })
    assert response.status_code == 200
    assert response.json() == [
        {
            "date": "2021-05-13T01:01:43-08:00",
            "type": "pay_by_link",
            "payment_mean": "mbank",
            "description": "Abonament na siłownię",
            "currency": "EUR",
            "amount": 3000,
            "amount_in_pln": 13487
        },
        {
            "date": "2021-05-14T08:27:09Z",
            "type": "dp",
            "payment_mean": "DE91100000000123456789",
            "description": "FastFood",
            "currency": "USD",
            "amount": 599,
            "amount_in_pln": 2203
        },
        {
            "date": "2021-05-13T09:00:05+02:00",
            "type": "card",
            "payment_mean": "John Doe 2222********2222",
            "description": "REF123457",
            "currency": "PLN",
            "amount": 2450,
            "amount_in_pln": 2450
        },
        {
            "date": "2021-05-14T18:32:26Z",
            "type": "card",
            "payment_mean": "John Doe 1111********1111",
            "description": "REF123456",
            "currency": "GBP",
            "amount": 1000,
            "amount_in_pln": 5224
        }
    ]


def test_payment_report_currency():
    response_currency = client.post("/report", json={
        "pay_by_link": [
            {
                "created_at": "2021-05-13T01:01:43-08:00",
                "currency": "YEN",
                "amount": 3000,
                "description": "Abonament na siłownię",
                "bank": "mbank"
            }
        ],
        "dp": [
            {
                "created_at": "2021-05-14T08:27:09Z",
                "currency": "COS",
                "amount": 599,
                "description": "FastFood",
                "iban": "DE91100000000123456789"
            }
        ],
        "card": [
            {
                "created_at": "2021-05-13T09:00:05+02:00",
                "currency": 1234,
                "amount": 2450,
                "description": "REF123457",
                "cardholder_name": "John",
                "cardholde_surname": "Doe",
                "card_number": "2222222222222222"
            },
            {
                "created_at": "2021-05-14T18:32:26Z",
                "currency": "KW@!",
                "amount": 1000,
                "description": "REF123456",
                "cardholder_name": "John",
                "cardholde_surname": "Doe",
                "card_number": "1111111111111111"
            },
        ]
    })
    assert response_currency.status_code == 400


def test_payment_dikt():
    response = client.post("/report", json={
        "pay_bqwqweqy_link": [
            {
                "created_at": "2021-05-13T01:01:43-08:00",
                "currency": "EUR",
                "amount": 3000,
                "description": "Abonament na siłownię",
                "bank": "mbank"
            }
        ],
        "qwedp": [
            {
                "created_at": "2021-05-14T08:27:09Z",
                "currency": "USD",
                "amount": 599,
                "description": "FastFood",
                "iban": "DE91100000000123456789"
            }
        ],
        "carqweqd": [
            {
                "created_at": "2021-05-13T09:00:05+02:00",
                "currency": "PLN",
                "amount": 2450,
                "description": "REF123457",
                "cardholder_name": "John",
                "cardholde_surname": "Doe",
                "card_number": "2222222222222222"
            },
            {
                "created_at": "2021-05-14T18:32:26Z",
                "currency": "GBP",
                "amount": 1000,
                "description": "REF123456",
                "cardholder_name": "John",
                "cardholde_surname": "Doe",
                "card_number": "1111111111111111"
            },
        ]
    })
    assert response.status_code == 400


def test_payment_wrong_dikt():
    response = client.post("/report", json={
        1231231: "2131"
    })
    assert response.status_code == 400


def test_payment_report_date():
    response = client.post("/report", json={
        "pay_by_link": [
            {
                "created_at": "132412132",
                "currency": "EUR",
                "amount": 3000,
                "description": "Abonament na siłownię",
                "bank": "mbank"
            }
        ],
        "dp": [
            {
                "created_at": "2021-05-14T08:27:09Z",
                "currency": "USD",
                "amount": 599,
                "description": "FastFood",
                "iban": "DE91100000000123456789"
            }
        ],
        "card": [
            {
                "created_at": "2021-05-13T09:00:05+02:00",
                "currency": "PLN",
                "amount": 2450,
                "description": "REF123457",
                "cardholder_name": "John",
                "cardholde_surname": "Doe",
                "card_number": "2222222222222222"
            },
            {
                "created_at": "2021-05-14T18:32:26Z",
                "currency": "GBP",
                "amount": 1000,
                "description": "REF123456",
                "cardholder_name": "John",
                "cardholde_surname": "Doe",
                "card_number": "1111111111111111"
            },
        ]
    })
    assert response.status_code == 400


def test_customer_payment_report():
    response = client.post('/customer-report', json={
        "customer_id": 123,
        "pay_by_link": [
            {
                "created_at": "2021-05-13T01:01:43-08:00",
                "currency": "EUR",
                "amount": 3000,
                "description": "Abonament na siłownię",
                "bank": "mbank",
            }
        ],
        "dp": [
            {
                "created_at": "2021-05-14T08:27:09Z",
                "currency": "USD",
                "amount": 599,
                "description": "FastFood",
                "iban": "DE91100000000123456789",
            }
        ],
        "card": [
            {
                "created_at": "2021-05-14T18:32:26Z",
                "currency": "PLN",
                "amount": 2450,
                "description": "REF123457",
                "cardholder_name": "John",
                "cardholde_surname": "Doe",
                "card_number": "2222222222222222",
            },
            {
                "created_at": "2021-05-13T09:00:05+02:00",
                "currency": "GBP",
                "amount": 1000,
                "description": "REF123456",
                "cardholder_name": "John",
                "cardholde_surname": "Doe",
                "card_number": "1111111111111111",
            },
        ]
    })
    assert response.status_code == 200
    assert response.json() == [
        {
            "customer_id": 123,
            "date": "2021-05-13T01:01:43-08:00",
            "type": "pay_by_link",
            "payment_mean": "mbank",
            "description": "Abonament na siłownię",
            "currency": "EUR",
            "amount": 3000,
            "amount_in_pln": 13487
        },
        {
            "customer_id": 123,
            "date": "2021-05-14T08:27:09Z",
            "type": "dp",
            "payment_mean": "DE91100000000123456789",
            "description": "FastFood",
            "currency": "USD",
            "amount": 599,
            "amount_in_pln": 2203
        },
        {
            "customer_id": 123,
            "date": "2021-05-14T18:32:26Z",
            "type": "card",
            "payment_mean": "John Doe 2222********2222",
            "description": "REF123457",
            "currency": "PLN",
            "amount": 2450,
            "amount_in_pln": 2450
        },
        {
            "customer_id": 123,
            "date": "2021-05-13T09:00:05+02:00",
            "type": "card",
            "payment_mean": "John Doe 1111********1111",
            "description": "REF123456",
            "currency": "GBP",
            "amount": 1000,
            "amount_in_pln": 5224
        }
    ]
    response = client.get('/customer-report/123/')
    assert response.status_code == 200
    assert response.json() =={
            "customer_id": 123,
            "date": "2021-05-14T18:32:26Z",
            "type": "card",
            "payment_mean": "John Doe 2222********2222",
            "description": "REF123457",
            "currency": "PLN",
            "amount": 2450,
            "amount_in_pln": 2450
        }
