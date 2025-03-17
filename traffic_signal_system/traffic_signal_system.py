import __future__ as annotations
import threading
from enum import Enum
import time

class Signal(Enum):
    RED = 1
    YELLOW = 2
    GREEN = 3

class TrafficLight:
    def __init__(self, id: int, red_duration: int, yellow_duration: int, green_duration: int):
        self.id = id
        self.red_duration = red_duration
        self.yellow_duration = yellow_duration
        self.green_duration = green_duration
        self.current_signal = Signal.RED
        self.lock = threading.Lock()

    def change_signal(self, new_signal: Signal):
        with self.lock:
            self.current_signal = new_signal

    def get_current_signal(self):
        return self.current_signal

class Road:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.traffic_light = None

    def set_traffic_light(self, traffic_light: TrafficLight):
        self.traffic_light = traffic_light

    def get_traffic_light(self):
        return self.traffic_light

    def get_id(self):
        return self.id
    
class TrafficController:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.roads = {}
        return cls._instance
    
    @classmethod
    def get_instance(cls):
        return cls()
    
    def add_road(self, road: Road):
        self.roads[road.get_id()] = road

    def remove_road(self, road: Road):
        if road not in self.roads:
            raise Exception("Road not found")
        
        del self.roads[road.get_id()]

    def start_traffic_control(self):
        for road in self.roads.values():
            traffic_light = road.get_traffic_light()
            threading.Thread(target=self._control_traffic_light, args=(traffic_light,), daemon=True).start()

    def _control_traffic_light(self, traffic_light: TrafficLight):
        while True:
            try:
                time.sleep(traffic_light.red_duration / 1000)
                traffic_light.change_signal(Signal.GREEN)
                time.sleep(traffic_light.yellow_duration / 1000)
                traffic_light.change_signal(Signal.YELLOW)
                time.sleep(traffic_light.red_duration / 1000)
                traffic_light.change_signal(Signal.RED)
            except:
                print("An error occurred while controlling traffic light")

    def handle_emergency(self, road_id: int):
        road = self.roads[road_id]

        if road:
            traffic_light = road.get_traffic_light()
            traffic_light.change_signal(Signal.RED)

class TrafficSignalSystemDemo:
    @staticmethod
    def run():
        traffic_controller = TrafficController.get_instance()

        road1 = Road(1, "Main Street")
        road2 = Road(2, "Queen Street")
        road3 = Road(3, "King Street")
        road4 = Road(4, "Park Avenue")

        traffic_light1 = TrafficLight(1, 30000, 5000, 30000)
        traffic_light2 = TrafficLight(2, 30000, 5000, 30000)
        traffic_light3 = TrafficLight(3, 30000, 5000, 30000)
        traffic_light4 = TrafficLight(4, 30000, 5000, 30000)

        road1.set_traffic_light(traffic_light1)
        road2.set_traffic_light(traffic_light2)
        road3.set_traffic_light(traffic_light3)
        road4.set_traffic_light(traffic_light4)

        traffic_controller.add_road(road1)
        traffic_controller.add_road(road2)
        traffic_controller.add_road(road3)
        traffic_controller.add_road(road4)

        traffic_controller.start_traffic_control()

        traffic_controller.handle_emergency(2)

if __name__ == "__main__":
    TrafficSignalSystemDemo.run()