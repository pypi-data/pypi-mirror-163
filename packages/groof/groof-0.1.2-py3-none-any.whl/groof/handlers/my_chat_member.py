from .base import Handler
from .. import filters
from ..loader import HANDLERS


def my_chat_member(
        status: str | list[str] = None,
        user_id: int | list[int] = None,
        chat_type: str | list[str] = None,
        state: str = None,
):
    _filters = [
        filters.MyChatMember(),
        filters.State(state),
    ]

    if status:
        _filters.append(filters.ChanMemberStatus(status))

    if user_id:
        _filters.append(filters.UserId(user_id))

    if chat_type:
        _filters.append(filters.ChatType(chat_type))

    def _(func):
        if isinstance(func, Handler):
            func = func.func

        handler = Handler(func, _filters)
        HANDLERS.append(handler)
        return handler

    return _
