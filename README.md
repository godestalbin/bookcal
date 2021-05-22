# BookCal README

## Principle
Allow potential customers to quickly indentify availabilies for a guest house and preregister the dates they intend to book.
We consider it is a preregistration as, currently, we do not request to pay any no deposit.

## Current features
Status on 2020-01-11
* Display a booking calendar with a form to send preregistation
* Show unavailable dates (guest house closing dates)
* Show other booked dates
* Allow to select a date range for the preregistration
* Provide basic controls on the data keyed in
* Post the form and register the data in a MongoDb
* Send a SMS (Free mobile gateway)
* Implemented storage of all keys in Google secret manager

## Currently working on
* Implement booking form for more than one room

## Next features
* Allow to manage more room, currently we have only one hardcoded room
* Send mail/SMS when a booking is registered