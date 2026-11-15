import sublime
import sublime_plugin


class WrapCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        settings = sublime.load_settings("Wrap.sublime-settings")

        file_name = self.view.file_name()
        if file_name:
            extension = self.view.file_name().split(".")[-1]
        else:  # In blank view without file open
            extension = ""

        # Determine bracket type
        bracket_type = settings.get("bracket_type", "()")
        for c in settings.get("contexts"):
            scope = c.get("scope")
            extensions = c.get("extensions")
            if (scope is not None and self.view.match_selector(self.view.sel()[0].begin(), scope)) or (extensions is not None and extension in extensions):
                bracket_type = c.get("bracket_type", "()")
                break
        try:
            a, b = bracket_type
        except:
            sublime.error_message(
                "[Wrap] Invalid bracket type: %r. For a pair of brackets that is not 2 characters, use a list in Wrap.sublime-settings." % bracket_type
            )
            return

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
