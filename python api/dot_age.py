"""
Calculate Dot's age.
*** Sat 15th Feb 2020
"""
from datetime import date as d

print("Let's calculate your pooch's age!\n")

now = d.today()
birth = d(2018,8,25)

print("Today is " + now.strftime("%c") + "\nPooch's birthday is " + birth.strftime("%c"))
print("")

# How many years' difference
# between today's year and 
# year of birth?
result = now.year - birth.year

# If we have not reached date
# of birth this year yet,
# decrement by one month.
decremented = False
if now.month < birth.month or (now.month == birth.month and now.day < birth.day):
  result-=1
  decremented = True

# How many months passed
# since last birthday?
if decremented:
  remainderMonths = 12 - birth.month + now.month
  if remainderMonths == 12: remainderMonths = 11
else: 
  remainderMonths = now.month - birth.month

# Take away a month if
# we have not yet matched
# day of birth this month.
if now.day < birth.day and decremented == False:
  remainderMonths-=1

# Print results.
if result == 1: yr = " year"
else: yr = " years"
if remainderMonths == 1: mr = " month :D"
else: mr = " months :)"

print(str(result) + yr + "\nAnd " + str(remainderMonths) + mr)
print("\nSo, that's " + str(result * 7) + " human years. Wow.")