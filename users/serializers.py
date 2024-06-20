from rest_framework.serializers import ModelSerializer

from users.models import User, Payment


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class UserSerializer(ModelSerializer):
    payment_history = PaymentSerializer(source='user_payment', many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'

    def get_payment_history(self, instance):
        return PaymentSerializer(instance.payment_history, many=True).data