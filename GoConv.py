#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sublime, sublime_plugin, subprocess, threading

def get_settings_value(key):
	settings = {}
	settings = sublime.load_settings(__name__ + '.sublime-settings')
	return settings.get(key)

print get_settings_value("node_path")

class GoconvCommand(sublime_plugin.TextCommand):

	def run(self, edit, config):

		for region in self.view.sel():
			if not region.empty():
				convtext = self.view.substr(region)
				convregion = region
			else:
				convtext = self.view.substr(sublime.Region(0, self.view.size()))
				convregion = sublime.Region(0, self.view.size())

			args = [
					sublime.load_settings(__name__+".sublime-settings").get("node_path"),
					sublime.packages_path() + '/' + __name__ + '/lib/goconv.js',
					config, convtext
			]

			thread = NodeJS(args)
			thread.start()
			self.handle_thread(thread, edit, config, convregion)
				

	def handle_thread(self, thread, edit, config, convregion):
		if (thread.isAlive()):
			sublime.set_timeout(lambda: self.handle_thread(thread, edit, config, convregion), 100)
		elif (thread.result != False):
			thread.result = thread.result.decode('utf-8')
			self.view.replace(edit, convregion, thread.result)

class NodeJS(threading.Thread):

	def __init__(self, args):
		self.args = args
		self.result = None
		threading.Thread.__init__(self)

	def run(self):
		try:
			process = subprocess.Popen(self.args, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.STDOUT);

			# Make the result accessible by the main thread
			self.result = process.communicate()[0]

		except OSError:
			sublime.error_message('Error calling NodeJS app')
			self.result = False