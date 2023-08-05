import contextlib
import contextlib as anything
from contextlib import asynccontextmanager, contextmanager
from typing import Any

import trio

_ = ""

# INCLUDE TRIO107


async def foo() -> Any:
    await foo()


async def foo_yield_1():
    await foo()
    yield 5
    await foo()


async def foo_yield_2():
    yield  # error: 4, "yield", Statement("function definition", lineno-1)
    yield  # error: 4, "yield", Statement("yield", lineno-1)
    await foo()


async def foo_yield_3():  # error: 0, "exit", Statement("yield", lineno+2)
    await foo()
    yield


async def foo_yield_4():  # error: 0, "exit", Statement("yield", lineno+3)
    yield  # error: 4, "yield", Statement("function definition", lineno-1)
    await (yield)  # error: 11, "yield", Statement("yield", lineno-1)
    yield  # safe


async def foo_yield_return_1():
    yield  # error: 4, "yield", Statement("function definition", lineno-1)
    return  # error: 4, "return", Statement("yield", lineno-1)


async def foo_yield_return_2():
    await foo()
    yield
    return  # error: 4, "return", Statement("yield", lineno-1)


async def foo_yield_return_3():
    await foo()
    yield
    await foo()
    return


# async with
# async with guarantees checkpoint on at least one of entry or exit
async def foo_async_with():  # error: 0, "exit", Statement("yield", lineno+2)
    async with trio.fail_after(5):
        yield  # error: 8, "yield", Statement("function definition", lineno-2)


# fmt: off
async def foo_async_with_2():  # error: 0, "exit", Statement("yield", lineno+4)
    # with'd expression evaluated before checkpoint
    async with (yield):  # error: 16, "yield", Statement("function definition", lineno-2)
        # not guaranteed that async with checkpoints on entry (or is that only for trio?)
        yield  # error: 8, "yield", Statement("yield", lineno-2)
# fmt: on


async def foo_async_with_3():  # error: 0, "exit", Statement("yield", lineno+3)
    async with trio.fail_after(5):
        ...
    yield  # safe


async def foo_async_with_4():  # error: 0, "exit", Statement("yield", lineno+4)
    async with trio.fail_after(5):
        yield  # error: 8, "yield", Statement("function definition", lineno-2)
        await foo()
    yield


async def foo_async_with_5():  # error: 0, "exit", Statement("yield", lineno+3)
    async with trio.fail_after(5):
        yield  # error: 8, "yield", Statement("function definition", lineno-2)
    yield  # error: 4, "yield", Statement("yield", lineno-1)


# async for
async def foo_async_for():  # error: 0, "exit", Statement("yield", lineno+6)
    async for i in (
        yield  # error: 8, "yield", Statement("function definition", lineno-2)
    ):
        yield  # safe
    else:
        yield  # safe


# await anext(iter) is not called on break
async def foo_async_for_2():  # error: 0, "exit", Statement("yield", lineno+2)
    async for i in trio.trick_pyright:
        yield
        if ...:
            break


async def foo_async_for_3():  # safe
    async for i in trio.trick_pyright:
        yield


async def foo_async_for_4():  # safe
    async for i in trio.trick_pyright:
        yield
        continue


# for
async def foo_for():  # error: 0, "exit", Statement("yield", lineno+3)
    await foo()
    for i in "":
        yield  # error: 8, "yield", Statement("yield", lineno)


async def foo_for_1():  # error: 0, "exit", Statement("function definition", lineno) # error: 0, "exit", Statement("yield", lineno+3)
    for _ in "":
        await foo()
        yield


# while

# safe if checkpoint in else
async def foo_while_1():  # error: 0, "exit", Statement("yield", lineno+5)
    while ...:
        ...
    else:
        await foo()  # will always run
    yield  # safe


# simple yield-in-loop case
async def foo_while_2():  # error: 0, "exit", Statement("yield", lineno+3)
    await foo()
    while ...:
        yield  # error: 8, "yield", Statement("yield", lineno)


