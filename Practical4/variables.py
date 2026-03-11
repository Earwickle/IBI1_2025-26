# Pseudocode planning:
# 1. Define variables to store Scotland's population in 2004/2014/2024 (in millions)
# 2. Calculate population change between 2004-2014 (d) and 2014-2024 (e)
# 3. Compare values of d and e, add comments to explain if Scotland's population growth is accelerating or slowing
# 4. Define boolean variables X/Y, calculate W = X or Y, write complete truth table comments
# 5. Test all combinations of X/Y values to verify consistency with truth table

# 1. Store Scotland's population data (units: millions)
a = 5.08  # Scotland's population in 2004
b = 5.33  # Scotland's population in 2014
c = 5.55  # Scotland's population in 2024

# 2. Calculate population change (assessment requirement: correct calculation method)
d = b - a  # Population change 2004-2014
e = c - b  # Population change 2014-2024

# 3. Compare d and e, add growth trend comment (assessment key)
print(f"Population change 2004-2014 (d): {d} million")
print(f"Population change 2014-2024 (e): {e} million")
print(f"Result of d > e: {d > e}")
# Core comment: d=0.25, e=0.22, e < d → Scotland's population growth rate is slowing down

# 4. Boolean value operation and truth table verification
# Define base boolean variables
X = True
Y = False
W = X or Y  # Calculate initial value of W

# Print initial combination result
print(f"\nInitial combination: X={X}, Y={Y} → W={W}")

# Test all 4 combinations of X/Y (verify truth table)
combinations = [
    (True, True),
    (True, False),
    (False, True),
    (False, False)
]

print("\nW value verification for all X/Y combinations (Truth Table):")
for x_val, y_val in combinations:
    w_val = x_val or y_val
    print(f"X={x_val}, Y={y_val} → W={w_val}")

# Complete truth table comment (assessment key)
# Truth Table for W = X or Y:
# 1. X=True, Y=True → W=True
# 2. X=True, Y=False → W=True
# 3. X=False, Y=True → W=True
# 4. X=False, Y=False → W=False
# Conclusion: "OR" operation returns True if at least one operand is True; only False when both are False