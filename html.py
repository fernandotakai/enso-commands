def htmlifier(func):
    def wrapper(ensoapi):
        seldict = ensoapi.get_selection()
        text = seldict.get("text", "")
        html = seldict.get("html", text)
        if not text:
            ensoapi.display_message("No selection!")
        else:
            result = func(ensoapi, html)
            ensoapi.set_selection(
                {"html":result,
                 "text":result}
                )

    return wrapper

@htmlifier
def cmd_bold(ensoapi, text):
    return "<b>%s</b>" % text

@htmlifier
def cmd_italics(ensoapi, text):
    return "<i>%s</i>" % text

@htmlifier
def cmd_monospace(ensoapi, text):
    return "<pre>%s</pre>" % text

def cmd_normalize(ensoapi):
    normal_template = "<span style=\"font-weight: normal;\">%s</span>"
    seldict = ensoapi.get_selection()
    text = seldict.get("text", "")
    if not text:
        ensoapi.display_message("No selection!")
    else:
        ensoapi.set_selection(
            {"html":normal_template % text,
             "text":text} )