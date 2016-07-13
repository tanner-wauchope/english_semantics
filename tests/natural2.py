from plain_english.natural5 import *


def tanner_semantics():
    # tanner is a person
    tanner = Word('tanner')
    Person = type('Person', (Noun,), {})
    person = Person()
    executable = Is(tanner, person)
    scope = {}
    executable.run(scope)
    assert scope['tanner'] is person


# time/minute/hour/day/week/month/year
"""
1 day has 24 hours
1 hour has 60 minutes
1 minute has 60 seconds

a week has 7 days
day 1 is sunday
day 2 is monday
day 3 is tuesday
day 4 is wednesday
day 5 is thursday
day 6 is friday
day 7 is saturday

a year has 12 months
month 1 is january
month 2 is february
month 3 is march
month 4 is april
month 5 is may
month 6 is june
month 7 is july
month 8 is august
month 9 is september
month 10 is october
month 11 is november
month 12 is december

january has 31 days
march has 31 days
april has 30 days
may has 31 days
june has 30 days
july has 31 days
august has 31 days
september has 30 days
october has 31 days
november has 30 days
december has 31 days

february has 29 days some years
4 divides the years
february has 28 days some years
4 does not divide the years

a time has
    seconds
    minutes
    hours

a date has
    a day
    a month
    a year

an event has
    a time
    a date


a time has a value
the value is (seconds + 60 * minutes + 3600 * hours)

a time has a name
the name is "HH:MM:SS"
the hour is HH
the minute is MM
the second is SS

a date has a name
the name is "YYYY-MM-DD"
the year is YYYY
the month is MM
the day is DD

a date has a value
D is the day
M is the month
Y is (year % 100)
C is (year // 100)
the value is (D + (13 * (M + 1)) // 5 + Y + Y // 4 + C // 4 - 2 * C)

a date has a weekday
N is (date % 7)
a week has days
the name is day N

humanize a date
the result is ("{w}, {d} {m} {y}".format(w=weekday, d=day, m=month, y=year))

thing 1 is before thing 2
thing 1 has a value
N is the value
thing 2 has a value
M is the value
do/say/make? (N < M)
"""

"""
person - wrapper for IO functions
place - wrapper for lat-lon
thing - wrapper for object
group - wrapper for ordered dict
text - wrapper for string
number - wrapper for decimal
time - wrapper for datetime
"""

# be, have, do, say, go, can, get, make, will
