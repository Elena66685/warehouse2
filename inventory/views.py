from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Employee, OfficeSupply, EmployeeSupply


def index(request):
    """Первый интерфейс - форма добавления"""
    employees = Employee.objects.all()
    supplies = OfficeSupply.objects.all()

    return render(request, 'index.html', {
        'employees': employees,
        'supplies': supplies
    })


def add_record(request):
    """Добавление записи о выдаче"""
    if request.method == 'POST':
        employee_id = request.POST.get('employee')
        supply_ids = request.POST.getlist('supplies')  # Множественный выбор

        if employee_id and supply_ids:
            employee = Employee.objects.get(id=employee_id)

            for supply_id in supply_ids:
                supply = OfficeSupply.objects.get(id=supply_id)
                EmployeeSupply.objects.create(employee=employee, supply=supply)

    return redirect('records')


def records(request):
    """Второй интерфейс - просмотр записей"""
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
