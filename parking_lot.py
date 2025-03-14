from __future__ import annotations
from enum import Enum
from abc import ABC, abstractmethod
from typing import List

# The parking lot should have multiple levels, each level with a certain number of parking spots.
# The parking lot should support different types of vehicles, such as cars, motorcycles, and trucks.
# Each parking spot should be able to accommodate a specific type of vehicle.
# The system should assign a parking spot to a vehicle upon entry and release it when the vehicle exits.
# The system should track the availability of parking spots and provide real-time information to customers.
# The system should handle multiple entry and exit points and support concurrent access.

class ParkingLot:
    _instance = None

    def __init__(self):
        if ParkingLot._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            ParkingLot._instance = self
            self.levels: List[Level] = []

    @staticmethod
    def get_instance():
        if ParkingLot._instance is None:
            ParkingLot()
        return ParkingLot._instance
    
    def add_level(self, level: Level):
        self.levels.append(level)

    def park_vehicle(self, vehicle: Vehicle) -> bool:
        for level in self.levels:
            if level.park_vehicle(vehicle):
                return True
            
        return False
    
    def unpark_vehicle(self, vehicle: Vehicle) -> bool:
        for level in self.levels:
            if level.unpark_vehicle(vehicle):
                return True
            
        return False
    
    def display_availability(self) -> None:
        for level in self.levels:
            level.display_availability()


class Level:
    def __init__(self, floor: int, total_spots: int):
        self.floor = floor
        self.parking_spots: List[ParkingSpot] = [ParkingSpot(i) for i in range(total_spots)]

    def park_vehicle(self, vehicle: Vehicle) -> bool:
        for spot in self.parking_spots:
            if spot.is_available():
                spot.park_vehicle(vehicle)
                return True
            
        return False
    
    def unpark_vehicle(self, vehicle: Vehicle) -> bool:
        for spot in self.parking_spots:
            if not spot.is_available() and spot.get_parked_vehicle() == vehicle:
                spot.unpark_vehicle()
                return True
            
        return False
    
    def display_availability(self) -> None:
        print(f"Level {self.floor} Availability:")
        for spot in self.parking_spots:
            print(f"Spot {spot.get_spot_number()}: {'Available' if spot.is_available() else 'Occupoied'}")


class ParkingSpot:
    def __init__(self, spot_number: int):
        self.spot_number = spot_number
        self.vehicle_type = None
        self.is_occupied = False
        self.parked_vehicle = None

    def is_available(self):
        return not self.is_occupied
    
    def park_vehicle(self, vehicle: Vehicle):
        if self.is_available():
            self.is_occupied = True
            self.vehicle_type = vehicle.get_vehicle_type()
            self.parked_vehicle = vehicle
        else:
            raise Exception("Parking spot is not available")
        
    def unpark_vehicle(self):
        if self.is_available():
            raise Exception("Parking spot is already available")
        
        self.is_occupied = False
        self.vehicle_type = None

    def get_parking_spot_vehicle_type(self):
        return self.vehicle_type

    def get_parked_vehicle(self):
        return self.parked_vehicle
    
    def get_spot_number(self):
        return self.spot_number


class VehicleType(Enum):
    CAR = 1
    MOTORCYCLE = 2
    TRUCK = 3


class Vehicle(ABC):
    def __init__(self, plate_number: str, vehicle_type: VehicleType):
        self.plate_number = plate_number
        self.vehicle_type = vehicle_type

    def get_vehicle_type(self):
        return self.vehicle_type
    

class Car(Vehicle):
    def __init__(self, plate_number: str):
        super().__init__(plate_number, VehicleType.CAR)


class Motorcycle(Vehicle):
    def __init__(self, plate_number: str):
        super().__init__(plate_number, VehicleType.MOTORCYCLE)


class Truck(Vehicle):
    def __init__(self, plate_number: str):
        super().__init__(plate_number, VehicleType.TRUCK)


class Test:
    def run():
        parking_lot = ParkingLot.get_instance()
        parking_lot.add_level(Level(1, 3))
        parking_lot.add_level(Level(2, 3))

        car = Car("ABC123")
        motorcycle = Motorcycle("DEF456")
        truck = Truck("GHI789")

        parking_lot.park_vehicle(car)
        parking_lot.park_vehicle(motorcycle)
        parking_lot.park_vehicle(truck)

        print(f"After parking car, motorcycle, and truck:")

        parking_lot.display_availability()

        parking_lot.unpark_vehicle(motorcycle)

        print(f"After unparking motorcycle:")

        parking_lot.display_availability()

if __name__ == "__main__":
    Test.run()