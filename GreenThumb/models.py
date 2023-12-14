from django.db import models


# Create a model for Sample Market Segments
class Companysector(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Create a model for Employee Count
class EmployeeCount(models.Model):
    count = models.CharField(max_length=10)

    def __str__(self):
        return self.count


# Create a model for Annual Electricity Budget
class ElectricityBudget(models.Model):
    budget = models.CharField(max_length=20)

    def __str__(self):
        return self.budget


# Create a model for Annual Natural Gas Budget
class NaturalGasBudget(models.Model):
    budget = models.CharField(max_length=20)

    def __str__(self):
        return self.budget


# Update the Company model to use ForeignKey for each criteria
class Company(models.Model):
    company_name = models.CharField(max_length=100)
    Email_ID = models.EmailField(max_length=100)
    postal_code = models.CharField(max_length=10)
    employee_count = models.ForeignKey(
        'EmployeeCount',
        on_delete=models.DO_NOTHING,
        null=True,
        related_name='companies_by_employee_count'
    )
    annual_electricity_budget = models.ForeignKey(
        'ElectricityBudget',
        on_delete=models.DO_NOTHING,
        null=True,
        related_name='companies_by_electricity_budget'
    )


    company_sector = models.ForeignKey(
        'Companysector',
        on_delete=models.DO_NOTHING,
        null=True,
        related_name='companies_by_sector'
    )
    annual_natural_gas_budget = models.ForeignKey(
        'NaturalGasBudget',
        on_delete=models.DO_NOTHING,
        null=True,
        related_name='companies_by_gas_budget'
    )

    def __str__(self):
        return self.company_name

class Program(models.Model):
        program_name = models.TextField()
        link = models.URLField(default='https://example.com')

        supporting_docs = models.JSONField(default=list) # Use TextField to store links as a string
        description = models.TextField()
        eligible_employee_count = models.ManyToManyField(
            'EmployeeCount',
            related_name='programs_by_employee_count'
        )
        eligible_annual_electricity_budget = models.ManyToManyField(
            'ElectricityBudget',
            related_name='programs_by_electricity_budget'
        )
        eligible_company_sector = models.ManyToManyField(
        'Companysector',
        related_name='programs_to_sector',
        )
        eligible_annual_natural_gas_budget = models.ManyToManyField(
            'NaturalGasBudget',
            related_name='programs_by_gas_budget'
        )

        def __str__(self):
            return self.program_name



class Feedback(models.Model):
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Below Average'),
        (3, '3 - Average'),
        (4, '4 - Good'),
        (5, '5 - Excellent'),
    ]

    rating = models.IntegerField(choices=RATING_CHOICES)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Rating: {self.rating}"