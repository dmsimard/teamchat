# A minimal IRC backend configuration for Errbot, for more details see
# - http://errbot.io/en/latest/user_guide/setup.html
# - http://errbot.io/en/latest/user_guide/configuration/irc.html

import logging
import os
import teamchat

# The following configuration is required for teamchat
ROOT = os.path.expanduser("~/.teamchat")
BOT_DATA_DIR = os.path.join(ROOT, "slack")
BOT_LOG_FILE = os.path.join(ROOT, "bot.log")
BOT_EXTRA_PLUGIN_DIR = os.path.join(os.path.dirname(teamchat.__file__), "errbot")

for directory in [ROOT, BOT_DATA_DIR]:
    if not os.path.isdir(directory):
        os.makedirs(directory, mode=0o700, exist_ok=True)

##########################################################################
# Core Errbot configuration                                              #
##########################################################################

BACKEND = 'Slack'
STORAGE = 'Shelf'
AUTOINSTALL_DEPS = False
PLUGINS_CALLBACK_ORDER = (None, )
BOT_LOG_LEVEL = logging.INFO
BOT_LOG_SENTRY = False
SENTRY_DSN = ''
SENTRY_LOGLEVEL = BOT_LOG_LEVEL

BOT_IDENTITY = {
    'token': '',
}
CHATROOM_PRESENCE = ('#',)
BOT_ADMINS = ('',)

REVERSE_CHATROOM_RELAY = {}
CHATROOM_RELAY = {}
DIVERT_TO_PRIVATE = ()
DIVERT_TO_THREAD = ()
