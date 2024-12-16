from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import Expense
from .serializers import ExpenseSerializer
from django.utils.dateparse import parse_date
from django.db.models import Sum

class ExpenseViewSet(ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    @swagger_auto_schema(
        operation_description="Filter expenses by start_date and end_date.",
        manual_parameters=[
            openapi.Parameter('start_date', openapi.IN_QUERY, description="Start date in format YYYY-MM-DD", type=openapi.TYPE_STRING),
            openapi.Parameter('end_date', openapi.IN_QUERY, description="End date in format YYYY-MM-DD", type=openapi.TYPE_STRING),
        ],
        responses={
            200: ExpenseSerializer(many=True),
            400: "Invalid parameters",
        }
    )
    @action(detail=False, methods=['get'])
    def filter_by_date(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not start_date or not end_date:
            return Response(
                {"error": "Both start_date and end_date parameters are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            expenses = self.queryset.filter(
                date__range=[parse_date(start_date), parse_date(end_date)]
            )
            serializer = self.get_serializer(expenses, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Summarize expenses by category for a specific month and year.",
        manual_parameters=[
            openapi.Parameter('year', openapi.IN_QUERY, description="Year in format YYYY", type=openapi.TYPE_INTEGER),
            openapi.Parameter('month', openapi.IN_QUERY, description="Month in format MM", type=openapi.TYPE_INTEGER),
        ],
        responses={
            200: openapi.Response(
                description="Summary of expenses by category",
                examples={
                    "application/json": [
                        {"category": "Food", "total": 120.50},
                        {"category": "Travel", "total": 85.00}
                    ]
                }
            ),
            400: "Invalid parameters"
        }
    )
    @action(detail=False, methods=['get'])
    def summary_by_category(self, request):
        month = request.query_params.get('month')
        year = request.query_params.get('year')

        if not month or not year:
            return Response(
                {"error": "Both month and year parameters are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            expenses = self.queryset.filter(date__year=year, date__month=month)
            summary = expenses.values('category').annotate(total=Sum('amount'))
            return Response(summary)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)