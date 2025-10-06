from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Enum для квалификации сотрудников
class QualificationEmployees(models.TextChoices):
    TEACHER = 'Воспитатель детского сада'
    SENIOR_TEACHER = 'Старший воспитатель'
    METHODIST = 'Методист'
    MUSIC_DIRECTOR = 'Музыкальный руководитель'
    PSYCHOLOGIST = 'Педагог-психолог'
    SPEECH_THERAPIST = 'Логопед'
    DEFECTOLOGIST = 'Дефектолог'
    PE_TEACHER = 'Физкультурный руководитель'
    TEACHER_ASSISTANT = 'Помощник воспитателя'
    KINDERGARTEN_HEAD = 'Заведующий детским садом'

# Enum для возрастных групп
class AgeGroups(models.TextChoices):
    JUNIOR = 'Младшая'
    MIDDLE = 'Средняя'
    SENIOR = 'Старшая'

# Enum для ролей пользователей
class Roles(models.TextChoices):
    ADMIN = 'Admin'
    EMPLOYEE = 'Employee'
    PARENT = 'Parent'

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('Users must have a username')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)   # хеширование пароля
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    role = models.CharField(max_length=10, choices=Roles.choices)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.BigIntegerField(unique=True,
        validators=[MinValueValidator(80000000000), MaxValueValidator(89999999999)])

    def __str__(self):
        return f'{self.lname} {self.fname}'

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50, blank=True, null=True)
    gender = models.BooleanField()  # например, True = Мужчина, False = Женщина
    birthday = models.DateField()
    phone_number = models.BigIntegerField(unique=True,
        validators=[MinValueValidator(80000000000), MaxValueValidator(89999999999)])
    qualification = models.CharField(max_length=50, choices=QualificationEmployees.choices, unique=True)
    work_experience = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.lname} {self.fname}'

class EducationalProgram(models.Model):
    description = models.TextField()
    age_category_children = models.PositiveIntegerField()

    def __str__(self):
        return f'Программа {self.id}'

class Group(models.Model):
    name = models.CharField(max_length=50)
    age_group = models.CharField(max_length=10, choices=AgeGroups.choices)
    count_children = models.PositiveIntegerField(default=0)
    educational_program = models.ForeignKey(EducationalProgram, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Child(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50, blank=True, null=True)
    gender = models.BooleanField()  # True/False для пола.
    birthday = models.DateField()
    group = models.ForeignKey(Group, on_delete=models.PROTECT)  # нельзя удалить группу при наличии детей
    transfer_date = models.DateField()

    def __str__(self):
        return f'{self.lname} {self.fname}'

class ParentsChilds(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    child = models.ForeignKey(Child, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('parent', 'child')

class MedicalContraindicationsChild(models.Model):
    C = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    child = models.ForeignKey(Child, on_delete=models.CASCADE)

    def __str__(self):
        return self.C

class Event(models.Model):
    name = models.CharField(max_length=50, unique=True)
    date_event = models.DateTimeField()
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)
    count_participants = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class ListsEvents(models.Model):
    educational_program = models.ForeignKey(EducationalProgram, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('educational_program', 'event')

class AssignedEmployees(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=QualificationEmployees.choices)

    class Meta:
        unique_together = ('group', 'employee')

class ListParticipants(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    child = models.ForeignKey(Child, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('event', 'child')
