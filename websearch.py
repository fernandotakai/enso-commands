class WebSearchCmd(object):
    def __init__(self, url_template):
        self._url_template = url_template

    def __call__(self, ensoapi, query=None):
        if not query:
            query = ensoapi.get_selection().get("text", u"")
        query = query.strip()

        if not query:
            ensoapi.display_message( "No query." )
            return

        query = urllib.quote( query.encode("utf-8") )        

        webbrowser.open( self._url_template % {"query" : query} )

cmd_wiki = WebSearchCmd("http://en.wikipedia.org/wiki/%(query)s")
cmd_amaz = WebSearchCmd("http://www.amazon.com/exec/obidos/search-handle-url/index%%3Dblended%%26field-keywords%%3D%(query)s%%26store-name%%3Dall-product-search")
cmd_imdb = WebSearchCmd("http://www.imdb.com/find?s=all&q=%(query)s&x=0&y=0")
cmd_mdc = WebSearchCmd("http://www.google.com/search?hl=en&q=%(query)s+site%%3Adeveloper.mozilla.org&btnG=Google+Search")
