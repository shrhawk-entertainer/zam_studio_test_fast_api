import pytest


class TestPaymentProcessApi(object):
    """
    Tests for process-payment api
    """

    @pytest.fixture(scope='class')
    def api_url(self, app_):
        """
        Api url fixture.
        """
        return app_.url_path_for('payment_process_api')

    def test_without_basic_auth(self, client, api_url):
        """
        Test PaymentProcess api without basic auth.
        """

        response = client.post(api_url)
        assert response.status_code == 401

    def test_empty_params(self, client, api_url, basic_auth_header):
        """
        Test the PaymentProcess api without/empty params
        """
        response = client.post(api_url, json={}, headers=basic_auth_header)
        response_data = response.json()
        assert response.status_code == 400
        assert 'field required' in response_data['errors']['CreditCardNumber']
        assert 'field required' in response_data['errors']['CardHolder']

    def test_invalid_card_number(self, client, api_url, basic_auth_header):
        """
        Test the PaymentProcess api with invald card number
        """
        data = {
            'CreditCardNumber': '55555555555544441',
            'CardHolder': 'syed hassan raza',
            'ExpirationDate': '2021-12-12',
            'Amount': 12,
            'SecurityCode': 321
        }
        response = client.post(api_url, json=data, headers=basic_auth_header)
        response_data = response.json()

        assert response.status_code == 400
        assert 'card number is not valid' in response_data['errors']['CreditCardNumber']

    def test_valid_card_number(self, client, api_url, basic_auth_header):
        """
        Test the PaymentProcess api with valid card number
        """
        data = {
            'CreditCardNumber': '5555555555554444',
            'CardHolder': 'syed hassan raza',
            'ExpirationDate': '2021-12-12',
            'Amount': 12,
            'SecurityCode': 321
        }
        response = client.post(api_url, json=data, headers=basic_auth_header)
        response_data = response.json()
        assert response.status_code == 200
        assert response_data == "ok"

    def test_invalid_expiration_date(self, client, api_url, basic_auth_header):
        """
        Test the PaymentProcess api with ivalid expiration date
        """
        data = {
            'CreditCardNumber': '5555555555554444',
            'CardHolder': 'syed hassan raza',
            'ExpirationDate': '2012-121212',
            'Amount': 12,
            'SecurityCode': 321
        }
        response = client.post(api_url, json=data, headers=basic_auth_header)
        response_data = response.json()
        assert response.status_code == 400
        assert 'invalid date format' in response_data['errors']['ExpirationDate']

    def test_past_expiration_date(self, client, api_url, basic_auth_header):
        """
        Test the PaymentProcess api with past expiration date
        """
        data = {
            'CreditCardNumber': '5555555555554444',
            'CardHolder': 'syed hassan raza',
            'ExpirationDate': '2020-12-12',
            'Amount': 12,
            'SecurityCode': 321
        }
        response = client.post(api_url, json=data, headers=basic_auth_header)
        response_data = response.json()
        assert response.status_code == 400
        assert 'Invalid date must future date' in response_data['errors']['ExpirationDate']

    def test_invalid_amount(self, client, api_url, basic_auth_header):
        """
        Test the PaymentProcess api with invalid amount
        """
        data = {
            'CreditCardNumber': '5555555555554444',
            'CardHolder': 'syed hassan raza',
            'ExpirationDate': '2020-12-12',
            'Amount': -12,
            'SecurityCode': 321
        }
        response = client.post(api_url, json=data, headers=basic_auth_header)
        response_data = response.json()
        assert response.status_code == 400
        assert 'ensure this value is greater than 0' in response_data['errors']['Amount']

    def test_invalid_security_code(self, client, api_url, basic_auth_header):
        """
        Test the PaymentProcess api with invalid security code
        """
        data = {
            'CreditCardNumber': '5555555555554444',
            'CardHolder': 'syed hassan raza',
            'ExpirationDate': '2020-12-12',
            'Amount': -12,
            'SecurityCode': 'ab1'
        }
        response = client.post(api_url, json=data, headers=basic_auth_header)
        response_data = response.json()
        assert response.status_code == 400
        assert 'Invalid security code must be digits' in response_data['errors']['SecurityCode']

    def test_invalid_security_code_length(self, client, api_url, basic_auth_header):
        """
        Test the PaymentProcess api with invalid security code length
        """
        data = {
            'CreditCardNumber': '5555555555554444',
            'CardHolder': 'syed hassan raza',
            'ExpirationDate': '2020-12-12',
            'Amount': -12,
            'SecurityCode': '12345'
        }
        response = client.post(api_url, json=data, headers=basic_auth_header)
        response_data = response.json()
        assert response.status_code == 400
        assert 'Invalid security code length must be equal to 3' in response_data['errors']['SecurityCode']
