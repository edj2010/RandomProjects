# Dice Grid Team Game
# Grid looks as follows
#
#     +-------------+------------------+----------------+----------------+-----------------------+
# 1:1 | sum > 52    | # even > 3       | min > 3        | median > 11    | # prime > # composite |
#     +-------------+------------------+----------------+----------------+-----------------------+
# 1:2 | duplicate # | prod % 8<>0      | prod % 128 = 0 | sum < 46       | max - min < 12        |
#     +-------------+------------------+----------------+----------------+-----------------------+
# 1:3 | max = 18    | max * min > 120  | # cubes >= 2   | max < 15       | min = 5               |
#     +-------------+------------------+----------------+----------------+-----------------------+
# 1:5 | all odd     | sum in [60, 65]  | no primes      | # squares >= 3 | sum in [47, 50]       |
#     +-------------+------------------+----------------+----------------+-----------------------+
#
# Note: order matters because people are distinct:
# 2, 4 has same p as 3, 3 and same as 4, 2

def choose(n,k):
    top = 1
    bot = 1
    for i in range(k):
        top *= (n - i)
        bot *= (i + 1)
    return top / bot

MIN_ROLL = 1
MAX_ROLL = 20 # prime list below needs updating if this is changed
NUM_STATES = MAX_ROLL - MIN_ROLL + 1

C_SE = dict()
def count_sumEquals(n, total):
    if n == 1:
        return 1 if MIN_ROLL <= total <= MAX_ROLL else 0
    
    if (n, total) in C_SE:
        return C_SE[(n, total)]
    
    C_SE[(n, total)] = sum(count_sumEquals(n - 1, total - i)
                            for i in range(MIN_ROLL, min(MAX_ROLL, total) + 1))
    
    return C_SE[(n, total)]

def p_sumInRange(n, low, high): #inclusive
    return sum(count_sumEquals(n, s)
                for s in range(low, high+1))

def p_binDistInRange(n, p, low, high):
    return sum(choose(n, i)*pow(p, i)*pow(1 - p, n - i)
                for i in range(low, high+1))

### Only needs to be computed once, so done here    
pow_count = [NUM_STATES]
base = 2
while base < NUM_STATES:
    next_pow = MAX_ROLL // base - MIN_ROLL // base
    pow_count[-1] -= next_pow
    pow_count.append(next_pow)
    base *= 2
###

def p_prod2CountInRange(c, low, high):
    if high < 0:
        return 0
    if c == 0:
        return low <= 0
    total = 0
    for i, num_occ in enumerate(pow_count):
        total += p_prod2CountInRange(c - 1, low - i, high - i)*num_occ/NUM_STATES
    return total

def p_deltaMinMaxRange(n, roll, high):
    lower_min = max(1, roll - high)
    upper_max = min(MAX_ROLL, roll + high)
    total = 0
    for m in range(lower_min, upper_max + 1):
        for num_min in range(1, n + 1):
            print(m, num_min, (min(m + high, upper_max) - (m)),(p_binDistInRange(n, 1/NUM_STATES, num_min, num_min) * p_binDistInRange(n - num_min, (min(m + high, upper_max) - (m))/NUM_STATES, n - num_min, n - num_min)) )
            total += (p_binDistInRange(n, 1/NUM_STATES, num_min, num_min) * p_binDistInRange(n - num_min, (min(m + high, upper_max) - (m))/NUM_STATES, n - num_min, n - num_min))
    return total

def getPayoutGrid(roll):
    grid = [[i] * 5 for i in [2, 3, 4, 6]]
    # 0, 0
    grid[0][0] *= p_sumInRange(4, 52 - roll, 4 * MAX_ROLL)
    # 0, 1
    grid[0][1] *= p_binDistInRange(4, pow_count[1]/NUM_STATES, 4 - (1 if roll % 2 == 0 else 0), 4)
    # 0, 2
    if roll <= 3:
        grid[0][2] = 0
    else:
        grid[0][2] *= p_binDistInRange(4, 17/NUM_STATES, 4, 4)
    # 0, 3
    if roll > 11:
        grid[0][3] *= p_binDistInRange(4, 9/NUM_STATES, 2, 2)
    else:
        grid[0][3] *= p_binDistInRange(4, 9/NUM_STATES, 3, 3)
    # 0, 4
    if roll in [2, 3, 5, 7, 11, 13, 17, 19]: #needs to be updated if max roll > 20
        grid[0][4] *= p_binDistInRange(4, 8/NUM_STATES, 2, 4)
    else:
        grid[0][4] *= p_binDistInRange(4, 8/NUM_STATES, 3, 4)
    # 1, 0
    grid[1][0] *= p_binDistInRange(4, 1/NUM_STATES, 1, 4)
    # 1, 1
    n = roll
    prod2Countroll = 0
    while n > 1 and n % 2 == 0:
        n //= 2
        prod2CountRoll += 1
    grid[1][1] *= p_prod2CountInRange(4, 0, 2 - prod2CountRoll)
    # 1, 2
    grid[1][2] *= p_prod2CountInRange(4, 7 - prod2CountRoll, NUM_STATES)
    # 1, 3
    grid[1][3] *= p_sumInRange(4, 0, 45 - roll)
    # 1, 4
    grid[1][4] *= p_deltaMinMaxRange(4, roll, 11)
        
print(p_deltaMinMaxRange(5, 10, 100))
