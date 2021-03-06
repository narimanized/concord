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

from concord.constants import EventType
from concord.context import Context
from concord.ext.base.filters.common import PatternFilter
from concord.middleware import is_successful_result as isr, middleware as m
from concord.utils import empty_next_callable

from tests.helpers import make_discord_object


@pytest.mark.asyncio
async def test_simple_pattern(client):
    event = EventType.MESSAGE
    pattern = r"some text"
    content = "A message with some text to check"
    context = Context(
        client, event, message=make_discord_object(0, content=content)
    )

    pf = PatternFilter(pattern)
    assert isr(await pf.run(ctx=context, next=empty_next_callable))


@pytest.mark.asyncio
async def test_pattern_with_named_groups(client):
    event = EventType.MESSAGE
    pattern = r"find (?P<first>\w+) and (?P<second>\w+)"
    content = "It should find 42 and firework as first and second parameters"
    context = Context(
        client, event, message=make_discord_object(0, content=content)
    )

    @m(PatternFilter(pattern))
    async def mw(*args, ctx, next, first, second, **kwargs):
        assert first == "42"
        assert second == "firework"

    assert isr(await mw.run(ctx=context, next=empty_next_callable))


@pytest.mark.asyncio
async def test_pattern_with_named_groups_ignores_unnamed(client):
    event = EventType.MESSAGE
    pattern = r"find (\w+) and (?P<first>\w+)"
    content = "It should find 42 and firework but match only firework as first"
    context = Context(
        client, event, message=make_discord_object(0, content=content)
    )

    @m(PatternFilter(pattern))
    async def mw(*args, ctx, next, first, **kwargs):
        assert first == "firework"

    assert isr(await mw.run(ctx=context, next=empty_next_callable))


@pytest.mark.asyncio
async def test_ignoring(client):
    event = EventType.MESSAGE
    pattern = r"some text"
    content = "A message without text to match"
    context = Context(
        client, event, message=make_discord_object(0, content=content)
    )

    pf = PatternFilter(pattern)
    assert not isr(await pf.run(ctx=context, next=empty_next_callable))
