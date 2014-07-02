import string
import argparse
import re
import os

from .. import git
from ... tools.toolbox import bash

alias=['plugins']

def _is_plugin_installed(module_name):
    #Quick-n-dirty hack to check which modules are installed.
    #TODO: Fix this!!!
    subdirs = os.walk('..').next()[1] #Get dirnames
    if module_name in subdirs:
       return True
    return False

class Plugin():
    name = ''
    download_name = ''
    descripton = ''
    git_url = ''
    is_installed = False

    def __init__(self, **kwargs):
        for kw, arg in kwargs.iteritems():
            setattr(self, kw, arg)

class PluginFactory(list):
    def parse(self, line):
        raise NotImplementedError()

class PipePluginFactory(PluginFactory):
    def parse(self, line):
        items = string.split(line, '|')
        new_plugin = Plugin(name=items[0], download_name=items[1], description=items[2], git_url=items[3])
        new_plugin.is_installed = _is_plugin_installed(new_plugin.module_name)
        return new_plugin

class PluginFile(file):
    pass

class Plugins(list):
    plugin_file = None
    plugin_factory = None

    def __init__(self, plugin_file, plugin_factory):
        self.plugin_file = plugin_file
        self.plugin_factory = plugin_factory

    def __str__(self):
        return self.plugins

    def parse_file(self):
        for line in self.plugin_file:
            if not line.lstrip().startswith('#'):
                plugin = self.plugin_factory.parse(line)
                self.append(plugin)

plugins = None
with PluginFile('plugin_urls.txt','r') as plugin_file:
    plugins = Plugins(plugin_file, PipePluginFactory())
    plugins.parse_file()

def usage():
    print 'plugin [list [wildcard]|install <module name>|update <module name>]'

def plugin_list(wildcard):
    #TODO: Enhance silly wildcard implementation
    #TODO: Make this better
    wildcard = wildcard.replace('*','.*')
    for plugin in plugins:
        print 'Name:{0}\nDescription: {1}\n\n'.format(plugin.name, plugin.descripton)

def plugin_install(plugin_name):
    #TODO: Fix this ugly directory hack. Quick n dirty
    #TODO: Plugins should be a hash, not a list
    if not _is_plugin_installed(plugin_name):
        for plugin in plugins:
            if plugin.name == plugin_name:
                os.mkdir(os.path.append('..',plugin_name))
                git.do_git('clone ' + plugin.git_url)
    else:
        print 'Already installed'

def plugin_update(plugin_name):
    raise NotImplementedError()

def plugin_remove(plugin_name):
    raise NotImplementedError()

def main(self, line):
    args = re.split('\s+')
    if len(args) > 0:

        command = args[0]
        args = args[1:]

        if command == 'list':
            plugin_list(*args)
        elif command == 'install':
            plugin_install(*args)
        elif command == 'update':
            plugin_update(*args)
        elif command == 'remove':
            plugin_remove(*args)

        #parser = argparse.ArgumentParser(prog='plugin'
        #                                 , usage='plugin [list|install|update|remove]'
        #                                 , description="Perform operations on plugins")

        #parser.add_argument('url', type=str, nargs='?', help='URL to push to')
        #parser.add_argument('-u', metavar='username[:password]', type=str, required=False, help='username[:password]')
        #result = parser.parse_args(args)

        #parser.add_argument('url', type=str, nargs='?', help='URL to push to')

