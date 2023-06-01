# Bank Bot

# Table of contents
- [Bot features](#bot-features)
- [Prerequisites](#prerequisites)
- [Running locally](#running-locally)
- [Technical aspects and implementation details](#technical-aspects-and-implementation-details)

## Bot features:

- paying credit card debts,
- planning a meeting with a bank manager,
- helping to choose a credit card.

### Paying credit card debts

- The Bot offers to choose a card that will be used to pay the debt. One can choose a card seeing the last 4 digits.
- The Bot offers to state the date of withdrawal. There is a payment deadline for each card. The stated date must be not earlier than the current one and not later than the payment deadline.
- The Bot offers to state the sum of payment. There is a minimal sum for each card. A user has got a debit account which will be used to withdraw the payment. The sum of payment must be not lower than a minimal one and not more than the debit account balance.
- The Bot ask a user to confirm the payment.

### Planning a meeting with a bank manager

- The Bot asks for the date and time of a meeting.
- The Bot asks for the postal/ZIP code of a client to offer the nearest bank offices. Checking the code the Bot detects if the bank has nearest offices. Even ones have and odd ones don’t have.
- If there are available offices, the Bot shows a map and asks to choose a suitable office with the help of a digit.
- The Bot asks for the purpose of a meeting – a free form text.
- The Bot informs that the meeting has been appointed successfully.


### Helping to choose a credit card

The Bot offers clients different types of credit cards:

- MegaSaver — a low interest rate for using the loan,
- MegaCredit — the spending limit increases when the credit history improves,
- TravelRewads — airline miles reward,
- UltimateCashBack — a cashback bonus is accrued by cash,
- BalancedRewards — a cashback bonus is accrued by points.

The Bot must help a client to choose a credit card. It asks some clarifying questions and then offers one or several cards to choose from.

First of all, the Bot must clarify what is the most important for a user:

- to save money (MegaSaver),
- to increase a credit rating (MegaCredit),
- to get a cashback.

If a user wants to increase a credit rating, the Bot additionally clarifies the current rating to set up a limit on a MegaCredit card. There are 3 values of a credit rating: low, average and high. A user can write these values or state a digit. The digits are interpreted as:

- lower than 300 — low,
- from 300 to 700 — average,
- more than 700 — high.

If a user wants to get a cashback, the Bot clarifies which way is preferable: airline miles, points or cash, and then offers an appropriate card.

The bank is more interested in issuing cards with a cashback. That is why the Bot asks a user if they are interested in getting a cashback when they choose to save money or to increase a credit rating. If yes, the Bot clarifies the type of a cashback.

# Prerequisites

1. Install [Poetry](https://python-poetry.org/docs/#installation).
2. Install [Docker](https://docs.docker.com/engine/install/).

> **Warning**
> If you are running one of the Linux distros on WSL, select "Docker Desktop for Windows" instead of "Docker Desktop for Linux".

3. Obtain your bot token in [Telegram](https://core.telegram.org/bots/tutorial#obtain-your-bot-token).

Maxbot is compatible with 64-bit Python versions 3.9 – 3.11 and runs on Unix/Linux, macOS/OS X and Windows.

But the `bank_bot example` depends on the [RASA](https://pypi.org/project/rasa/) package which does not support Python 3.11.
So you need Python 3.9 or 3.10 to run the example.


# Running locally

1. Clone this repository and change current directory

```
$ git clone git@github.com:maxbot-ai/bank_bot.git
$ cd bank_bot
```

2. Install the dependencies

```
$ poetry install
```

3. Pull [rasa/duckling image](https://hub.docker.com/r/rasa/duckling)

```
$ docker pull rasa/duckling
```

4. Run rasa/duckling container

```
$ docker run -d -p 8000:8000 docker.io/rasa/duckling
```

Depends on your OS settings, you may need to use `sudo` command to run container, e.g.

```
$ sudo docker run -d -p 8000:8000 docker.io/rasa/duckling
```

Then check that duckling NER runs well:

```
$ curl -XPOST http://localhost:8000/parse --data 'locale=en_GB&text=tomorrow at eight'
```

The result must be similar to

```
[
  {
    "body": "tomorrow at eight",
    "start": 0,
    "value": {
      "values": [
        {
          "value": "2023-05-11T08:00:00.000-07:00",
          "grain": "hour",
          "type": "value"
        },
        {
          "value": "2023-05-11T20:00:00.000-07:00",
          "grain": "hour",
          "type": "value"
        }
      ],
      "value": "2023-05-11T08:00:00.000-07:00",
      "grain": "hour",
      "type": "value"
    },
    "end": 17,
    "dim": "time",
    "latent": false
  }
]
```

5. Train RASA NLU models

```
$ cd rasa
$ rasa train nlu
```
The model will be stored in the `./models` directory as a zipped file.

6. Running an NLU server

For convenience, it's better to run it in a separate terminal. In this case you should previously change directory to one where the model is stored.

```
$ cd bank_bot/rasa
$ rasa run --enable-api -m models
```

Wait until you see `Rasa server is up and running.` before continuing, it can take about a minute or more.

To make sure that RASA service is configured correctly and working you can execute a command:

```
$ curl localhost:5005/model/parse -d '{"text":"Hello! Today."}'
```

The result must contain the data similar to

```
...
"intent": {
    "name": "general_conversation_greetings",
    "confidence": 0.9538576006889343
  },
  "entities": [
    {
      "start": 7,
      "end": 12,
      "text": "Today",
      "value": "2023-02-14T00:00:00.000-05:00",
      "confidence": 1,
      "additional_info": {
        "values": [
          {
            "value": "2023-02-14T00:00:00.000-05:00",
            "grain": "day",
            "type": "value"
          }
        ],
        "value": "2023-02-14T00:00:00.000-05:00",
        "grain": "day",
        "type": "value"
      },
      "entity": "time",
      "extractor": "DucklingEntityExtractor"
    }
...
```

7. Final checks

```
$ cd ..
$ tree
.
├── README.md
├── bank_bot
│   ├── __init__.py
│   ├── bot.py
│   ├── bot.yaml
│   ├── cc_payment.py
│   ├── db.py
│   ├── dialog
│   │   ├── booking.yaml
│   │   ├── cc_choosing.yaml
│   │   ├── fallback.yaml
│   │   ├── making_payment.yaml
│   │   └── welcome.yaml
│   ├── dialog.yaml
│   ├── extensions
│   │   ├── __init__.py
│   │   └── quick_replies.py
│   └── macro
│       └── cc_choosing.jinja
├── poetry.lock
├── pyproject.toml
├── rasa
│   ├── config.yml
│   ├── data
│   │   └── nlu.yml
│   └── models
│       └── nlu-20230214-170902-mode-fuse.tar.gz
└── tests
    ├── test_cc_payment.py
    └── test_db.py
```

Open the file `bot.yaml` and make sure that the settings are correct (note, that telegram api_token will be set on the next step).

```
extensions:
  quick_replies: {}
  babel:
    locale: en_US
  datetime: {}
  jinja_loader: {}
  rasa:
    url: http://0.0.0.0:5005

channels:
  telegram:
    api_token: !ENV ${TELEGRAM_API_KEY}
```

8. Create `.env` file for your telegram bot token.

```
$ echo 'TELEGRAM_API_KEY="110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw"' >> .env
```

9. Run the application

```
$ maxbot run --bot bank_bot.bot -v
```

Note, that `--bot` parameter value (`bank_bot.bot`) is not the file name, but the name of the Bank bot module. See the [docs](https://maxbot.ai/coding-guides/packaging#run-the-bot) for details.

Now you can write to bot in Telegram and check it's features, described above.

# Technical aspects and implementation details

In this case technical aspects are shown:

- using an external NLU-service,
- adding a new command `quick_replies` in the channel with `python` extension,
- the implementation of business logic as a separate `python` module,
- decomposing a dialog into several files,
- using `jinja` macros for deduplication of the code,
- using internal extensions `format` and `datetime`.


## Using an external NLU-service

As an external NLU-service in this example [RASA](https://github.com/RasaHQ/rasa) is used. Maxbot has a built-in support of RASA, for details look into [documentation](https://maxbot.ai/extensions/rasa).

When using an external NLU-service all the `intents` and `entities` are described only in the used service, that means that there is no need to describe these points when adjusting Maxbot. In this case, addressing them in a scenario happens as usual.

To make the example work correctly it is necessary to launch RASA with the support of [Duckling](https://github.com/facebook/duckling). The easiest way to do it is using a docker-container [rasa/duckling](https://hub.docker.com/r/rasa/duckling).

`docker run -p 8000:8000 rasa/duckling`

Config file — `./rasa/config.yml`.<br/>
Training data — `./rasa/data/nlu.yml`.

> **Note**
> Pay attention to the meaning of an attribute url in settings `DucklingEntityExtractor`.
> The address must equal, with the one you used to launch Duckling.


## Adding a command `quick_replies`

Quick Replies allow you to get message recipient input by sending buttons in a message. When a quick reply is tapped, the value of the button is sent in the conversation.

Using Quick Replies allows to guide a conversation in the right direction, offering a user  the most relevant answers at the current stage of a conversation.

At the moment of the implementation of this example a built-in implementation of Maxbot for a `Telegram` channel didn’t support `QuickReplies`. So we had to implement it as an external extension. You can read about extending the opportunities of channels in [documentation](https://maxbot.ai/coding-guides/channels#extending-channels).

The command `QuickReplies` is implemented in the module `quick_replies.py` of the `extentions` package.

> **Note**
> Of course, the implementation of the command as a separate `python` extension is only presented as an example.
> In a real project, it would be much easier to add this command to the `bot.py` file.
> See related [example (https://maxbot.ai/coding-guides/channels#extending-channels).


```
...
│   ├── extensions
│   │   ├── __init__.py
│   │   └── quick_replies.py
...
```

The implementation is rather simple, so there is no point in dwelling on it.

To be able to use the extension in Maxbot it’s necessary to state [entry points specification](https://packaging.python.org/en/latest/specifications/entry-points/). For that we need to describe our extension in the section [plugins](https://python-poetry.org/docs/pyproject/#plugins) in the file `pyproject.toml`.

```
[tool.poetry.plugins.maxbot_extensions]
quick_replies = "bank_bot.extensions:quick_replies_extension"
```

This option to load extensions is useful if you want to distribute your extension as a separate package and be able to use it in other Maxbot's projects. However, if you only need an extension for the current project, it is easier to register the extension using the builder pattern. For details look into [documentation](https://maxbot.ai/coding-guides/extensions#applying-in-source-code). It is important to remember that to be able to configure extensions in the `bot.yaml`, the `available_extensions` parameter must be set in the [builder factory](https://maxbot.ai/coding-guides/extensions#in-project-extensions).

> **Warning**
> To make a command `quick_replies` available in a scenario one has to turn it on in preferences of the Bot.
> In our example the setting is done with the file `bot.yaml`. So it must have this line:


```
...
extensions:
  quick_replies: {}
...
```
We don’t set any preferences for the extension, so we give an empty dictionary `{}` as settings.


## The implementation of business logic as a separate `python` module

While designing the Maxbot library we proceeded from the fact that the dialog logic and business logic of an app must be separated. At the same time, business logic of an app can be implemented in the general-purpose language.

In our example the logic of working with the cards is implemented a separate `python` module.

Look at the file:

```
cc_payment.py
```

The logic of working is encapsulated in the object `User`, that gives the properties and methods of managing user’s cards.

To be able to use the object `User` inside the scenario we have to [extend scenario context](https://maxbot.ai/coding-guides/bots#extending-scenario-context). Thus, we update the information about a user before processing every new reply from them. The updated information (at the moment of processing a reply) is available in the scenario.

```python
@builder.before_turn
def provide_profile(ctx):
    """Provide user profile from external database to scenario context."""
    ctx.scenario.profile = db.get_user(ctx.dialog["user_id"])
```

## Decomposing a dialog into several files

To better the development and simplicity of support it’s rational to decompose complex scenarios into several files according to the logic or some other criteria. For that in Maxbot we use a mechanism [subtrees](https://maxbot.ai/design-guides/subtrees). In our example the scenario of the Bot’s work is split into several files according to the tasks to be solved:

```
...
│   ├── dialog
│   │   ├── booking.yaml
│   │   ├── cc_choosing.yaml
│   │   ├── fallback.yaml
│   │   ├── making_payment.yaml
│   │   └── welcome.yaml
...
```
And the main file of a dialog `dialog.yaml` looks like that:

```
- subtree: welcome

- subtree: booking

- subtree: cc_choosing

- subtree: cc_making_payment

- subtree: fallback
```

> **Note**
> It’s important to remember that the order of including files matters, as it determines the order of units in the final tree of dialogs.


## Using `jinja` macros for deduplication of the code

To deduplicate the code it’s reasonable to use `jinja` macros. In Maxbot the usage of macros is implemented with the internal extension [loader](https://maxbot.ai/extensions/jinja_loader).

Keep in mind, that to be able to use the extension we need to switch it on in the Bot’s settings.

Look at the file `bot.yaml`.

```
extensions:
  ...
  jinja_loader: {}
  ...
```

> **Note**
> It’s important to remember that in the catalogue `dialog` there can be only subtrees of dialogs, that is why macros can’t be located in this
> catalogue. But you can create an appropriate catalogue for them.


In our case the macros are located in the file `cc_choosing.jinja` in the catalogue

```
...
│   └── macro
│       └── cc_choosing.jinja
...
```

## Using internal extensions

The Maxbot library contains several internal extensions that simplify writing scenarios.
The list of extensions you can find in the catalogue [./maxbot/extensions](https://github.com/maxbot-ai/maxbot/tree/main/maxbot/extensions).

```
$ tree
.
├── __init__.py
├── _manager.py
├── datetime.py
├── format.py
├── jinja_loader.py
├── rasa.py
└── rest.py
```

In the example we use filters `format_date` and `format_time` from the module `format.py` to format the date and time respectively. And a filter `datetime` from the module `datetime` to convert the string into an object `datetime`.


# License

This sample code is licensed under MIT license.<br>
Full license text is available in [LICENSE](./LICENSE).
