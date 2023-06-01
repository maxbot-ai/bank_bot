"""Quick replies implementation for Telegram channel."""

from marshmallow import Schema, fields
from maxbot.maxml import markup
from telegram import KeyboardButton, ReplyKeyboardMarkup


class QuickRepliesCommand(Schema):
    """Text message with button list."""

    # Text message sent to the user along with the button list.
    text = markup.Field(required=True, metadata={"maxml": "element"})

    # Button titles to be sent to the user.
    button = fields.List(fields.String)

    # The placeholder to be shown in the input field when the keyboard is active.
    input_field_placeholder = fields.String(required=False)

    # Requests clients to hide the keyboard as soon as it's been used.
    one_time_keyboard = fields.Bool(required=False, missing=True, default=True)


class QuickRepliesExtension:
    """Extension for send quick replies."""

    async def send_quick_replies(self, command: dict, dialog: dict):
        """Send quick replies command, :class:`QuickRepliesCommand`.

        See https://core.telegram.org/bots/api#replykeyboardmarkup
        See https://core.telegram.org/bots/api#keyboardbutton

        :param dict command: A command with the payload :attr:`QuickRepliesCommand`.
        :param dict dialog: A dialog we respond in, with the schema :class:`~maxbot.schemas.DialogSchema`.
        """
        keyboard = [[KeyboardButton(text)] for text in command["quick_replies"]["button"]]
        await self.bot.send_message(
            dialog["user_id"],
            text=command["quick_replies"]["text"].render(),
            reply_markup=ReplyKeyboardMarkup(
                keyboard,
                resize_keyboard=True,
                one_time_keyboard=command["quick_replies"].get("one_time_keyboard"),
                input_field_placeholder=command["quick_replies"].get("input_field_placeholder"),
            ),
        )
