"""Building bank bot."""

from maxbot import MaxBot

from bank_bot.db import DataBase

builder = MaxBot.builder()

# this is a stub, actually you can load user
# profile from database or external api

db = DataBase()


@builder.before_turn
def provide_profile(ctx):
    """Provide user profile from external database to scenario context."""
    ctx.scenario.profile = db.get_user(ctx.dialog["user_id"])


builder.use_package_resources("bank_bot")
bot = builder.build()
