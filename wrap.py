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
        for c in settings.get("contexts"):
            scope = c.get("scope")
            extensions = c.get("extensions")
            if (scope is not None and self.view.match_selector(self.view.sel()[0].begin(), scope)) or (extensions is not None and extension in extensions):
                a, b = c.get("bracket_type", "()")
                break
        else:
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