# no checkpoint after yield if else is entered
async def foo_while_3():  # error: 0, "exit", Statement("yield", lineno+5)
    while ...:
        await foo()
        yield
    else:
        yield  # error: 8, "yield", Statement("yield", lineno-2) # error: 8, "yield", Statement("function definition", lineno-5)


# check that errors are suppressed in visit_While
async def foo_while_4():  # error: 0, "exit", Statement("yield", lineno+3) # error: 0, "exit", Statement("yield", lineno+5) # error: 0, "exit", Statement("yield", lineno+7)
    await foo()
    while ...:
        yield  # error: 8, "yield", Statement("yield", lineno) # error: 8, "yield", Statement("yield", lineno+2) # error: 8, "yield", Statement("yield", lineno+4)
        while ...:
            yield  # error: 12, "yield", Statement("yield", lineno)# error: 12, "yield", Statement("yield", lineno-2)# error: 12, "yield", Statement("yield", lineno+2)
            while ...:
                yield  # error: 16, "yield", Statement("yield", lineno-2)# error: 16, "yield", Statement("yield", lineno)


# check error suppression is reset
async def foo_while_5():
    await foo()
    while ...:
        yield  # error: 8, "yield", Statement("yield", lineno)

        async def foo_nested_error():  # error: 8, "exit", Statement("yield", lineno+1)# error: 8, "exit", Statement("yield", lineno+1)
            yield  # error: 12, "yield", Statement("function definition", lineno-1)# error: 12, "yield", Statement("function definition", lineno-1)

    await foo()


# --- while + continue ---
# no checkpoint on continue
async def foo_while_continue_1():  # error: 0, "exit", Statement("yield", lineno+3)
    await foo()
    while ...:
        yield  # error: 8, "yield", Statement("yield", lineno)
        if ...:
            continue
        await foo()


# multiple continues
async def foo_while_continue_2():  # error: 0, "exit", Statement("yield", lineno+3)
    await foo()
    while ...:
        yield  # error: 8, "yield", Statement("yield", lineno)
        if ...:
            continue
        await foo()
        if ...:
            continue
        while ...:
            yield  # safe
            await foo()


# --- while + break ---
# else might not run
async def foo_while_break_1():  # error: 0, "exit", Statement("yield", lineno+6)
    while ...:
        if ...:
            break
    else:
        await foo()
    yield  # error: 4, "yield", Statement("function definition", lineno-6)


# no checkpoint on break
async def foo_while_break_2():  # error: 0, "exit", Statement("yield", lineno+3)
    await foo()
    while ...:
        yield  # safe
        if ...:
            break
        await foo()


# guaranteed if else and break
async def foo_while_break_3():  # error: 0, "exit", Statement("yield", lineno+7)
    while ...:
        await foo()
        if ...:
            break  # if it breaks, have checkpointed
    else:
        await foo()  # runs if 0-iter
    yield  # safe


# break at non-guaranteed checkpoint
async def foo_while_break_4():  # error: 0, "exit", Statement("yield", lineno+7)
    while ...:
        if ...:
            break
        await foo()  # might not run
    else:
        await foo()  # might not run
    yield  # error: 4, "yield", Statement("function definition", lineno-7)


# check break is reset on nested
async def foo_while_break_5():  # error: 0, "exit", Statement("yield", lineno+12)
    await foo()
    while ...:
        yield
        if ...:
            break
        await foo()
        while ...:
            yield  # safe
            await foo()
        yield  # safe
        await foo()
    yield  # error: 4, "yield", Statement("yield", lineno-9)


# check multiple breaks
async def foo_while_break_6():  # error: 0, "exit", Statement("yield", lineno+11)
    await foo()
    while ...:
        yield
        if ...:
            break
        await foo()
        yield
        await foo()
        if ...:
            break
    yield  # error: 4, "yield", Statement("yield", lineno-8)


