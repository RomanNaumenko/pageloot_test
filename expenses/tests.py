from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Expense

class ExpenseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
        )
        self.expense_data = {
            "user": self.user,
            "title": "Test Expense",
            "amount": 100.50,
            "date": "2024-12-14",
            "category": "Food",
        }
        self.expense = Expense.objects.create(**self.expense_data)
        self.expenses_url = "/expenses/"

    def test_create_expense(self):
        data = {
            "user": self.user.id,
            "title": "New Expense",
            "amount": 200.00,
            "date": "2024-12-15",
            "category": "Travel"
        }
        response = self.client.post("/expenses/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_expense(self):
        response = self.client.get(self.expenses_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_expense(self):
        update_data = {
            "user": self.user.id,
            "title": "Updated Expense",
            "amount": 150.00,
            "date": "2024-12-16",
            "category": "Travel"
        }
        response = self.client.put(f"/expenses/{self.expense.id}/", update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.expense.refresh_from_db()
        self.assertEqual(self.expense.title, "Updated Expense")

    def test_delete_expense(self):
        response = self.client.delete(f"{self.expenses_url}{self.expense.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Expense.objects.count(), 0)

    def test_filter_by_date(self):
        url = f"{self.expenses_url}filter_by_date/?start_date=2024-12-01&end_date=2024-12-31"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_summary_by_category(self):
        url = f"{self.expenses_url}summary_by_category/?year=2024&month=12"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["category"], "Food")
        self.assertEqual(float(response.data[0]["total"]), 100.50)

    def test_create_expense_invalid_data(self):
        invalid_data = {
            "user": self.user.id,
            "title": "",
            "amount": -10,
            "date": "invalid-date",
            "category": "Unknown"
        }
        response = self.client.post(self.expenses_url, invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)
        self.assertIn("amount", response.data)
        self.assertIn("date", response.data)
        self.assertIn("category", response.data)

