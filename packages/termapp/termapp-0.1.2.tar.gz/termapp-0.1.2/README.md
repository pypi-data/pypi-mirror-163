# termapp

[![CI Status](https://github.com/halimath/termapp/workflows/CI/badge.svg)](https://github.com/halimath/termapp/actions/workflows/ci.yaml)
[![Releases](https://img.shields.io/github/v/release/halimath/termapp.svg)](https://github.com/halimath/termapp/releases)
[![PyPi](https://img.shields.io/pypi/v/termapp.svg)](https://pypi.org/project/termapp/)
[![Wheel](https://img.shields.io/pypi/wheel/termapp.svg)](https://pypi.org/project/termapp/)
[![Python Versions](https://img.shields.io/pypi/pyversions/termapp.svg)](https://pypi.org/project/termapp/)

Create terminal applications with python.

# Installation

```shell
pip install termapp
```

# Usage

```python
import asyncio

from termapp import __version__
from termapp.styles import BOLD
from termapp.asyncio import create_app

app = create_app()


async def start():
    await app.write_line(f"termapp demo app v{__version__}", BOLD)
    await app.write_line('This app demonstrates the capabilities of the termapp module.')

    await app.info('info is used to introduce an important step in the app.')
    await app.details('details can be used to add additional informationen.')

    await app.warn('warn shows a warning')
    await app.details('which can also be enhanced with a details message.')

    await app.danger('error reports an error message')
    await app.details('which can also be enhanced with a details message.')

    await app.start_progress(show_completion=True)
    await asyncio.sleep(5)
    await app.stop_progress()
    await app.details('Longer operation finished.')

    await app.success('success is used to indicate success')

    await app.failure('failure is used to indicate the operation failed')


async def warn_later():
    await asyncio.sleep(0.5)
    await app.update_progress(completion=0.3, message='Some task to be done')
    await asyncio.sleep(0.5)
    await app.update_progress(completion=0.6)
    await asyncio.sleep(0.5)
    await app.update_progress(message='Another task to be done')
    await asyncio.sleep(0.5)
    await app.update_progress(completion=0.9)
    await asyncio.sleep(1)
    await app.warn('Something unexpected happened')


async def main():
    return await asyncio.gather(start(), warn_later())

asyncio.run(main())
```

# License

Copyright 2022 Alexander Metzner.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
