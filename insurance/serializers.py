from rest_framework import serializers
from .models import Customer, Policy, PolicyStateHistory
from .utils import calculate_quote


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["id", "first_name", "last_name", "dob"]


class PolicySerializer(serializers.ModelSerializer):
    customer_id = serializers.IntegerField(write_only=True)
    customer = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Policy
        fields = [
            "id",
            "customer_id",
            "customer",
            "policy_type",
            "premium",
            "cover",
            "state",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        customer_id = validated_data.pop("customer_id")
        policy_type = validated_data.get("policy_type")

        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            raise serializers.ValidationError("Customer does not exist")

        premium, cover = calculate_quote(customer, policy_type)
        validated_data["premium"] = premium
        validated_data["cover"] = cover
        print(validated_data)
        policy = Policy.objects.create(customer=customer, **validated_data)
        policy_state_history = PolicyStateHistory.objects.create(policy=policy, state=policy.state)
        return policy


class PaymentSerializer(serializers.Serializer):
    payment_method = serializers.CharField(max_length=255)

    def validate_payment_method(self, value):
        if not value:
            raise serializers.ValidationError("Payment method required.")
        return value


class PolicyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = "__all__"


class PolicyStateHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PolicyStateHistory
        fields = ["id", "policy", "state", "updated_at"]
