from rest_framework import serializers
from .models import User, Employee, Parent, Event,\
    EducationalProgram, Group, Child, MedicalContraindicationsChild, AssignedEmployees, ListParticipants

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
        fields = ['id', 'description', 'age_category_children']

class GroupSerializer(serializers.ModelSerializer):
    educational_program = EducationalProgramSerializer(read_only=True)
    class Meta:
        model = Group
        fields = ['id', 'name', 'age_group', 'count_children', 'educational_program']

class MedicalContraindicationsChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalContraindicationsChild
        fields = ['C', 'description', 'child']

class ChildSerializer(serializers.ModelSerializer):
    gender_display = serializers.SerializerMethodField()
    gender = serializers.BooleanField(write_only=True)
    medical_contraindications = MedicalContraindicationsChildSerializer(
        many=True, read_only=True, source='medicalcontraindicationschild_set'
    )
    group_name = serializers.ReadOnlyField(source='group.name')

    # добавляем связанных родителей, связанных через ParentsChilds
    parents = serializers.SerializerMethodField()

    class Meta:
        model = Child
        fields = ['id', 'fname', 'lname', 'patronymic', 'gender', 'gender_display', 'birthday',
                  'group', 'group_name', 'transfer_date', 'medical_contraindications', 'parents']

    def get_gender_display(self, obj):
        return "woman" if obj.gender else "man"

    def get_parents(self, obj):
        parents_qs = Parent.objects.filter(parentschilds__child=obj)
        return ParentSerializer(parents_qs, many=True).data

class AssignedEmployeesSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    group = GroupSerializer(read_only=True)

    class Meta:
        model = AssignedEmployees
        fields = ['group', 'employee', 'role']

class EventSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'name', 'date_event', 'employee', 'count_participants']
        read_only_fields = ['employee']

class ListParticipantsSerializer  (serializers.ModelSerializer):
    child = ChildSerializer(read_only=True)
    event = EventSerializer(read_only=True)
    class Meta:
        model = ListParticipants
        fields = ['id', 'event', 'child']