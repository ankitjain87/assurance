
import json
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Customer, Policy, PolicyStateHistory

class CustomerPolicyTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Create a customer for testing
        self.customer = Customer.objects.create(
            first_name="Ben",
            last_name="Stokes",
            dob="1991-06-25"  # Assuming this is in YYYY-MM-DD format
        )
        
        # Create policies for the customer
        self.policy1 = Policy.objects.create(
            customer=self.customer,
            policy_type="personal-accident",
            premium=200,
            cover=200000,
            state="new"
        )
        
        self.policy2 = Policy.objects.create(
            customer=self.customer,
            policy_type="life",
            premium=300,
            cover=500000,
            state="quoted"
        )

        # Create policy state history
        PolicyStateHistory.objects.create(
            policy=self.policy1,
            state="new"
        )
        PolicyStateHistory.objects.create(
            policy=self.policy1,
            state="bound"
        )

    def test_search_customer_by_name(self):
        response = self.client.get(reverse('customer_search'), {'name': 'Ben'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['first_name'], 'Ben')

    def test_search_customer_by_dob(self):
        response = self.client.get(reverse('customer_search'), {'dob': '25-06-1991'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['last_name'], 'Stokes')

    def test_search_customer_by_policy_type(self):
        response = self.client.get(reverse('customer_search'), {'policy_type': 'personal-accident'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['first_name'], 'Ben')

    def test_search_customer_with_no_results(self):
        response = self.client.get(reverse('customer_search'), {'name': 'Unknown'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_list_policies_for_customer(self):
        url = reverse('policy-list-list')
        response = self.client.get(url, {'customer_id': self.customer.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_policy_payment(self):
        url = reverse('quote-pay', kwargs={'pk': self.policy1.id})
        data = {'payment_method': 'credit_card'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.policy1.refresh_from_db()
        self.assertEqual(self.policy1.state, 'bound')

    def test_policy_history(self):
        url = reverse('policy_history', kwargs={'policy_id': self.policy1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['state'], 'bound')
        self.assertEqual(response.data[1]['state'], 'new')
