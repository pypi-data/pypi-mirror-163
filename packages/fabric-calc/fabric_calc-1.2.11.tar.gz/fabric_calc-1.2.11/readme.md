# Fabric Calc

List of rectangle, a rectangle is a tuple of two ints, (length, width)
```python

from fabric_calc.fabric_calc import calculate 

# length, width, quantity
rectangles = [
            (30, 40, 5),
            (55, 36, 4),
            (33, 16,1),
            (20, 36,6),
        ]
print(calculate(rectangles))

```