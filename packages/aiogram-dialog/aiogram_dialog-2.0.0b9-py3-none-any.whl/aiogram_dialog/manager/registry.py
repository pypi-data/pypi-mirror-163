import asyncio
from contextvars import copy_context
from typing import Sequence, Type, Dict, Optional

from aiogram import Dispatcher, Bot, Router
from aiogram.dispatcher.event.telegram import TelegramEventObserver
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup, any_state
from aiogram.types import User, Chat, Message

from .manager import ManagerImpl
from .manager_middleware import ManagerMiddleware
from .protocols import (
    ManagedDialogProto, DialogRegistryProto, DialogManager,
    MediaIdStorageProtocol, MessageManagerProtocol, DialogManagerFactory,
)
from .update_handler import handle_update
from ..context.events import StartMode, DIALOG_EVENT_NAME, DialogUpdate
from ..context.intent_filter import (
    IntentFilter, IntentMiddlewareFactory, IntentErrorMiddleware,
    context_saver_middleware,
)
from ..context.media_storage import MediaIdStorage
from ..exceptions import UnregisteredDialogError
from ..message_manager import MessageManager


class DialogEventObserver(TelegramEventObserver):
    pass


class DialogRegistry(DialogRegistryProto):
    def __init__(
            self,
            dp: Dispatcher,
            dialogs: Sequence[ManagedDialogProto] = (),
            media_id_storage: Optional[MediaIdStorageProtocol] = None,
            message_manager: Optional[MessageManagerProtocol] = None,
            dialog_manager_factory: DialogManagerFactory = ManagerImpl,
            default_router: Optional[Router] = None,
    ):
        self.dp = dp
        self.update_handler = self.dp.observers[DIALOG_EVENT_NAME] = DialogEventObserver(
            router=self.dp, event_name=DIALOG_EVENT_NAME
        )
        self.default_router = default_router if default_router else dp.include_router(
            Router(name="aiogram_dialog_router")
        )

        self.dialogs = {
            d.states_group(): d for d in dialogs
        }
        self.state_groups: Dict[str, Type[StatesGroup]] = {
            d.states_group_name(): d.states_group() for d in dialogs
        }
        self.register_update_handler(handle_update, any_state)

        if media_id_storage is None:
            media_id_storage = MediaIdStorage()
        self._media_id_storage = media_id_storage
        if message_manager is None:
            message_manager = MessageManager()
        self._message_manager = message_manager
        self.dialog_manager_factory = dialog_manager_factory
        self._register_middleware()

    @property
    def media_id_storage(self) -> MediaIdStorageProtocol:
        return self._media_id_storage

    @property
    def message_manager(self) -> MessageManagerProtocol:
        return self._message_manager

    def register(self, dialog: ManagedDialogProto, *args, router: Router = None, **kwargs):
        group = dialog.states_group()
        if group in self.dialogs:
            raise ValueError(f"StatesGroup `{group}` is already used")
        self.dialogs[group] = dialog
        self.state_groups[dialog.states_group_name()] = group
        dialog.register(
            self,
            router if router else self.default_router,
            IntentFilter(aiogd_intent_state_group=group),
            *args,
            **kwargs
        )

    def register_start_handler(self, state: State):
        async def start_dialog(m: Message, dialog_manager: DialogManager):
            await dialog_manager.start(state, mode=StartMode.RESET_STACK)

        self.dp.message.register(start_dialog, Command(commands="start"), any_state)

    def _register_middleware(self):
        manager_middleware = ManagerMiddleware(
            self, self.dialog_manager_factory,
        )
        intent_middleware = IntentMiddlewareFactory(
            storage=self.dp.fsm.storage, state_groups=self.state_groups
        )
        self.dp.message.middleware(manager_middleware)
        self.dp.callback_query.middleware(manager_middleware)
        self.update_handler.middleware(manager_middleware)
        self.dp.my_chat_member.middleware(manager_middleware)
        self.dp.errors.middleware(manager_middleware)

        self.dp.message.outer_middleware(intent_middleware.process_message)
        self.dp.callback_query.outer_middleware(intent_middleware.process_callback_query)
        self.update_handler.outer_middleware(intent_middleware.process_aiogd_update)
        self.dp.my_chat_member.outer_middleware(intent_middleware.process_my_chat_member)

        self.dp.message.middleware(context_saver_middleware)
        self.dp.callback_query.middleware(context_saver_middleware)
        self.update_handler.middleware(context_saver_middleware)
        self.dp.my_chat_member.middleware(context_saver_middleware)

        self.dp.errors.outer_middleware(IntentErrorMiddleware(
            storage=self.dp.fsm.storage, state_groups=self.state_groups
        ))

    def find_dialog(self, state: State) -> ManagedDialogProto:
        try:
            return self.dialogs[state.group]
        except KeyError as e:
            raise UnregisteredDialogError(
                f"No dialog found for `{state.group}`"
                f" (looking by state `{state}`)"
            ) from e

    def register_update_handler(self, callback, *custom_filters, **kwargs) -> None:
        self.update_handler.register(
            callback, *custom_filters, **kwargs
        )

    async def notify(self, bot: Bot, update: DialogUpdate) -> None:
        callback = lambda: asyncio.create_task(self._process_update(bot, update))

        asyncio.get_running_loop().call_soon(
            callback,
            context=copy_context()
        )

    async def _process_update(self, bot: Bot, update: DialogUpdate):
        event = update.event
        Bot.set_current(bot)
        User.set_current(event.from_user)
        Chat.set_current(event.chat)
        await self.dp.propagate_event(
            update_type="update",
            event=update,
            bot=bot,
            event_from_user=event.from_user,
            event_chat=event.chat,
        )
