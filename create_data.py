import os
import sys
import django

# настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'warehouse2.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from inventory.models import Employee, OfficeSupply, EmployeeSupply


def clear_data():
    #Очистка всех данных
    EmployeeSupply.objects.all().delete()
    Employee.objects.all().delete()
    OfficeSupply.objects.all().delete()
    print("Старые данные удалены")


def create_data():
    print("Создание тестовых данных...")

    # Создаем сотрудников
    employees = [
        "Иванов Иван",
        "Петрова Мария",
        "Сидоров Алексей",
        "Козлова Анна",
        "Тутина Елена",
        "Костин Максим",
        "Румянцев Игорь",
        "Бочева Инга",
        "Воеводин Станислав"
    ]

    employee_objects = {}
    for name in employees:
        obj, created = Employee.objects.get_or_create(name=name)
        employee_objects[name] = obj
        status = "создан" if created else "уже существует"
        print(f"  Сотрудник: {name} - {status}")

    # создаем канцтовары
    supplies = [
        "Ручка шариковая",
        "Блокнот А4",
        "Карандаш",
        "Степлер",
        "Скрепки",
        "Клей-карандаш",
        "Линейка",
        "Ножницы"
    ]

    supply_objects = {}
    for name in supplies:
        obj, created = OfficeSupply.objects.get_or_create(name=name)
        supply_objects[name] = obj
        status = "создан" if created else "уже существует"
        print(f"  Канцтовар: {name} - {status}")

    # создаем записи о выдаче
    issuances = [
        ("Иванов Иван", ["Ручка шариковая", "Блокнот А4", "Карандаш"]),
        ("Петрова Мария", ["Степлер", "Скрепки", "Линейка"]),
        ("Сидоров Алексей", ["Ручка шариковая", "Ножницы"]),
        ("Козлова Анна", ["Клей-карандаш", "Блокнот А4"]),
    ]

    for emp_name, supply_names in issuances:
        employee = employee_objects[emp_name]
        for supply_name in supply_names:
            supply = supply_objects[supply_name]
            EmployeeSupply.objects.get_or_create(
                employee=employee,
                supply=supply
            )
        print(f"  {emp_name} взял: {', '.join(supply_names)}")

    # статистика
    print("\nСтатистика:")
    print(f"  Всего сотрудников: {Employee.objects.count()}")
    print(f"  Всего канцтоваров: {OfficeSupply.objects.count()}")
    print(f"  Всего выдач: {EmployeeSupply.objects.count()}")
    print("\nТестовые данные успешно созданы!")


if __name__ == "__main__":
    # Спросим пользователя
    response = input("Очистить старые данные? (y/n): ").strip().lower()
    if response == 'y':
        clear_data()

    create_data()

    # Проверим работу
    print("\nПроверка данных:")
    from django.db.models import Count

    for emp in Employee.objects.all():
        count = EmployeeSupply.objects.filter(employee=emp).count()
        supplies = EmployeeSupply.objects.filter(employee=emp)
        supply_names = [es.supply.name for es in supplies]
        print(f"  {emp.name}: {count} выдач ({', '.join(supply_names[:3])}...)")