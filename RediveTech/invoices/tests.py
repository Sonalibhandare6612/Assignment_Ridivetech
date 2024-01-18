from django.test import TestCase

# Create your tests here.
# test cases
# invoices/tests.py

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Invoice, InvoiceDetail
from datetime import date

class InvoiceAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create test data
        self.invoice_data = {'date': date.today(), 'customer_name': 'Test Customer'}
        self.invoice = Invoice.objects.create(**self.invoice_data)

        self.detail_data = {'description': 'Test Item', 'quantity': 2, 'unit_price': 10.0, 'price': 20.0}
        self.detail = InvoiceDetail.objects.create(invoice=self.invoice, **self.detail_data)

    def test_create_invoice(self):
        response = self.client.post('/invoices/', self.invoice_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Invoice.objects.count(), 2)

    def test_retrieve_invoice(self):
        response = self.client.get(f'/invoices/{self.invoice.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['customer_name'], self.invoice_data['customer_name'])

    def test_update_invoice(self):
        updated_data = {'customer_name': 'Updated Customer'}
        response = self.client.put(f'/invoices/{self.invoice.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Invoice.objects.get(id=self.invoice.id).customer_name, updated_data['customer_name'])

    def test_delete_invoice(self):
        response = self.client.delete(f'/invoices/{self.invoice.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Invoice.objects.count(), 0)

    def test_create_invoice_detail(self):
        detail_data = {'description': 'New Item', 'quantity': 3, 'unit_price': 15.0, 'price': 45.0}
        response = self.client.post(f'/invoices/{self.invoice.id}/details/', detail_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(InvoiceDetail.objects.count(), 2)

    def test_retrieve_invoice_detail(self):
        response = self.client.get(f'/invoices/{self.invoice.id}/details/{self.detail.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], self.detail_data['description'])

    def test_update_invoice_detail(self):
        updated_data = {'description': 'Updated Item'}
        response = self.client.put(f'/invoices/{self.invoice.id}/details/{self.detail.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(InvoiceDetail.objects.get(id=self.detail.id).description, updated_data['description'])

    def test_delete_invoice_detail(self):
        response = self.client.delete(f'/invoices/{self.invoice.id}/details/{self.detail.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(InvoiceDetail.objects.count(), 0)