async def foo_while_break_7():  # error: 0, "exit", Statement("function definition", lineno)# error: 0, "exit", Statement("yield", lineno+5)
    while ...:
        await foo()
        if ...:
            break
        yield
        break


# try
async def foo_try_1():  # error: 0, "exit", Statement("function definition", lineno) # error: 0, "exit", Statement("yield", lineno+2)
    try:
        yield  # error: 8, "yield", Statement("function definition", lineno-2)
    except:
        pass


# no checkpoint after yield in ValueError
async def foo_try_2():  # error: 0, "exit", Statement("yield", lineno+5)
    try:
        await foo()
    except ValueError:
        # try might not have checkpointed
        yield  # error: 8, "yield", Statement("function definition", lineno-5)
    except:
        await foo()
    else:
        pass


async def foo_try_3():  # error: 0, "exit", Statement("yield", lineno+6)
    try:
        ...
    except:
        await foo()
    else:
        yield  # error: 8, "yield", Statement("function definition", lineno-6)


async def foo_try_4():  # safe
    try:
        ...
    except:
        yield  # error: 8, "yield", Statement("function definition", lineno-4)
    finally:
        await foo()


async def foo_try_5():
    try:
        await foo()
    finally:
        # try might crash before checkpoint
        yield  # error: 8, "yield", Statement("function definition", lineno-5)
        await foo()


async def foo_try_6():  # error: 0, "exit", Statement("yield", lineno+5)
    try:
        await foo()
    except ValueError:
        pass
    yield  # error: 4, "yield", Statement("function definition", lineno-5)


async def foo_try_7():  # error: 0, "exit", Statement("yield", lineno+16)
    await foo()
    try:
        yield
        await foo()
    except ValueError:
        await foo()
        yield
        await foo()
    except SyntaxError:
        yield  # error: 8, "yield", Statement("yield", lineno-7)
        await foo()
    finally:
        pass
    # If the try raises an exception without checkpointing, and it's not caught
    # by any of the excepts, jumping straight to the finally.
    yield  # error: 4, "yield", Statement("yield", lineno-13)


## safe only if (try or else) and all except bodies either await or raise
## if foo() raises a ValueError it's not checkpointed, and may or may not yield
async def foo_try_8():  # error: 0, "exit", Statement("function definition", lineno) # error: 0, "exit", Statement("yield", lineno+3)
    try:
        await foo()
        yield
        await foo()
    except ValueError:
        ...
    except:
        raise
    else:
        await foo()


# no checkpoint after yield in else
async def foo_try_9():  # error: 0, "exit", Statement("yield", lineno+6)
    try:
        await foo()
    except:
        await foo()
    else:
        yield


# in theory safe, but not currently handled
async def foo_try_10():
    try:
        await foo()
    except:
        await foo()
    finally:
        yield  # error: 8, "yield", Statement("function definition", lineno-6)
        await foo()


# if
async def foo_if_1():
    if ...:
        yield  # error: 8, "yield", Statement("function definition", lineno-2)
        await foo()
    else:
        yield  # error: 8, "yield", Statement("function definition", lineno-5)
        await foo()


async def foo_if_2():  # error: 0, "exit", Statement("yield", lineno+6)
    await foo()
    if ...:
        ...
    else:
        yield
    yield  # error: 4, "yield", Statement("yield", lineno-1)


async def foo_if_3():  # error: 0, "exit", Statement("yield", lineno+6)
    await foo()
    if ...:
        yield
    else:
        ...
    yield  # error: 4, "yield", Statement("yield", lineno-3)


async def foo_if_4():  # error: 0, "exit", Statement("yield", lineno+7)
    await foo()
    yield
    if ...:
        await foo()
    else:
        ...
    yield  # error: 4, "yield", Statement("yield", lineno-5)


async def foo_if_5():  # error: 0, "exit", Statement("yield", lineno+8)
    await foo()
    if ...:
        yield
        await foo()
    else:
        yield
        ...
    yield  # error: 4, "yield", Statement("yield", lineno-2)


