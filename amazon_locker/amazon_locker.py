from __future__ import annotations
from enum import Enum
from uuid import uuid4
from collections import deque
from typing import Dict

# Interviewer: An Amazon pickup location has various lockers for packages to be dropped off and picked up. We have both packages and lockers of varying sizes. 
# Model the lockers, packages, and pickup location and implement an algorithm to find the best possible empty locker for a given package efficiently.

# Start with Clarifying Questions
# A sample communication between a candidate and an interview can look like:

# What are the sizes for packages and lockers?
# Small, Medium, Large

# Can I assume that a package should go to the corresponding locker size?
# Yes

# What if there is no small locker left and a small package arrives?
# Good question, if there is no locker with matching size of the package, the package should go to the next locker size available (e.g. Small package goes inside of a medium locker)

# Nice, how many lockers from each size exist in the pickup location?
# It changes per pickup location. Your model should be able to handle that.

# Understood, what if a package arrives and there is no valid locker available?
# Your pickup location should not accept the package.

# What do you mean by finding an empty locker efficiently?
# Well, customers drop and pick up packages constantly. The lockers becomes full and empty constantly as well. Your code should be able to find an available locker very quickly.

class Size:
    SMALL = 1
    MEDIUM = 2
    LARGE = 3

class Package:
    def __init__(self, size: Size):
        self.size = size
        self.package_id = str(uuid4())

class Locker:
    def __init__(self, size: Size):
        self.size = size
        self.locker_id = str(uuid4())
        self.package = None

    def assign_package(self, package: Package):
        self.package = package

    def empty_locker(self):
        if not self.package:
            raise Exception("The locker is already empty.")
        
        package = self.package
        self.package = None
        return package
    
class PackageLocation:
    def __init__(self, locker_sizes: Dict[Size, int]):
        self.available_lockers = {size: deque() for size in Size}
        self.package_loc = {}
        for size, count in locker_sizes.items():
            for _ in range(count):
                self.available_lockers[size].append(Locker(size))

    def assign_package(self, package: Package):
        for locker_size in Size:
            if locker_size.value < package.size.value:
                continue

            locker = self._assign_locker(package, locker_size)
            if locker:
                return locker
        
        return None

    def _assign_locker(self, package: Package, size: Size):
        if not self.available_lockers[size]:
            return None
        locker = self.available_lockers[size].popleft()
        locker.assign_package(package)
        self.package_loc[package.package_id] = locker
        return locker

    def get_package(self, package: Package):
        if package.package_id not in self.package_loc:
            raise Exception("Package not in here.")
        
        locker = self.package_loc[package.package_id]
        package = locker.empty_locker()
        self.available_lockers[locker.size].append(locker)
        del self.package_loc[package.package_id]
        return package