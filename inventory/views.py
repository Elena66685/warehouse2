# inventory/views.py
from django.shortcuts import render, redirect
from django.db.models import Q, Count
from .models import Employee, OfficeSupply, EmployeeSupply
from .forms import EmployeeForm


def index(request):
    """Первый интерфейс - форма добавления"""
    employees = Employee.objects.all()
    supplies = OfficeSupply.objects.all()
    form = EmployeeForm()

    return render(request, 'index.html', {
        'employees': employees,
        'supplies': supplies,
        'form': form,
    })


def add_employee(request):
    """Обработка формы добавления сотрудника"""
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')

    employees = Employee.objects.all()
    supplies = OfficeSupply.objects.all()
    return render(request, 'index.html', {
        'employees': employees,
        'supplies': supplies,
        'form': EmployeeForm(request.POST) if request.method == 'POST' else EmployeeForm(),
    })


def add_record(request):
    """Добавление записи о выдаче"""
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
    """Второй интерфейс - просмотр записей"""
    search_query = request.GET.get('search', '').strip()  # Убираем пробелы
    sort_by = request.GET.get('sort_by', '-taken_date')

    # Базовый запрос
    records_list = EmployeeSupply.objects.all()

    # Поиск
    if search_query:
        records_list = records_list.filter(
            Q(employee__name__icontains=search_query) |
            Q(supply__name__icontains=search_query)
        )

    # Сортировка
    records_list = records_list.order_by(sort_by)

    # Агрегирование
    total_records = records_list.count()
    supplies_count = records_list.values('supply').distinct().count()
    employees_count = records_list.values('employee').distinct().count()

    context = {
        'records': records_list,
        'search_query': search_query,
        'sort_by': sort_by,
        'total_records': total_records,
        'supplies_count': supplies_count,
        'employees_count': employees_count,
    }

    return render(request, 'records.html', context)


