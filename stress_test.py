import random

from locust import HttpLocust, TaskSequence, seq_task
from pyquery import PyQuery


class DonorBehaviour(TaskSequence):
    # Default host to use, override with --host on the command line
    host = 'http://localhost:8000'

    def __init__(self, parent):
        super().__init__(parent)
        self.donation_payload = {
            'email': 'test@example.com',
            'first_name': 'firstname',
            'last_name': 'lastname',
            'address_line_1': '123 Fake Street',
            'post_code': 'M5V1T5',
            'town': 'Toronto',
            'country': 'CA',
            'amount': 50,
            'landing_url': 'https://donate-wagtail-staging.herokuapp.com/en-US/',
            'project': 'mozillafoundation',
            'campaign_id': 'testing-a-donation',
            # https://developers.braintreepayments.com/reference/general/testing/python#nonces-representing-cards
            'braintree_nonce': 'fake-valid-nonce'
        }
        self.donation_params = {
            'currency': 'usd',
            'source_page_id': 3,
            'amount': 50
        }

    @seq_task(1)
    def load_donate_form(self):
        resp = self.client.get('/en-CA/')

    @seq_task(2)
    def load_payment_information_form(self):
        resp = self.client.get(f'/en-US/card/single/', params=self.donation_params)
        pq = PyQuery(resp.content)
        self.donation_payload['csrfmiddlewaretoken'] = pq('input[name=csrfmiddlewaretoken]').val()

    @seq_task(3)
    def make_payment(self):
        resp = self.client.post('/en-US/card/single/', params=self.donation_params, data=self.donation_payload)


class DonorUser(HttpLocust):
    task_set = DonorBehaviour
    # exponentially distributed wait time between actions, avg 15 seconds
    wait_function = lambda self: random.expovariate(1) * 2000
