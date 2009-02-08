def cmd_farewell(ensoapi):
    import AppKit

    app = AppKit.NSApplication.sharedApplication()
    app.terminate_(None)


def _runAppleScript( script ):
    params = [ "osascript", "-e", script ]
    popen = subprocess.Popen( params )
    print popen

def cmd_screen_saver(ensoapi):
    """
    Starts your screen saver.
    """

    _runAppleScript(
        "tell application id \"com.apple.ScreenSaver.Engine\" "
        "to launch"
        )

def cmd_sleep(ensoapi):
    """
    Puts your computer to sleep.
    """

    _runAppleScript(
        "tell application \"Finder\" to sleep"
        )

def cmd_play(ensoapi):
    """
    Plays the current iTunes song.
    """

    _runAppleScript(
        "tell application \"iTunes\" to play"
        )

def cmd_pause(ensoapi):
    """
    Pauses the current iTunes song.
    """

    _runAppleScript(
        "tell application \"iTunes\" to pause"
        )


def cmd_next_track(ensoapi):
    """
    Goes to the next track on iTunes.
    """

    _runAppleScript(
        "tell application \"iTunes\" to next track"
        )

def cmd_previous_track(ensoapi):
    """
    Goes to the previous track on iTunes.
    """

    _runAppleScript(
        "tell application \"iTunes\" to back track"
        )
        
def cmd_refresh_netnewswire(ensoapi):
    """
    Refresh NetNewsWire feeds
    """
    _runAppleScript(
        "tell application \"NetNewsWire\" \n"
        "refreshAll\n"
        "activate\n"
        "end tell"
    )

cmd_refresh_netnewswire.description = "Refresh NetNewsWire feeds"

def cmd_send_colloquy(ensoapi, text=""):
    if not text:
        seldict = ensoapi.get_selection()
        text = seldict.get("text", "")
    
    if not text:
        ensoapi.display_message("No text!")
        return
    
    _runAppleScript("tell application \"Colloquy\"\n"
          "tell active panel of front window\n"
             "send message \"%s\"\n "
          "end tell\n"
        "end tell" % text
    )

cmd_send_colloquy.description = "Sends a message to the active irc channel on Colloquy"