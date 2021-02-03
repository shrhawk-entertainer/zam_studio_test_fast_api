from datetime import date
from typing import Optional

from pydantic import BaseModel, PaymentCardNumber, PositiveFloat, errors, validator

from common.constants import INVALID_CARD_NUMBER_MESSAGE

errors.LuhnValidationError.msg_template = INVALID_CARD_NUMBER_MESSAGE


class PaymentRequest(BaseModel):
    CreditCardNumber: PaymentCardNumber
    CardHolder: str
    ExpirationDate: date
    SecurityCode: Optional[str] = ''
    Amount: PositiveFloat

    # class Config:
    #     error_msg_templates = {
    #         'value_error.payment_card_number.luhn_check': 'Invalid card number',
    #     }

    @validator('ExpirationDate')
    def expiration_future_date(cls, expiration_date):
        if expiration_date < date.today():
            raise ValueError('Invalid date must future date')
        return expiration_date

    @validator('SecurityCode')
    def security_code_length_and_type(cls, security_code):
        if not str(security_code).isdigit():
            raise ValueError('Invalid security code must be digits')
        if len(str(security_code)) != 3:
            raise ValueError('Invalid security code length must be equal to 3')
        return security_code
