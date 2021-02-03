from fastapi import Response

from apis.api_v1.payment_process_api.validation import PaymentRequest
from common.online_transactions import OnlineTransaction


async def payment_process_api(payment_details: PaymentRequest, response: Response):
    transaction_flow = OnlineTransaction(
        payment_details.CreditCardNumber,
        payment_details.CardHolder,
        payment_details.ExpirationDate,
        payment_details.Amount,
        security_code=payment_details.SecurityCode
    )
    result = transaction_flow.make_transaction()
    response.status_code = result['status_code']
    return result['data']
