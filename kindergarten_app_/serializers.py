from rest_framework import serializers
from .models import User, Employee, Parent

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['fname', 'lname', 'patronymic', 'gender', 'birthday',
                  'phone_number', 'qualification', 'work_experience']

    def create(self, validated_data):
        user = self.context.get('user')  # получаем user из контекста сериализатора
        if 'user' in validated_data:
            validated_data.pop('user')
        return Employee.objects.create(user=user, **validated_data)

class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = ['fname', 'lname', 'patronymic', 'phone_number']

    def create(self, validated_data):
        user = self.context.get('user')
        return Parent.objects.create(user=user, **validated_data)
