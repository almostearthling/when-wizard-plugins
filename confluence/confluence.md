# The Confluence Plugin

The *Confluence* plugin allows to let multiple events or conditions converge to a single action. Due to the "wizard" based interface of the **When Wizard** it's impossible to build up events that depends on several conditions, and here is where the *Confluence* plugin comes to help. The process to activate a confluence is quite simple:

1. choose *Miscellaneous* in the drop-down menu when choosing a task, and *Confluent Task* in the list that appears on the wizard pane
2. give a name to the confluence group in the configuration page: names can consist of letters and digits and underscores, must begin with a letter and are case sensitive. This yields if you are creating a confluence group: if you want to add conditions to an existing one its name must be used, and can be chosen from the drop-down list
3. choose the event that the group depends on, as with other simple tasks: repeat steps 2 and 3 restarting the **When Wizard** until all events that concur to the action are defined
4. restart the **When Wizard** again choose the actual action that should occur in the end as usual
5. in the condition pane, choose *Miscellaneous* from the drop-down box, and *Confluence* in the list that appears below
6. after clicking *Next*, choose the above defined confluence group from the drop-down list.

After this last action is registered, it will only occur after *all* the conditions that are associates with *confluent tasks* of the same group are satisfied. Note that the *event-to-confluent-task* and *confluence-to-task* actions are all listed separately in the **When Wizard Manager**, and that disabling just one of the actions will prevent the confluence from being satisfied.


## Installation Notes

The plugin can be installed using the **When Wizard Manager**: the two *.wwpz* packages must be installed using the *Plugins* tab, and the provided *.widf* file has to be imported using the *Import* tab. No parameters have to be specified for the *.widf* file. To uninstall the plugin, both the *Confluence* and *Confluent Task* plugins must be removed, as well as the *.widf* item definition file.
