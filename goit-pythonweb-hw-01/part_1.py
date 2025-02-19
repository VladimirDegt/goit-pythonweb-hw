import logging
from abc import ABC, abstractmethod

logging.basicConfig(level=logging.INFO)


class Vehicle(ABC):
    """
    Abstract base class for vehicles.

    Attributes:
        make (str): The make of the vehicle.
        model (str): The model of the vehicle.
        region (str): The region specification of the vehicle.
    """

    def __init__(self, make: str, model: str, region: str) -> None:
        self.make = make
        self.model = model
        self.region = region

    @abstractmethod
    def start_engine(self) -> None:
        """Starts the engine of the vehicle."""
        pass


class Car(Vehicle):
    def start_engine(self) -> None:
        """Starts the engine of the car."""
        logging.info(f"{self.make} {self.model} ({self.region} Spec): Двигун запущено")


class Motorcycle(Vehicle):
    def start_engine(self) -> None:
        """Starts the engine of the motorcycle."""
        logging.info(f"{self.make} {self.model} ({self.region} Spec): Мотор заведено")


class VehicleFactory(ABC):
    """
    Abstract factory for creating vehicles.
    """

    @abstractmethod
    def create_car(self, make: str, model: str) -> Car:
        """Creates a car."""
        pass

    @abstractmethod
    def create_motorcycle(self, make: str, model: str) -> Motorcycle:
        """Creates a motorcycle."""
        pass


class USVehicleFactory(VehicleFactory):
    def create_car(self, make: str, model: str) -> Car:
        """Creates a car for the US market."""
        return Car(make, model, "US")

    def create_motorcycle(self, make: str, model: str) -> Motorcycle:
        """Creates a motorcycle for the US market."""
        return Motorcycle(make, model, "US")


class EUVehicleFactory(VehicleFactory):
    def create_car(self, make: str, model: str) -> Car:
        """Creates a car for the EU market."""
        return Car(make, model, "EU")

    def create_motorcycle(self, make: str, model: str) -> Motorcycle:
        """Creates a motorcycle for the EU market."""
        return Motorcycle(make, model, "EU")


us_factory = USVehicleFactory()
eu_factory = EUVehicleFactory()

vehicle1 = us_factory.create_car("Ford", "Mustang")
vehicle1.start_engine()

vehicle2 = eu_factory.create_motorcycle("BMW", "R1250")
vehicle2.start_engine()
