from rest_framework import serializers
from .models import User, Employee, Parent, EducationalProgram, Group

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
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    gender = serializers.BooleanField(write_only=True)  # Принимается при создании/обновлении, но не выводится
    gender_display = serializers.SerializerMethodField(read_only=True)  # Выводится только для чтения

    class Meta:
        model = Employee
        fields = ['id', 'user_id', 'fname', 'lname', 'patronymic', 'gender', 'gender_display',
                  'birthday', 'phone_number', 'qualification', 'work_experience']

    def get_gender_display(self, obj):
        return "woman" if obj.gender else "man"

class ParentSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    class Meta:
        model = Parent
        fields = ['id', 'user_id', 'fname', 'lname', 'patronymic', 'phone_number']

    def create(self, validated_data):
        user = self.context.get('user')
        return Parent.objects.create(user=user, **validated_data)

class EducationalProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationalProgram
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'