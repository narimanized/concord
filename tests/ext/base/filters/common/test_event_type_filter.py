"""
The MIT License (MIT)

Copyright (c) 2017-2018 Nariman Safiulin

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import pytest

from hugo.core.client import Client
from hugo.core.constants import EventType
from hugo.core.context import Context
from hugo.core.middleware import is_successful_result
from hugo.ext.base.filters.common import EventTypeFilter


@pytest.mark.asyncio
async def test_ignoring(client):
    event = EventType.READY
    ec = EventTypeFilter(EventType.MESSAGE)

    assert not is_successful_result(
        await ec.run(
            ctx=Context(client, event), next=Client.default_next_callable
        )
    )


@pytest.mark.asyncio
async def test_passing(client):
    event = EventType.MESSAGE
    ec = EventTypeFilter(event)

    assert is_successful_result(
        await ec.run(
            ctx=Context(client, event), next=Client.default_next_callable
        )
    )
