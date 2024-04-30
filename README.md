# Automatic booking of washing machines at NSU.

This package provides the opportunity for booking washing machine in NSU dormitories.

## Installation

`pip install nsubooking`

## Setting env

For use this package you need tu setup your envirement variables.

You can do that with `.env` file in root directory or `export $var = data`.

**You need folowing envirement variables:**

- EMAIL (required) - email of your booking account.
- PASSWORD (required) - password of your booking account.
- PAGE_LIVE_TIME (nonrequired) - time between bookings.
- BOOK_WAIT (nonrequired) - time between page reloads while waiting available machines.

## Quickstart

To quickstart try following code:

```python
from nsubooking import run


if __name__ == 'main':
  run()
```

To inject app to async loop you can also use:

```python
from nsubooking import run_loop
import asyncio


if __name__ == 'main':
  asyncio.run(run_loop())
```

**But in this case logger will not configured.**
