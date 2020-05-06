teamchat
========

.. image:: docs/source/_static/team_chat.png

`XKCD <https://xkcd.com/1782/>`_

teamchat breaks the barriers between communities and instant messaging platforms.

teamchat replays messages from two different communication systems to each other
in order to allow everyone to talk to each other regardless of their chat platform
preferences.

The project is meant to be a spiritual successor to `slack-irc <https://github.com/ekmartin/slack-irc>`_
which stopped working when `Slack discontinued the IRC gateway <https://news.ycombinator.com/item?id=16539857>`_.

TL;DR
=====

In a nutshell, teamchat leverages `Errbot <http://errbot.io/en/latest/>`_, a python
chatbot framework. It launches two bots, one for each desired backend.

These bots will relay messages they see in their channel to each other over a
localhost webhook implementation that Errbot provides out of the box.

That's it, really.

Supported backends
==================

Errbot supports many different `backends <http://errbot.io/en/latest/features.html#multiple-server-backends>`_
out of the box:

- XMPP (Any standards-compliant XMPP/Jabber server should work - Google Talk/Hangouts included)
- Hipchat
- IRC
- Slack
- Telegram

Many other backends are available through community support such as Discord,
Mattermost and Skype.

Installing teamchat
===================

Anywhere with python >= 3.6 available::

    pip3 install teamchat

Configuring teamchat
====================

teamchat launches two chat bots, one in each of the configured and requested
backends.
It joins the desired channels and then forwards messages from one channel to the
other in both directions.

Each of your communication backend must be configured in a different
`Errbot settings file <http://errbot.io/en/latest/user_guide/setup.html#id1>`_.

You can get started from the Errbot configuration template by running
``teamchat template`` which will generate a template for you at
``~/.teamchat/backends/template.py``.

When running the ``teamchat connect`` command to create the bridge, these
backend file names will be used. For example:

- The backend named ``slack_community`` would be expected at ``~/.teamchat/backends/slack_community.py``
- The backend named ``irc_community`` would be expected at ``~/.teamchat/backends/irc_community.py``.

Your server, credentials, nicknames, tokens and other fine tuning will need to
be set up through those files according to the Errbot backend
`configuration documentation <http://errbot.io/en/latest/features.html#multiple-server-backends>`_.

Please note that your backend settings file needs to contain a few extra lines
meant for teamchat::

    import teamchat

    # The following configuration is required for teamchat
    ROOT = os.path.expanduser("~/.teamchat")
    BOT_DATA_DIR = os.path.join(ROOT, "irc")
    BOT_LOG_FILE = os.path.join(ROOT, "bot.log")
    BOT_EXTRA_PLUGIN_DIR = os.path.join(os.path.dirname(teamchat.__file__), "errbot")

    for directory in [ROOT, BOT_DATA_DIR]:
        if not os.path.isdir(directory):
            os.makedirs(directory, mode=0o700, exist_ok=True)

For examples of backend configuration files, look at the ``contrib`` directory
of the project on `GitHub <https://github.com/dmsimard/teamchat>`_.

Using teamchat
==============

Getting started with teamchat once you have your configuration set up looks like this::

    teamchat connect irc_community \    # From IRC
             --bridge slack_community \ # To Slack
             --channel "#dev" \         # From #dev on the server configured in ~/.teamchat/backends/irc_community.py
             --to "#general"            # To #general on the server configured in ~/.teamchat/backends/slack_community.py

The order of the arguments as well as the from/to destinations does not matter.
The messages will always be replayed from one backend to the other in both directions.

For example, the following command would yield the exact same results as the one above::

    teamchat connect slack_community \ # From Slack
         --bridge irc_community \      # To IRC
         --channel "#general" \        # From #general on the server configured in ~/.teamchat/backends/slack_community.py
         --to "#dev"                   # To #dev on the server configured in ~/.teamchat/backends/irc_community.py

Known issues
============

- Naming your backend file ``~/.teamchat/backends/irc.py`` does not work because it conflicts with the ``irc`` python module.
