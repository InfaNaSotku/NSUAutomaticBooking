**Automatic booking of washing machines at NSU.**
-------------------------------------------------

This package provides the opportunity for booking washing machine in NSU dormitories.

For use this package you need tu setup your envirement variables first.

You can do that with `.env` file in root directory or `export $var = data`.

**You need folowing envirement variables:**
- EMAIL (required) - email of your booking account.
- PASSWORD (required) - password of your booking account.
- PAGE_LIVE_TIME (nonrequired) - time between bookings.
- BOOK_WAIT (nonrequired) - time between page reloads while waiting available machines.

**You can use this package in two scenarios:**
- Application mode:
  1. Clone repo to your machine.
  2. Install `requirements.txt` locate in  root directory.
  3. Run `manage.py` file locate in  root directory.
- Package mode:
  Following...
