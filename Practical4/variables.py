# Pseudocode:
# 1. Define variables to store Scotland's population in 2004/2014/2024
# 2. Calculate population change between 2004-2014 and 2014-2024
# 3. Compare values, add comments to explain if Scotland's population growth is accelerating or slowing
# 4. Define boolean variables X/Y, calculate W = X or Y, write complete truth table comments
# 5. Test all combinations of X/Y values to verify consistency with truth table

# Store Scotland's population data
a = 5.08 
b = 5.33 
c = 5.55

# Calculate population change 
d = b - a  
e = c - b 

# Compare d and e, add growth trend comment
print(f"Population change 2004-2014 (d): {d} million")
print(f"Population change 2014-2024 (e): {e} million")
print(f"Result of d > e: {d > e}")
# d=0.25, e=0.22, e < d → Scotland's population growth rate is slowing down

# Boolean value operation and truth table verification
X = True
Y = False
W = X or Y

# Print initial combination result
print(f"\nInitial combination: X={X}, Y={Y} → W={W}")

# Test all 4 combinations of X/Y, verify truth table
combinations = [(True, True),(True, False),(False, True),(False, False)]

print("\nW value verification for all X/Y combinations (Truth Table):")
for x_val, y_val in combinations:
    w_val = x_val or y_val
    print(f"X={x_val}, Y={y_val} → W={w_val}")

# Truth Table for W = X or Y:
# X=True, Y=True → W=True
# X=True, Y=False → W=True
# X=False, Y=True → W=True
# X=False, Y=False → W=False
# "OR" operation returns True if at least one operand is True; only False when both are False