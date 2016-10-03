import sublime_plugin

try:
    from .git_gutter_handler import GitGutterHandler
    from .git_gutter_compare import (
        GitGutterCompareCommit, GitGutterCompareBranch, GitGutterCompareTag,
        GitGutterCompareHead, GitGutterCompareOrigin, GitGutterShowCompare)
    from .git_gutter_jump_to_changes import GitGutterJumpToChanges
    from .git_gutter_popup import show_diff_popup
    from .git_gutter_show_diff import GitGutterShowDiff
except (ImportError, ValueError):
    from git_gutter_handler import GitGutterHandler
    from git_gutter_compare import (
        GitGutterCompareCommit, GitGutterCompareBranch, GitGutterCompareTag,
        GitGutterCompareHead, GitGutterCompareOrigin, GitGutterShowCompare)
    from git_gutter_jump_to_changes import GitGutterJumpToChanges
    from git_gutter_popup import show_diff_popup
    from git_gutter_show_diff import GitGutterShowDiff


class GitGutterCommand(sublime_plugin.TextCommand):
    def __init__(self, *args, **kwargs):
        sublime_plugin.TextCommand.__init__(self, *args, **kwargs)
        self.git_handler = GitGutterHandler(self.view)
        self.show_diff_handler = GitGutterShowDiff(self.view, self.git_handler)

    def run(self, edit, **kwargs):
        if not self.git_handler.on_disk() or not self.git_handler.git_dir:
            return

        if kwargs:
            self._handle_subcommand(**kwargs)
            return

        self.show_diff_handler.run()

    def _handle_subcommand(self, **kwargs):
        view = self.view
        git_handler = self.git_handler
        action = kwargs['action']
        if action == 'jump_to_next_change':
            GitGutterJumpToChanges(view, git_handler).jump_to_next_change()
        elif action == 'jump_to_prev_change':
            GitGutterJumpToChanges(view, git_handler).jump_to_prev_change()
        elif action == 'compare_against_commit':
            GitGutterCompareCommit(view, git_handler).run()
        elif action == 'compare_against_branch':
            GitGutterCompareBranch(view, git_handler).run()
        elif action == 'compare_against_tag':
            GitGutterCompareTag(view, git_handler).run()
        elif action == 'compare_against_head':
            GitGutterCompareHead(view, git_handler).run()
        elif action == 'compare_against_origin':
            GitGutterCompareOrigin(view, git_handler).run()
        elif action == 'show_compare':
            GitGutterShowCompare(view, git_handler).run()
        elif action == 'show_diff_popup':
            point = kwargs['point']
            flags = kwargs['flags']
            show_diff_popup(view, point, git_handler, flags=flags)
        else:
            assert False, 'Unhandled sub command "%s"' % action
