from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import User, Employee, Parent, EducationalProgram, Group
from .serializers import UserSerializer, EmployeeSerializer, ParentSerializer, EducationalProgramSerializer, GroupSerializer
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

    employee_serializer = EmployeeSerializer(data=employee_data, context={'user': user})
    if not employee_serializer.is_valid():
        transaction.set_rollback(True)
        return Response(employee_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    employee_serializer.save()

    return Response({'message': 'Сотрудник успешно добавлен'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def add_parent(request):
    # Проверка роли администратора
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

    parent_serializer.save()

    return Response({'message': 'Родитель успешно добавлен'}, status=status.HTTP_201_CREATED)

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
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_employee_by_user_id(request, user_id):
    employee = get_object_or_404(Employee, user__id=user_id)
    serializer = EmployeeSerializer(employee)
    return Response(serializer.data, status=status.HTTP_200_OK)

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