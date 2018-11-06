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

import ansible_runner
import click
import errbot
import os
import shlex
import shutil
import sys
import subprocess
import teamchat

ANSIBLE_ROOT = os.path.join(os.path.dirname(teamchat.__file__), "ansible")
BACKEND_ROOT = os.path.expanduser("~/.teamchat/backends")
# Errbot ships a template, use that as a base
SOURCE_TEMPLATE = os.path.join(os.path.dirname(errbot.__file__), "config-template.py")
CONFIG_TEMPLATE = os.path.join(BACKEND_ROOT, "template.py")

@click.group()
def main():
    pass

@main.command(help="Creates an Errbot backend configuration template")
def template():
    if not os.path.exists(BACKEND_ROOT):
        os.makedirs(BACKEND_ROOT, mode=0o700)
    shutil.copyfile(SOURCE_TEMPLATE, CONFIG_TEMPLATE)
    click.echo(f"Copied {SOURCE_TEMPLATE} to {CONFIG_TEMPLATE}")

@main.command(help="Connects two instant messaging platforms", context_settings=dict(
    ignore_unknown_options=True,
))
@click.argument("source")
@click.option("--bridge", help='destination backend', required=True)
@click.option("--channel", help='from source channel', required=True)
@click.option("--to", help='to destination channel', required=True)
def connect(source, bridge, channel, to):
    source_backend = os.path.join(BACKEND_ROOT, f"{source}.py")
    destination_backend = os.path.join(BACKEND_ROOT, f"{bridge}.py")

    # Minimum validation that the file exists
    for backend in [source_backend, destination_backend]:
        if not os.path.exists(backend):
            click.echo(f"{backend} configuration file not found.")
            sys.exit(1)

    # Use Ansible to set up two Errbot systemd unit services (because why not)
    # - teamchat-source
    # - teamchat-destination
    enable = os.path.join(ANSIBLE_ROOT, "enable-bot.yml")
    r = ansible_runner.run(
        playbook=enable,
        extravars=dict(
            source=source,
            source_backend=source_backend,
            destination=bridge,
            destination_backend=destination_backend,
            channel=channel,
            to=to
        )
    )
