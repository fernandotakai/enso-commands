class Launcher(object):
    def __init__(self):
        import Foundation
        import AppKit

        self._targets = {}

        query = Foundation.NSMetadataQuery.alloc().init()
        queryString = ( "((kMDItemKind == \"Application\") "
                        " and (kMDItemSupportFileType != \"MDSystemFile\"))" )
        queryString += " or (kMDItemKind == \"Mac OS X Preference Pane\")"
        predicate = Foundation.NSPredicate.predicateWithFormat_(
            queryString
            )
        query.setPredicate_( predicate )
        if query.startQuery() != True:
            raise Exception( "startQuery() failed." )
        self._query = query
        self._workspace = AppKit.NSWorkspace.sharedWorkspace()
        self._targets = {}

    def get_namespace(self):
        return self._targets.keys()

    def get_target(self, name):
        return self._targets[name]

    def update(self):
        query = self._query

        while query.isGathering():
            yield

        # TODO: Modify this so we just get notified whenever the query
        # results change instead of constantly "polling" every time
        # the quasimode starts.

        resultList = []
        targets = {}

        query.disableUpdates()
        numresults = query.resultCount()

        BATCH_SIZE = 10

        for i in range( numresults ):
            result = query.resultAtIndex_( i )
            fsname = result.valueForAttribute_("kMDItemFSName")
            name = result.valueForAttribute_("kMDItemDisplayName")
            kind = result.valueForAttribute_("kMDItemKind")
            if name:
                name = name.lower()
                itempath = result.valueForAttribute_("kMDItemPath")
                if kind == "Mac OS X Preference Pane":
                    name += " preferences"
                    target = ShellOpenLaunchableTarget(itempath)
                else:
                    target = AppLaunchableTarget(self._workspace, itempath)
                resultList.append(name)
                targets[name] = target
            if i / BATCH_SIZE == i / float(BATCH_SIZE):
                yield
        #print "total results: %s" % numresults
        query.enableUpdates()
        targets["computer"] = ShellOpenLaunchableTarget("/")
        self._targets = targets

class AppLaunchableTarget(object):
    def __init__(self, workspace, path):
        self._workspace = workspace
        self._path = path

    def launch(self, with_files=None):
        if with_files:
            for filename in with_files:
                self._workspace.openFile_withApplication_(
                    filename,
                    self._path
                    )
        else:
            self._workspace.launchApplication_( self._path )

    def can_launch_with(self):
        return True

class ShellOpenLaunchableTarget(object):
    def __init__(self, path):
        self._path = path

    def launch(self):
        subprocess.Popen( ["open", self._path] )

    def can_launch_with(self):
        return False

class OpenCommand(object):
    """
    Opens an application, folder, or URL.
    """

    def __init__(self, launcher):
        self.launcher = launcher
        self._isFetchingArgs = False

    def on_quasimode_start(self):
        if self._isFetchingArgs:
            return

        self._isFetchingArgs = True

        for _ in self.launcher.update():
            yield

        self.valid_args = self.launcher.get_namespace()

        self._isFetchingArgs = False

    valid_args = []

    def __call__(self, ensoapi, target=None):
        if not target:
            seldict = ensoapi.get_selection()
            if seldict.get("files"):
                for file in seldict["files"]:
                    subprocess.Popen( ["open", file] )
            elif seldict.get("text"):
                filename = seldict["text"].strip()
                if os.path.isabs(filename):
                    subprocess.Popen( ["open", filename] )
                else:
                    webbrowser.open(filename)
        else:
            self.launcher.get_target(target).launch()

class OpenWithCommand(object):
    """
    Opens the selected file(s) with a particular application.
    """

    def __init__(self, launcher):
        self.launcher = launcher

    def _get_valid_args(self):
        return self.launcher.get_namespace()

    valid_args = property(_get_valid_args)

    def __call__(self, ensoapi, target):
        files = ensoapi.get_selection().get("files", [])
        targ = self.launcher.get_target(target)
        if not files:
            ensoapi.display_message("No files selected!")
        elif not targ.can_launch_with():
            ensoapi.display_message("Can't open files with %s." % target)
        else:
            targ.launch(files)

cmd_go = OpenCommand(Launcher())
cmd_open = cmd_go
cmd_bust_with = OpenWithCommand(cmd_open.launcher)
