import time
from enum import Enum
from threading import Lock, Condition, Thread
from collections import deque
import math

# The elevator system should consist of multiple elevators serving multiple floors.
# Each elevator should have a capacity limit and should not exceed it.
# Users should be able to request an elevator from any floor and select a destination floor.
# The elevator system should efficiently handle user requests and optimize the movement of elevators to minimize waiting time.
# The system should prioritize requests based on the direction of travel and the proximity of the elevators to the requested floor.
# The elevators should be able to handle multiple requests concurrently and process them in an optimal order.
# The system should ensure thread safety and prevent race conditions when multiple threads interact with the elevators.

class Elevator:
    def __init__(self, id, capacity):
        self.id = id
        self.capacity = capacity
        self.current_floor = 1
        self.current_direction = Direction.UP
        self.requests = deque()
        self.lock = Lock()
        self.condition = Condition(self.lock)

    def add_request(self, request):
        with self.lock:
            if len(self.requests) < self.capacity:
                self.requests.append(request)
                print(f"Elevator {self.id} added request: {request.source_floor} to {request.destination_floor}")
                self.condition.notify()

    def get_next_request(self):
        with self.lock:
            while not self.requests:
                self.condition.wait()

            return self.requests.popleft()
        
    def process_requests(self):
        while True:
            request = self.get_next_request()
            self.process_request(request)

    def process_request(self, request):
        start_floor = self.current_floor
        end_floor = request.destination_floor

        if start_floor < end_floor:
            self.current_direction = Direction.UP
            for floor in range(start_floor, end_floor + 1):
                self.current_floor = floor
                print(f"Elevator {self.id} reached floor {self.current_floor}")
                time.sleep(1)
        else:
            self.current_direction = Direction.DOWN
            for floor in range(start_floor, end_floor - 1, -1):
                self.current_floor = floor
                print(f"Elevator {self.id} reached floor {self.current_floor}")
                time.sleep(1)

    def run(self):
        self.process_requests()


class ElevatorController:
    def __init__(self, num_elevators, capacity):
        self.elevators = []
        for i in range(num_elevators):
            elevator = Elevator(i + 1, capacity)
            self.elevators.append(elevator)
            Thread(target=elevator.run).start()

    def request_elevator(self, source_floor, destination_floor):
        optimal_elevator = self.find_optimal_elevator(source_floor, destination_floor)
        optimal_elevator.add_request(Request(source_floor, destination_floor))


    def find_optimal_elevator(self, source_floor, destination_floor):
        optimal_elevator = None
        min_distance = math.inf

        for elevator in self.elevators:
            distance = abs(elevator.current_floor - source_floor)
            if distance < min_distance:
                optimal_elevator = elevator
                min_distance = distance

        return optimal_elevator


class Direction(Enum):
    UP = 1
    DOWN = -1


class Request:
    def __init__(self, source_floor, destination_floor):
        self.source_floor = source_floor
        self.destination_floor = destination_floor

class ElevatorSystemDemo:
    @staticmethod
    def run():
        controller = ElevatorController(3, 5)
        time.sleep(3)
        controller.request_elevator(10, 12)
        time.sleep(3)
        controller.request_elevator(1, 7)
        time.sleep(3)
        controller.request_elevator(2, 5)
        time.sleep(3)
        controller.request_elevator(1, 9)

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Elevator system stopped")

if __name__ == "__main__":
    ElevatorSystemDemo.run()