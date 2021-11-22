import sublime
import sublime_plugin


class WrapCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        settings = sublime.load_settings("Wrap.sublime-settings")
        a, b = settings.get("bracket_type", "()")

        region = self.view.sel()[0]

        # Cursor on empty line
        if self.view.substr(self.view.word(region)).strip() == "":
            self.view.run_command("insert_snippet", {"contents": "${1:abc}" + a + "$0" + b})
            return

        # No selection
        if region.empty():
            # Do nothing if selection has no alphanumeric character
            if not any(char.isalnum() for char in self.view.substr(self.view.word(region))):
                return
            self.view.run_command("find_under_expand")  # Select text under cursor

        # Wrap selection with parentheses
        self.view.run_command("insert_snippet", {"contents": "${1:abc}" + a + "${0:$SELECTION}" + b})
