from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model 
class CarMake(models.Model):
    Name = models.CharField(null=False, max_length=30)
    Description = models.CharField(max_length=100)

    def __str__(self):
        return "Name: " + self.Name + "," + \
            "Description: " + self.Description
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object


# <HINT> Create a Car Model model 
class CarModel(models.Model):

    Types = [
        ('sedan', 'SEDAN'),
        ('suv', 'SUV'),
        ('wagon', 'WAGON')
    ]

    Car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    Name = models.CharField(null=False, max_length=30)
    Dealer_id = models.IntegerField()
    Type = models.CharField(null=False, max_length=30, choices=Types)
    Year = models.DateField()

    def __str__(self):
        return  "Car Make: " + self.Car_make + ", " + \
                "Name: " + self.Name + ", " \
                "Year: " + str(self.Year) + ", " + \
                "Dealer ID: " + self.Dealer_id + ", " + \
                "Type: " + self.Type
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object


# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
