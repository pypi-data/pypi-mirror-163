from typing import Callable, Awaitable, Union, Sequence

from aiogram.filters.content_types import ContentTypesFilter
from aiogram.types import Message, ContentType

from aiogram_dialog.manager.protocols import (
    DialogManager, ManagedDialogAdapterProto, ManagedDialogProto
)
from aiogram_dialog.widgets.action import Actionable
from aiogram_dialog.widgets.widget_event import (
    WidgetEventProcessor, ensure_event_processor,
)

MessageHandlerFunc = Callable[
    [Message, ManagedDialogAdapterProto, DialogManager],
    Awaitable,
]


class BaseInput(Actionable):
    async def process_message(self, m: Message, dialog: ManagedDialogProto, manager: DialogManager) -> bool:
        raise NotImplementedError


class MessageInput(BaseInput):
    def __init__(self, func: Union[MessageHandlerFunc, WidgetEventProcessor, None],
                 content_types: Union[Sequence[str], str] = ContentType.ANY):
        super().__init__()
        self.func = ensure_event_processor(func)
        self.filter = ContentTypesFilter(content_types=content_types)

    async def process_message(self, message: Message,
                              dialog: ManagedDialogProto,
                              manager: DialogManager) -> bool:
        if not await self.filter(message):
            return False
        await self.func.process_event(message, manager.dialog(), manager)
        return True
