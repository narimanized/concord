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
from hugo.core.middleware import AllOfAll, MiddlewareResult, collection_of


@pytest.mark.asyncio
async def test_running_behaviour(context, sample_parameters):
    sa, skw = sample_parameters

    async def first_mw(*args, ctx, next, **kwargs):
        return MiddlewareResult.IGNORE

    async def second_mw(*args, ctx, next, **kwargs):
        return 2

    async def third_mw(*args, ctx, next, **kwargs):
        return 3

    ooa = collection_of(AllOfAll, [first_mw, second_mw, third_mw])
    assert await ooa.run(
        *sa, ctx=context, next=Client.default_next_callable, **skw
    ) == (MiddlewareResult.IGNORE, 2, 3)
