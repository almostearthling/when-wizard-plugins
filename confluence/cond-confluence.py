# confluence.py
# -*- coding: utf-8 -*-
#
# Use multiple triggers for a task: consequence plugin (condition)
# Copyright (c) 2015-2018 Francesco Garosi
# Released under the BSD License (see LICENSE file)


import os
import re
import locale
import glob
from plugin import CommandConditionPlugin, PLUGIN_CONST, plugin_name

# setup localization for both plugin text and configuration pane
# locale.setlocale(locale.LC_ALL, locale.getlocale())
# locale.bindtextdomain(APP_NAME, APP_LOCALE_FOLDER)
# locale.textdomain(APP_NAME)
# _ = locale.gettext


# if localization is supported, uncomment the lines above, configure
# them as appropriate, and remove this replacement function
def _(x):
    return x


HELP = _("""\
The "Confluence" action contributes to the possibility to trigger another
action along with similar Confluence consequences in the same group: it will
be possible to let the ultimate action be triggered if all confluent actions
were successful.
""")


class Plugin(CommandConditionPlugin):

    def __init__(self):
        CommandConditionPlugin.__init__(
            self,
            basename=plugin_name(__file__),
            name=_("Confluence"),
            description=_("Triggered by a Group of Confluent Events"),
            author="Francesco Garosi",
            copyright="Copyright (c) 2016",
            icon='collect',
            help_string=HELP,
            version="0.1.0",
        )
        self.resources.append('plugin_cond-confluence.glade')
        self.builder = self.get_dialog('plugin_cond-confluence')
        self.plugin_panel = None
        self.forward_allowed = False
        self.scripts.append('cond-confluence.sh')
        self.command_line = None
        self.summary_description = None
        self.persistence_dir = self.file_storage('plugin_confluence')

    def get_pane(self):
        if self.plugin_panel is None:
            o = self.builder.get_object
            self.plugin_panel = o('viewPlugin')
            self.builder.connect_signals(self)
            o('cbEntry').get_model().clear()
            try:
                files = glob.glob('%s/*.expected' % self.persistence_dir)
            except FileNotFoundError:
                files = []
            groups = [os.path.basename(x).split('.')[0] for x in files]
            groups.sort()
            for x in groups:
                o('cbEntry').append_text(x)
        return self.plugin_panel

    def change_entry(self, obj):
        o = self.builder.get_object
        group_name = o('cbEntry').get_active_text()
        if group_name:
            self.command_line = '%s "%s" "%s"' % (
                self.get_script('cond-confluence.sh'),
                group_name,
                self.persistence_dir)
            self.summary_description = _(
                "When the events in the '%s' group occur") % group_name
            self.allow_forward(True)
        else:
            self.command_line = None
            self.summary_description = None
            self.allow_forward(False)


# end.