async def foo_if_6():  # error: 0, "exit", Statement("yield", lineno+8)
    await foo()
    if ...:
        yield
    else:
        yield
        await foo()
        ...
    yield  # error: 4, "yield", Statement("yield", lineno-5)


async def foo_if_7():  # error: 0, "exit", Statement("function definition", lineno)
    if ...:
        await foo()
        yield
        await foo()


async def foo_if_8():  # error: 0, "exit", Statement("function definition", lineno)
    if ...:
        ...
    else:
        await foo()
        yield
        await foo()


# IfExp
async def foo_ifexp_1():  # error: 0, "exit", Statement("yield", lineno+1) # error: 0, "exit", Statement("yield", lineno+1)
    print((yield) if await foo() else (yield))


# Will either enter else, and it's a guaranteed checkpoint - or enter if, in which
# case the problem is the yield.
async def foo_ifexp_2():  # error: 0, "exit", Statement("yield", lineno+2)
    print(
        (yield)  # error: 9, "yield", Statement("function definition", lineno-2)
        if ... and await foo()
        else await foo()
    )


# normal function
def foo_sync_1():
    return


def foo_sync_2():
    ...


def foo_sync_3():
    yield


def foo_sync_4():
    if ...:
        return
    yield


def foo_sync_5():
    if ...:
        return
    yield


def foo_sync_6():
    while ...:
        yield


def foo_sync_7():
    while ...:
        if ...:
            return
        yield


# nested function definition
async def foo_func_1():
    await foo()

    async def foo_func_2():  # error: 4, "exit", Statement("yield", lineno+1)
        yield  # error: 8, "yield", Statement("function definition", lineno-1)


async def foo_func_3():  # error: 0, "exit", Statement("yield", lineno+2)
    await foo()
    yield

    async def foo_func_4():
        await foo()


async def foo_func_5():  # error: 0, "exit", Statement("yield", lineno+2)
    await foo()
    yield

    def foo_func_6():  # safe
        yield

        async def foo_func_7():
            await foo()
            ...


# Guaranteed checkpoint in case `if` isn't entered
@asynccontextmanager
async def foo_cm_1():  # error: 0, "exit", Statement("yield", lineno+2)
    if ...:
        yield  # error: 8, "yield", Statement("function definition", lineno-2)


@contextlib.asynccontextmanager
async def foo_cm_2():  # error: 0, "exit", Statement("yield", lineno+2)
    if ...:
        yield  # error: 8, "yield", Statement("function definition", lineno-2)


@anything.asynccontextmanager
async def foo_cm_3():  # error: 0, "exit", Statement("yield", lineno+2)
    if ...:
        yield  # error: 8, "yield", Statement("function definition", lineno-2)


@contextmanager
def foo_cm_4():
    if ...:
        yield


@contextlib.contextmanager
def foo_cm_5():
    if ...:
        yield


@anything.contextmanager
def foo_cm_6():
    if ...:
        yield


# No error from function definition, but may shortcut after yield
async def foo_boolops_1():  # error: 0, "exit", Stmt("yield", line+1)
    _ = await foo() and (yield) and await foo()


# may shortcut after any of the yields
async def foo_boolops_2():  # error: 0, "exit", Stmt("yield", line+1) # error: 0, "exit", Stmt("yield", line+1)
    _ = await foo() and (yield) and await foo() and (yield)


# fmt: off
async def foo_boolops_3():  # error: 0, "exit", Stmt("yield", line+1) # error: 0, "exit", Stmt("yield", line+4) # error: 0, "exit", Stmt("yield", line+5)
    _ = (await foo() or (yield) or await foo()) or (
        ...
        or (
            (yield)  # error: 13, "yield", Stmt("yield", line-3)
            and (yield))  # error: 17, "yield", Stmt("yield", line-1)
    )
# fmt: on
