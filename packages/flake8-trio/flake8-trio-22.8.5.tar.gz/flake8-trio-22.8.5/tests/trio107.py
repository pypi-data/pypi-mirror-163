import typing
from typing import Any, Union, overload

import trio

_ = ""

# INCLUDE TRIO108


async def foo() -> Any:
    await foo()


async def foo2():  # error: 0, "exit", Statement("function definition", lineno)
    ...


# If
async def foo_if_1():  # error: 0, "exit", Statement("function definition", lineno)
    if _:
        await foo()


async def foo_if_2():
    if _:
        await foo()
    else:
        await foo()


async def foo_if_3():
    await foo()
    if _:
        ...


async def foo_if_4():  # safe
    await foo()
    if ...:
        ...
    else:
        ...


# IfExp
async def foo_ifexp_1():  # safe
    print(await foo() if _ else await foo())


async def foo_ifexp_2():  # error: 0, "exit", Statement("function definition", lineno)
    print(_ if False and await foo() else await foo())


# nested function definition
async def foo_func_1():
    await foo()

    async def foo_func_2():  # error: 4, "exit", Statement("function definition", lineno)
        ...


async def foo_func_3():  # error: 0, "exit", Statement("function definition", lineno)
    async def foo_func_4():
        await foo()


async def foo_func_5():  # error: 0, "exit", Statement("function definition", lineno)
    def foo_func_6():  # safe
        async def foo_func_7():  # error: 8, "exit", Statement("function definition", lineno)
            ...


async def foo_func_8():  # error: 0, "exit", Statement("function definition", lineno)
    def foo_func_9():
        raise


# normal function
def foo_normal_func_1():
    return


def foo_normal_func_2():
    ...


# overload decorator
@overload
async def foo_overload_1(_: bytes):
    ...


@typing.overload
async def foo_overload_1(_: str):
    ...


async def foo_overload_1(_: Union[bytes, str]):
    await foo()


# conditions
async def foo_condition_1():  # safe
    if await foo():
        ...


async def foo_condition_2():  # error: 0, "exit", Statement("function definition", lineno)
    if False and await foo():
        ...


async def foo_condition_3():  # error: 0, "exit", Statement("function definition", lineno)
    if ... and await foo():
        ...


async def foo_condition_4():  # safe
    while await foo():
        ...


async def foo_condition_5():  # safe
    for i in await foo():
        ...


async def foo_condition_6():  # in theory error, but not worth parsing
    for i in (None, await foo()):
        break


# loops
async def foo_while_1():  # error: 0, "exit", Statement("function definition", lineno)
    while _:
        await foo()


async def foo_while_2():  # now safe
    while _:
        await foo()
    else:
        await foo()


async def foo_while_3():  # safe
    await foo()
    while _:
        ...


# for
async def foo_for_1():  # error: 0, "exit", Statement("function definition", lineno)
    for _ in "":
        await foo()


async def foo_for_2():  # now safe
    for _ in "":
        await foo()
    else:
        await foo()


async def foo_while_break_1():  # safe
    while ...:
        await foo()
        break
    else:
        await foo()


async def foo_while_break_2():  # error: 0, "exit", Statement("function definition", lineno)
    while ...:
        break
    else:
        await foo()


async def foo_while_break_3():  # error: 0, "exit", Statement("function definition", lineno)
    while ...:
        await foo()
        break
    else:
        ...


async def foo_while_break_4():  # error: 0, "exit", Statement("function definition", lineno)
    while ...:
        break
    else:
        ...


async def foo_while_continue_1():  # safe
    while ...:
        await foo()
        continue
    else:
        await foo()


async def foo_while_continue_2():  # safe
    while ...:
        continue
    else:
        await foo()


async def foo_while_continue_3():  # error: 0, "exit", Statement("function definition", lineno)
    while ...:
        await foo()
        continue
    else:
        ...


async def foo_while_continue_4():  # error: 0, "exit", Statement("function definition", lineno)
    while ...:
        continue
    else:
        ...


async def foo_async_for_1():
    async for _ in trio.trick_pyright:
        ...


# async with
# async with guarantees checkpoint on at least one of entry or exit
async def foo_async_with():
    async with trio.trick_pyright:
        ...


# raise
async def foo_raise_1():  # safe
    raise ValueError()


async def foo_raise_2():  # safe
    if _:
        await foo()
    else:
        raise ValueError()


# try
# safe only if (try or else) and all except bodies either await or raise
# if foo() raises a ValueError it's not checkpointed
async def foo_try_1():  # error: 0, "exit", Statement("function definition", lineno)
    try:
        await foo()
    except ValueError:
        ...
    except:
        raise
    else:
        await foo()


async def foo_try_2():  # safe
    try:
        ...
    except ValueError:
        ...
    except:
        raise
    finally:
        await foo()


async def foo_try_3():  # safe
    try:
        await foo()
    except ValueError:
        await foo()
    except:
        raise


async def foo_try_4():  # safe
    try:
        ...
    except ValueError:
        raise
    except:
        raise
    else:
        await foo()


async def foo_try_5():  # safe
    await foo()
    try:
        pass
    except:
        pass
    else:
        pass


async def foo_try_6():  # error: 0, "exit", Statement("function definition", lineno)
    try:
        pass
    except:
        pass
    else:
        pass


async def foo_try_7():  # safe
    try:
        await foo()
    except:
        await foo()
    else:
        pass


# early return
async def foo_return_1():
    return  # error: 4, "return", Statement("function definition", lineno-1)


async def foo_return_2():  # safe
    if _:
        return  # error: 8, "return", Statement("function definition", lineno-2)
    await foo()


async def foo_return_3():  # error: 0, "exit", Statement("function definition", lineno)
    if _:
        await foo()
        return  # safe
