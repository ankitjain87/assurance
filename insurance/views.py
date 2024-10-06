from datetime import datetime

from django.contrib.auth.models import Group, User
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Customer, Policy, PolicyStateHistory

from .serializers import (
    CustomerSerializer,
    PolicySerializer,
    PolicyStateHistorySerializer,
    PaymentSerializer,
)


class CustomerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows customers to be created, viewed, edited, searched.
    """

    queryset = Customer.objects.all().order_by("-created_at")
    serializer_class = CustomerSerializer

    @action(detail=False, methods=["get"], url_path="search")
    def search(self, request):
        """
        Search customers by name, date of birth and policy type.
        """

        name = request.query_params.get("name", None)
        dob = request.query_params.get("dob", None)
        policy_type = request.query_params.get("policy_type", None)

        filters = Q()
        if name:
            filters &= Q(first_name__icontains=name) | Q(last_name__icontains=name)
        if dob:
            try:
                filters &= Q(dob=datetime.strptime(dob, "%d-%m-%Y").date())
            except ValueError:
                return Response(
                    {"error": "Invalid date format. Please use dd-mm-yyyy."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        customers = Customer.objects.filter(filters).distinct()
        if policy_type:
            for customer in customers:
                policies = Policy.objects.filter(customer=customer)
                if not policies.filter(policy_type__iexact=policy_type).exists():
                    customers = customers.exclude(id=customer.id)

        serializer = self.get_serializer(customers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PolicyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows policies to be created, viewed or edited.
    """

    queryset = Policy.objects.all().order_by("-created_at")
    serializer_class = PolicySerializer

    def create(self, request):
        """
        Create a quote for a customer.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=True, methods=["put"], url_path="pay")
    def pay(self, request, *args, **kwargs):
        """
        Process payment for a policy, once paid the policy is bound.
        """
        try:
            policy = self.get_object()
        except Policy.DoesNotExist:
            return Response(
                {"error": "Policy not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            payment_method = serializer.validated_data.get("payment_method")

            policy.state = "bound"
            policy.save()
            return Response(
                {"message": "Payment is successfully processed"},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PolicyListViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows policies to be viewed.
    """

    queryset = Policy.objects.all().order_by("-created_at")
    serializer_class = PolicySerializer

    def list(self, request):
        """
        List policies for a customer.
        """
        customer_id = request.query_params.get("customer_id", None)

        if not customer_id:
            return Response(
                {"error": "Customer ID is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        customer = Customer.objects.get(id=customer_id)
        if not customer:
            return Response({"error": "Customer not found"}, status=status.HTTP_400)

        try:
            policies = Policy.objects.filter(customer_id=customer_id)
            serializer = self.get_serializer(policies, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Policy.DoesNotExist:
            return Response(
                {"error": "No policies found for the provided customer ID."},
                status=status.HTTP_404_NOT_FOUND,
            )

    @action(detail=True, methods=["get"], url_path="history")
    def history(self, request, pk=None):
        """
        Get the history of a policy/quote.
        """
        policy = self.get_object()
        if not policy:
            return Response({"error": "Policy not found"}, status=status.HTTP_400)

        history = PolicyStateHistory.objects.filter(policy=policy).order_by(
            "-updated_at"
        )
        serializer = PolicyStateHistorySerializer(history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

