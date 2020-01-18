# confluence.py
# -*- coding: utf-8 -*-
#
# Use multiple triggers for a task: consequence plugin
# Copyright (c) 2015-2018 Francesco Garosi
# Released under the BSD License (see LICENSE file)


import os
import re
import locale
import glob
from plugin import TaskPlugin, PLUGIN_CONST, plugin_name

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


validate_confluence_name = re.compile(r"^[a-zA-Z][a-zA-Z0-9_]*$")


class Plugin(TaskPlugin):

    def __init__(self):
        TaskPlugin.__init__(
            self,
            category=PLUGIN_CONST.CATEGORY_TASK_MISC,
            basename=plugin_name(__file__),
            name=_("Confluent Task"),
            description=_("Concur in triggering a compound condition"),
            author="Francesco Garosi",
            copyright="Copyright (c) 2016",
            icon='parallel_tasks',
            help_string=HELP,
            version="0.1.0",
        )
        self.resources.append('plugin_confluence.glade')
        self.builder = self.get_dialog('plugin_confluence')
        self.plugin_panel = None
        self.forward_allowed = False

        self.scripts.append('confluence.sh')
        self.command_line = None
        self.summary_description = None
        self.persistence_dir = self.file_storage('plugin_confluence')
        self.group_name = None

        # the plugin data store can be used to save associations of tasks
        # and groups, because group information is lost in the default
        # task store process: in this way if this task is not a new one
        # its group can be easily retrieved; we can be sure no overwrite
        # is possible since ids are unique by construction
        self.data = self.data_retrieve()
        if self.data is None:
            self.data = {}
            self.data_store(self.data)

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

    def register_action(self):
        if self.group_name:
            expected = '%s.expected' % self.group_name
            with open(os.path.join(self.persistence_dir, expected), 'a') as f:
                f.write('%s\n' % self.unique_id)
            self.command_line = '%s "%s" "%s" "%s"' % (
                self.get_script('confluence.sh'),
                self.group_name,
                self.persistence_dir,
                self.unique_id)
            self.data[self.unique_id] = self.group_name
            self.data_store(self.data)
            return True
        else:
            # would never happen
            return False

    def remove_action(self):
        # in this case the group name is surely none because only the
        # manager can delete the action, so it has to be retrieved
        if self.group_name is None:
            if self.unique_id in self.data:
                self.group_name = self.data[self.unique_id]
        if self.group_name:
            expected = '%s.expected' % self.group_name
            with open(os.path.join(self.persistence_dir, expected), 'r') as f:
                l = f.read().strip().split()
            l.remove(self.unique_id)
            with open(os.path.join(self.persistence_dir, expected), 'w') as f:
                f.write('\n'.join(l))
            del self.data[self.unique_id]
            self.data_store(self.data)
        return True

    def change_entry(self, obj):
        o = self.builder.get_object
        s = o('txtEntry').get_text()
        if validate_confluence_name.match(s):
            self.group_name = s
            self.summary_description = _(
                "Add up to the '%s' confluence group") % self.group_name
            self.allow_forward(True)
        else:
            self.group_name = None
            self.summary_description = None
            self.allow_forward(False)


# end.
