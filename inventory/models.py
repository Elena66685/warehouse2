from django.db import models


class Employee(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя сотрудника")

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def __str__(self):
        return self.name


class OfficeSupply(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название канцтовара")

    class Meta:
        verbose_name = "Канцтовар"
        verbose_name_plural = "Канцтовары"

    def __str__(self):
        return self.name


class EmployeeSupply(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="Сотрудник")
    supply = models.ForeignKey(OfficeSupply, on_delete=models.CASCADE, verbose_name="Канцтовар")
    taken_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата выдачи")

    class Meta:
        verbose_name = "Выдача канцтовара"
        verbose_name_plural = "Выдачи канцтоваров"

    def __str__(self):
        return f"{self.employee} взял {self.supply}"
