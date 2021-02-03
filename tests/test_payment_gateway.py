import datetime

import asynctest
import pytest

from common.online_transactions import OnlineTransaction


class TestPaymentGateWay(object):
    """
    Tests for Payment-GateWays
    """

    @pytest.mark.asyncio
    async def test_cheap_payment_gateway(self):
        """
        Test cheap payment gateway response.
        """
        transaction_flow = OnlineTransaction(
            '5555555555554444',
            'syed hassan raza',
            datetime.datetime(2021, 12, 12),
            12,
            security_code=321
        )
        result = await transaction_flow.make_transaction()
        assert result['status_code'] == 200
        assert result['data'] == 'ok'

    @pytest.mark.asyncio
    @asynctest.patch('common.online_transactions.CheapPaymentGateway.make_transaction')
    async def test_cheap_payment_gateway_using_function_calling(self, make_transaction):
        """
        Test cheap payment gateway called with their own class make_transaction function
        """
        transaction_flow = OnlineTransaction(
            '5555555555554444',
            'syed hassan raza',
            datetime.datetime(2021, 12, 12),
            12,
            security_code=321
        )
        await transaction_flow.make_transaction()
        make_transaction.assert_called_once()

    @pytest.mark.asyncio
    async def test_premium_payment_gateway(self):
        """
        Test premium payment gateway response.
        """
        transaction_flow = OnlineTransaction(
            '5555555555554444',
            'syed hassan raza',
            datetime.datetime(2021, 12, 12),
            521,  # premium amount
            security_code=321
        )
        result = await transaction_flow.make_transaction()
        assert result['status_code'] == 200
        assert result['data'] == 'ok'

    @pytest.mark.asyncio
    @asynctest.patch('common.online_transactions.PremiumPaymentGateway.make_transaction')
    async def test_premium_payment_gateway_using_function_calling(self, make_transaction):
        """
        Test premium payment gateway called with their own class make_transaction function
        """
        transaction_flow = OnlineTransaction(
            '5555555555554444',
            'syed hassan raza',
            datetime.datetime(2021, 12, 12),
            521,  # premium amount
            security_code=321
        )
        await transaction_flow.make_transaction()
        make_transaction.assert_called_once()

    @pytest.mark.asyncio
    @asynctest.patch('common.online_transactions.make_request', side_effect=[
        {'data': 'ok', 'status_code': 200}, {'data': 'ok', 'status_code': 200}
    ])
    async def test_premium_payment_gateway_retries(self, make_request):
        """
        Test premium payment gateway with retries
        """
        transaction_flow = OnlineTransaction(
            '5555555555554444',
            'syed hassan raza',
            datetime.datetime(2021, 12, 12),
            521,  # premium amount
            security_code=321
        )
        await transaction_flow.make_transaction()
        #  second call with transaction call contains retries
        args, kwargs = make_request.call_args_list[1]
        assert kwargs['retries'] == 3

    @pytest.mark.asyncio
    async def test_expensive_payment_gateway(self):
        """
        Test expensive payment gateway response.
        """
        transaction_flow = OnlineTransaction(
            '5555555555554444',
            'syed hassan raza',
            datetime.datetime(2021, 12, 12),
            450,  # expensive amount
            security_code=321
        )
        result = await transaction_flow.make_transaction()
        assert result['status_code'] == 200
        assert result['data'] == 'ok'

    @pytest.mark.asyncio
    @asynctest.patch('common.online_transactions.ExpensivePaymentGateway.make_transaction')
    async def test_expensive_payment_gateway_using_function_calling(self, make_transaction):
        """
        Test expensive payment gateway called with their own class make_transaction function
        """
        transaction_flow = OnlineTransaction(
            '5555555555554444',
            'syed hassan raza',
            datetime.datetime(2021, 12, 12),
            450,  # expensive amount
            security_code=321
        )
        await transaction_flow.make_transaction()
        make_transaction.assert_called_once()

    @pytest.mark.asyncio
    @asynctest.patch('common.online_transactions.make_request', side_effect=[
        {'data': 'ok', 'status_code': 500}, {'data': 'ok', 'status_code': 200}, {'data': 'ok', 'status_code': 200}
    ])
    @asynctest.patch('common.online_transactions.CheapPaymentGateway.make_transaction', side_effect=[
        {'data': 'ok', 'status_code': 200}
    ])
    async def test_expensive_payment_failure(self, make_transaction, make_request):
        """
        Test expensive payment gateway failure with cheap payment gateway
        first side effect will throw failure that expensive_payment is unavailable and move to cheap payment gateway
        """
        transaction_flow = OnlineTransaction(
            '5555555555554444',
            'syed hassan raza',
            datetime.datetime(2021, 12, 12),
            450,  # expensive amount
            security_code=321
        )
        result = await transaction_flow.make_transaction()
        make_transaction.assert_called_once()
        assert result['status_code'] == 200
        assert result['data'] == 'ok'
