---
blogpost: true
date: Mar 13, 2025
author: Jens W. Klein
location: Austria
category: Knowledge
language: en
---

# Storing a Date Without a Timezone Kills a Kitten on Every Save

When storing event dates in an IT system, the most important factor is preserving the original editor’s intended timezone, rather than normalizing everything to UTC.
UTC is just another timezone — it doesn’t inherently simplify calculations.
By storing the event in the editor’s intended timezone, all necessary computations for display can be performed dynamically.

## Lessons Learned

During the development of `plone.app.event`, we explored this in depth.
Initially, we experimented with storing in UTC or storing the timezone in a separate field, but this approach introduced unnecessary complexity.
In the end, we concluded that keeping the date in the editor’s timezone was the most effective solution - and storing it as a non-naive Python datetime (a datetime object with timezone attached).

## Timezone, not Offset

Important is to store the semantic timezone, like "Europe/Vienna" and not the offset like UTC+2 (or +1?).
Only the timezone tells us about daylight saving adjustments.

The [tz database](https://www.iana.org/time-zones) contains all timezones, including historial ones.
In Python 3.9+ the [zoneinfo](https://docs.python.org/3/library/zoneinfo.html) in the standard library provides it, before [pytz](https://pypi.org/project/pytz/) add-on was used often

## Recurring Events!

When dealing with recurring events, it's crucial to store the original date along with the editor’s timezone. Suppose a user in a U.S. timezone schedules a daily event at 10 AM during daylight saving time (DST).
If the system converts this to UTC, it loses the context of the intended timezone, since UTC has no DST.

This becomes a problem when daylight saving time ends or begins.
On the transition day, clocks either move back or forward by an hour, making that day 23 or 25 hours long.
Because different regions switch at different times, it's impossible to correctly adjust recurring events for display stored solely in UTC.

## No Information Must get Lost!

Timezone information is essential to ensure the event always aligns with the user’s original intent.

## Convert at Display Time

When displaying the event for other users in different time zones, conversions can be made dynamically — e.g., a 10 AM weekly event might usually appear as 3 PM for someone in a different timezoneelse.
During certain weeks, it may shift to 2 PM.
This adjustment must be handled at the time of rendering, not by normalizing the input to a fixed timezone.


*written because of many chats with different people about this, based on my [reply at community.plone.org in conversion "Datetime fields and timezones in Plone 5.2](https://community.plone.org/t/datetime-fields-and-timezones-in-plone-5-2/13332) 2021-01-14*