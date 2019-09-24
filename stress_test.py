import random
import urllib.parse

from locust import HttpLocust, TaskSet, seq_task
from pyquery import PyQuery


class DonorBehaviour(TaskSet):
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
            'landing_url': 'https://donate-wagtail-staging.herokuapp.com/en-CA/',
            'project': 'mozillafoundation',
            'campaign_id': ''
        }

    # Default host to use, override with --host on the command line
    host = 'http://localhost:8000'

    @seq_task(1)
    def load_donate_form(self):
        resp = self.client.get('/en-CA/')

    @seq_task(2)
    def load_payment_information_form(self):
        resp = self.client.get(f'/en-CA/card/single/?source_page_id={self.d_source_page_id}&currency={self.d_currency}'
                               f'&amount={self.d_amount}')
        pq = PyQuery(resp.content)
        self.donation_payload['csrfmiddlewaretoken'] = pq('input[name=csrfmiddlewaretoken]').val()
        self.donation_payload['braintree_nonce'] = pq('input#id_braintree_nonce').val()

    @seq_task(3)
    def make_payment(self):
        headers = {'content-type': 'application/x-www-form-encoded'}
        resp = self.client.post('/en-US/card/single', data=self.donation_payload, headers=headers)


class DonorUser(HttpLocust):
    task_set = DonorBehaviour
    # exponentially distributed wait time between actions, avg 15 seconds
    wait_function = lambda self: random.expovariate(1) * 15000
