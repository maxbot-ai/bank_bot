"""Simple quick replies extensions for Telegram channel."""


from .quick_replies import QuickRepliesCommand, QuickRepliesExtension


def quick_replies_extension(builder, config):
    """Register a `QuickRepliesCommand` command."""
    builder.add_command(QuickRepliesCommand, "quick_replies")
    builder.add_channel_mixin(QuickRepliesExtension, "telegram")
