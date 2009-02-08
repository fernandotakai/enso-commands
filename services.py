def _do_service(ensoapi, serviceName):
    import AppKit

    text = ensoapi.get_selection().get("text", "").strip()

    if not text:
        ensoapi.display_message("No text selection!")
        return

    pb = AppKit.NSPasteboard.pasteboardWithName_("EnsoServiceContent")

    pb.declareTypes_owner_( [AppKit.NSStringPboardType], None )

    try:
        if not pb.setString_forType_( text, AppKit.NSStringPboardType ):
            raise Exception( "Failed to set pasteboard data." )

        if not AppKit.NSPerformService( serviceName, pb ):
            raise Exception( "Failed to perform service." )
    finally:
        pass

def cmd_define(ensoapi):
    _do_service(ensoapi, "Look Up in Dictionary")

cmd_define.description = "Look Up In Dictonary for the selected word"

def cmd_speak(ensoapi):
    _do_service(ensoapi, "Speech/Start Speaking Text")

cmd_speak.description = "Speak the selected text"

def cmd_summarize(ensoapi):
    _do_service(ensoapi, "Summarize")
    
cmd_summarize.description = "Open summarize with the selected text."

def cmd_spotlight(ensoapi):
    _do_service(ensoapi, "Spotlight")
    
cmd_spotlight.description = "Searches on spotlight for the selected word"