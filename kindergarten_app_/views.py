from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import User, Employee, Parent, EducationalProgram, Group, Child, ParentsChilds
from .serializers import UserSerializer, EmployeeSerializer,  \
    ParentSerializer, EducationalProgramSerializer, GroupSerializer, ChildSerializer, MedicalContraindicationsChildSerializer
from django.shortcuts import get_object_or_404

@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# views.py
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def add_employee(request):
    if request.user.role != 'Admin':
        return Response({'error': 'Доступ запрещён, требуется роль администратора'}, status=status.HTTP_403_FORBIDDEN)

    user_data = request.data.get('user')
    employee_data = request.data.get('employee')

    user_serializer = UserSerializer(data=user_data)
    if not user_serializer.is_valid():
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    user = user_serializer.save()

    employee_serializer = EmployeeSerializer(data=employee_data)
    if not employee_serializer.is_valid():
        transaction.set_rollback(True)
        return Response(employee_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    employee = employee_serializer.save(user=user)

    result_serializer = EmployeeSerializer(employee)
    return Response(result_serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def add_parent(request):
    if request.user.role != 'Admin':
        return Response({'error': 'Доступ запрещён, требуется роль администратора'}, status=status.HTTP_403_FORBIDDEN)

    user_data = request.data.get('user')
    parent_data = request.data.get('parent')

    user_serializer = UserSerializer(data=user_data)
    if not user_serializer.is_valid():
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    user = user_serializer.save()

    parent_serializer = ParentSerializer(data=parent_data, context={'user': user})
    if not parent_serializer.is_valid():
        transaction.set_rollback(True)
        return Response(parent_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    parent = parent_serializer.save()

    # Сериализуем и возвращаем данные добавленного родителя
    output_serializer = ParentSerializer(parent)
    return Response(output_serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_parents(request):
    if request.user.role != 'Admin':
        return Response({'error': 'Доступ запрещён, требуется роль администратора'}, status=status.HTTP_403_FORBIDDEN)

    parents = Parent.objects.all()
    serializer = ParentSerializer(parents, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_employees(request):
    # Разрешаем доступ для ролей Admin или Employee
    if request.user.role not in ['Admin', 'Employee']:
        return Response({'error': 'Доступ запрещён'}, status=status.HTTP_403_FORBIDDEN)

    employees = Employee.objects.all()
    serializer = EmployeeSerializer(employees, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_parent_by_user_id(request, user_id):
    if request.user.role not in ['Admin', 'Employee']:
        return Response({'error': 'Доступ запрещён'}, status=status.HTTP_403_FORBIDDEN)

    parent = get_object_or_404(Parent, user__id=user_id)
    serializer = ParentSerializer(parent)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def edit_parent(request, parent_id):
    if request.user.role != 'Admin':
        return Response({'error': 'Доступ запрещён. Только администраторы могут редактировать родителя.'}, status=status.HTTP_403_FORBIDDEN)

    parent = get_object_or_404(Parent, id=parent_id)
    partial = request.method == 'PATCH'
    serializer = ParentSerializer(parent, data=request.data, partial=partial)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_employee_by_user_id(request, user_id):
    employee = get_object_or_404(Employee, user__id=user_id)
    serializer = EmployeeSerializer(employee)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def edit_employee(request, employee_id):
    if request.user.role != 'Admin':
        return Response({'error': 'Доступ запрещён. Только администраторы могут редактировать данные сотрудников.'}, status=status.HTTP_403_FORBIDDEN)

    employee = get_object_or_404(Employee, id=employee_id)
    partial = request.method == 'PATCH'
    serializer = EmployeeSerializer(employee, data=request.data, partial=partial)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_educational_program(request):
    if request.user.role != 'Employee':
        return Response({'error': 'Доступ запрещён. Только сотрудник может создавать программы.'}, status=status.HTTP_403_FORBIDDEN)

    serializer = EducationalProgramSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_educational_program_by_id(request, program_id):
    program = get_object_or_404(EducationalProgram, id=program_id)
    serializer = EducationalProgramSerializer(program)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_group(request):
    if request.user.role != 'Admin':
        return Response({'error': 'Доступ запрещён. Только администраторы могут создавать группы.'}, status=status.HTTP_403_FORBIDDEN)

    serializer = GroupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_groups(request):
    if request.user.role not in ['Admin', 'Employee']:
        return Response({'error': 'Доступ запрещен'}, status=status.HTTP_403_FORBIDDEN)

    groups = Group.objects.all()
    serializer = GroupSerializer(groups, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_group_by_id(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    serializer = GroupSerializer(group)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def edit_group(request, group_id):
    if request.user.role != 'Admin':
        return Response({'error': 'Доступ запрещён. Только администраторы могут редактировать группы.'}, status=status.HTTP_403_FORBIDDEN)

    group = get_object_or_404(Group, id=group_id)
    partial = request.method == 'PATCH'  # Позволяет частичное обновление
    serializer = GroupSerializer(group, data=request.data, partial=partial)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def add_child(request):
    if request.user.role != 'Admin':
        return Response({'error': 'Доступ запрещён, требуется роль администратора'}, status=status.HTTP_403_FORBIDDEN)

    child_data = request.data.get('child')
    contraindications_data = request.data.get('medical_contraindications', [])
    parent_id = request.data.get('parent_id')

    if not parent_id:
        return Response({'error': 'parent_id обязателен'}, status=status.HTTP_400_BAD_REQUEST)

    child_serializer = ChildSerializer(data=child_data)
    if not child_serializer.is_valid():
        return Response(child_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    child = child_serializer.save()

    # Связываем с родителем
    try:
        parent = Parent.objects.get(id=parent_id)
    except Parent.DoesNotExist:
        return Response({'error': 'Родитель с таким id не найден'}, status=status.HTTP_400_BAD_REQUEST)

    # Проверяем, что такая связь уникальна, либо создаём новую
    ParentsChilds.objects.get_or_create(parent=parent, child=child)

    # Сохраняем медицинские противопоказания если переданы
    for contraindication_data in contraindications_data:
        contraindication_data['child'] = child.id  # Связываем противопоказание с ребенком
        contraindication_serializer = MedicalContraindicationsChildSerializer(data=contraindication_data)
        if contraindication_serializer.is_valid():
            contraindication_serializer.save()
        else:
            transaction.set_rollback(True)
            return Response(contraindication_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    output_serializer = ChildSerializer(child)
    return Response(output_serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_child(request, child_id):
    if request.user.role not in ['Admin', 'Employee']:
        return Response({'error': 'Доступ запрещён'}, status=status.HTTP_403_FORBIDDEN)

    child = get_object_or_404(Child, id=child_id)
    serializer = ChildSerializer(child)
    return Response(serializer.data)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def edit_child(request, child_id):
    if request.user.role != 'Admin':
        return Response({'error': 'Доступ запрещён'}, status=status.HTTP_403_FORBIDDEN)

    child = get_object_or_404(Child, id=child_id)

    partial = request.method == 'PATCH'  # поддержка частичного обновления

    serializer = ChildSerializer(child, data=request.data, partial=partial)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
