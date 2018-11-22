# Copyright 2018 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import json
import os
import requests
import logging
from errbot import BotPlugin, webhook

class TeamChat(BotPlugin):
    @webhook("/teamchat")
    def bridge(self, request):
        """
        This is the part that receives bridge requests
        """
        # Parse incoming requests for parameters we're interested in
        params = {
            param: request.get(param, None)
            for param in ["source", "destination", "channel", "to", "author", "message"]
        }
        logging.debug("Request parsed to: %s" % str(params))

        # Don't handle the request if we're not the destination
        if params["destination"] != os.getenv('TC_SOURCE'):
            logging.warn(f"Ignoring request for bridging to {params['destination']}")
            return

        # Don't handle the request if we're not managing the channel
        if params["to"] != os.getenv('TC_CHANNEL'):
            logging.warn(f"Ignoring request for bridging to {params['destination']}")
            return

        # Broadcast the message to the channel we're configured to use
        for room in self.rooms():
            room = str(room)
            if room == params["to"]:
                self.send(
                    self.build_identifier(room),
                    f"{params['author']}: {params['message']}"
                )
                logging.info(f"Bridged message from {params['source']} by {params['author']} to [{params['channel']}")

    def callback_message(self, msg):
        """
        This is the part that requests a message to be bridged
        """
        # Messages sent privately to the bot should not be replayed !
        # We only want to replay messages that are coming from a thread or channel.
        if msg.is_direct:
            return

        # Get the data we need to send the callback webhook
        data = dict(
            source=self.bot_config.BACKEND,
            destination=os.getenv('TC_DESTINATION'),
            channel=os.getenv('TC_CHANNEL'),
            to=os.getenv('TC_TO'),
            author=msg.frm.nick,
            message=msg.body
        )
        endpoint = os.getenv('TC_DESTINATION_ENDPOINT')

        # Don't attempt to bridge messages that are empty or have failed to parse
        if data['author'] == '' or data['message'] == '':
            logging.info("Not sending bridge request: empty or failed to parse")
            return

        logging.info("Sending bridge request")
        r = requests.post(endpoint, data=json.dumps(data))
