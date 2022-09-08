from tabulate import tabulate
from math import floor

time_table = {
    "minutes": 1,
    "hours": 60,
    "workweeks": 40*60,
    "days": 24*60,
    "months": 24*60*30
}

def calculate_minutes(time_str: str) -> int:
    ar = time_str.split(" ")
    time = int(ar[0])
    form = ar[1]
    return time * time_table[form]

class LP_Item:
    def __init__(self, name, time, cost, revenue) -> None:
        self._name = name
        self._time = calculate_minutes(time)
        self._cost = cost
        self._rev = revenue
        self._prof = revenue - cost
    
    def __repr__(self):
        return f"""{self._name} can be built for ${self._cost} in {self._time} minutes resulting in ${self._rev} revenue."""

    @property
    def name(self):
        return self._name

    @property
    def cost(self):
        return self._cost
    
    @property
    def time(self):
        return self._time
    
    @property
    def revenue(self):
        return self._rev

class LP_Model:
    def __init__(self, item_a, item_b, cost_limit, time_limit) -> None:
        self._x = item_a
        self._y = item_b
        self._cost_limit = cost_limit
        self._time_limit = calculate_minutes(time_limit)
        print(f"Calculating maximal profits while building {self._x.name}s and {self._y.name}s")
        print(f"   under the constraints of ${self._cost_limit} max cost and {self._time_limit} minutes max time")
        print(self._x)
        print(self._y)
        print()

        x_bound, y_bound = self.find_boundaries()
        x, y = self.find_center_max()

        x_only_revenue = x_bound * self._x.revenue
        y_only_revenue = y_bound * self._y.revenue

        x_and_y_revenue = x * self._x.revenue + y * self._y.revenue
        x_and_y_cost = x * self._x.cost + y * self._y.cost
        x_and_y_profit  = x_and_y_revenue - x_and_y_cost

        table = tabulate(
            [
                [f"{self._x.name}s ({x_bound})", x_only_revenue, x_bound * self._x.cost, x_bound * (self._x.revenue - self._x.cost)],
                [f"{self._y.name}s ({y_bound})", y_only_revenue, y_bound * self._y.cost, y_bound * (self._y.revenue - self._y.cost)],
                [f"{self._x.name}s ({x}) + {self._y.name}s ({y})", x_and_y_revenue, x_and_y_cost, x_and_y_profit]
            ], 
            headers=["Method", "Revenue", "Cost", "Profit"]
        )

        print(table)


    def find_boundaries(self):
        x_time_bound = self._time_limit / self._x.time
        y_time_bound = self._time_limit / self._y.time

        x_cost_bound = self._cost_limit / self._x.cost
        y_cost_bound = self._cost_limit / self._y.cost

        x_bound = x_time_bound if x_time_bound < x_cost_bound else x_cost_bound
        y_bound = y_time_bound if y_time_bound < y_cost_bound else y_cost_bound

        return floor(x_bound), floor(y_bound)
    
    def find_center_max(self):
        x, y = self._x, self._y
        if x.time % x.cost == 0:
            mult = x.time/x.cost
            """
            multiply cost equation so that x's cancel out
                multiply cost of y and limiter
                solve for y
                    a = subtract ycost*mult from y.time
                    b = subtract cost_limit*mult from time_limit
                    y = b/a
            """
            a = y.cost * mult - y.time
            b = self._cost_limit * mult - self._time_limit
            y_val = b/a
            x_val = (self._cost_limit - y_val*y.cost)/x.cost

        elif y.time % y.cost == 0:
            mult = y.time/y.cost
            """
            multiply cost equation so that y's cancel out
                multiply cost of x and limiter
                solve for x
                    a = subtract xcost*mult from x.time
                    b = subtract cost_limit*mult from time_limit
                    x = b/a
            """
            a = x.cost * mult - x.time
            b = self._cost_limit * mult - self._time_limit
            x_val = b/a
            y_val = (self._cost_limit - x_val*x.cost)/y.cost

        elif x.cost % x.time == 0:
            mult = x.cost/x.time
            """
            multiply time equation so that x's cancel out
                multiply time of y and limiter
                solve for y
                    a = subtract ytime*mult from y.cost
                    b = subtract time_limit*mult from cost_limit
                    y = b/a
            """
            a = y.time * mult - y.cost
            b = self._time_limit * mult - self._cost_limit
            y_val = b/a
            x_val = (self._cost_limit - y_val*y.cost)/x.cost

        elif y.cost % y.time == 0:
            mult = y.cost/y.time
            """
            multiply time equation so that y's cancel out
                multiply time of x and limiter
                solve for x
                    a = subtract xtime*mult from x.cost
                    b = subtract time_limit*mult from cost_limit
                    y = b/a
            """
            a = y.time * mult - y.cost
            b = self._time_limit * mult - self._cost_limit
            x_val = b/a
            y_val = (self._cost_limit - x_val*x.cost)/y.cost

        return floor(x_val), floor(y_val)
