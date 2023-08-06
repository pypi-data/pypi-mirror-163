from typing import Generator

from .plugin import Plugin


class PluginHandler:
    def __init__(self, ert, plugin_jobs, parent_window):
        """@type plugin_jobs: list of WorkflowJob"""
        self.__ert = ert
        self.__plugins = []

        for job in plugin_jobs:
            plugin = Plugin(self.__ert, job)
            self.__plugins.append(plugin)
            plugin.setParentWindow(parent_window)

        self.__plugins = sorted(self.__plugins, key=Plugin.getName)

    def ert(self):
        """@rtype: res.enkf.enkf_main.EnKFMain"""
        return self.__ert

    def __iter__(self) -> Generator[Plugin, None, None]:
        index = 0
        while index < len(self.__plugins):
            yield self.__plugins[index]
            index += 1

    def __getitem__(self, index) -> Plugin:
        return self.__plugins[index]

    def __len__(self):
        return len(self.__plugins)
