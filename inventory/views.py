# inventory/views.py
from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Employee, OfficeSupply, EmployeeSupply
from .forms import EmployeeForm  # Импортируем форму


def index(request):
    """Первый интерфейс - форма добавления"""
    employees = Employee.objects.all()
    supplies = OfficeSupply.objects.all()
    form = EmployeeForm()  # Создаем пустую форму

    return render(request, 'index.html', {
        'employees': employees,
        'supplies': supplies,
        'form': form,  # Передаем форму в шаблон
    })


def add_employee(request):
    """Обработка формы добавления сотрудника"""
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()  # Сохраняем сотрудника в БД
            return redirect('index')  # Возвращаем на главную

    # Если форма не валидна или GET запрос
    employees = Employee.objects.all()
    supplies = OfficeSupply.objects.all()
    return render(request, 'index.html', {
        'employees': employees,
        'supplies': supplies,
        'form': EmployeeForm(request.POST) if request.method == 'POST' else EmployeeForm(),
    })


def add_record(request):
    """Добавление записи о выдаче (без изменений)"""
    if request.method == 'POST':
        employee_id = request.POST.get('employee')
        supply_ids = request.POST.getlist('supplies')

        if employee_id and supply_ids:
            employee = Employee.objects.get(id=employee_id)

            for supply_id in supply_ids:
                supply = OfficeSupply.objects.get(id=supply_id)
                EmployeeSupply.objects.create(employee=employee, supply=supply)

    return redirect('records')


def records(request):
    """Второй интерфейс - просмотр записей (без изменений)"""
    search_query = request.GET.get('search', '')

    if search_query:
        records_list = EmployeeSupply.objects.filter(
            Q(employee__name__icontains=search_query)
        )
    else:
        records_list = EmployeeSupply.objects.all()

    return render(request, 'records.html', {
        'records': records_list,
        'search_query': search_query
    })