def _get_clipboard_img_datafile():
    import AppKit

    pb = AppKit.NSPasteboard.generalPasteboard()
    if pb.availableTypeFromArray_([AppKit.NSTIFFPboardType]):
        bytes = pb.dataForType_(AppKit.NSTIFFPboardType).bytes()
        datafile = StringIO(str(bytes))
        return datafile
    else:
        return None

def image_command(func):
    def wrapper(ensoapi):
        import Image

        datafile = _get_clipboard_img_datafile()
        if datafile:
            img = Image.open(datafile)
            return func(ensoapi, img)
        else:
            files = ensoapi.get_selection().get("files", [])
            if files:
                if len(files) == 1:
                    filename = files[0]
                    img = None
                    try:
                        img = Image.open(filename)
                    except IOError, e:
                        ensoapi.display_message("An error occurred: %s." % e)
                    if img:
                        return func(ensoapi, img)
                else:
                    ensoapi.display_message("More than one file selected.")
            else:
                ensoapi.display_message("No image in clipboard, and no "
                                        "file selected.")
    return wrapper

@image_command
def cmd_get_image_size(ensoapi, img):
    outputfile = StringIO()
    img.save(outputfile, "PNG")
    png_size = outputfile.tell()
    outputfile = StringIO()
    img.save(outputfile, "JPEG", quality=90)
    jpg_size = outputfile.tell()
    ensoapi.display_message("png size: %d bytes. jpg-90 size: %d bytes." %
                            (png_size, jpg_size))

def cmd_unupload_image(ensoapi):
    url = ensoapi.get_selection().get("text", "")
    if url:
        if url.startswith(REMOTE_UPLOAD_URL):
            filename = url[len(REMOTE_UPLOAD_URL):]
            localfile = os.path.join(LOCAL_UPLOAD_DIR, filename)
            # It's just easier to upload a truncated file than it is
            # to remove the file remotely.
            open(localfile, "w").close()
            popen = subprocess.Popen(
                ["scp",
                 localfile,
                 "%s%s" % (REMOTE_UPLOAD_DIR, filename)]
                )
            while popen.poll() is None:
                yield
            if popen.returncode == 0:
                os.remove(localfile)
                ensoapi.display_message("Image removed.")
            else:
                ensoapi.display_message("An error occurred.")
        else:
            ensoapi.display_message("URL is not an upload URL.")
    else:
        ensoapi.display_message("No selection!")

LOCAL_UPLOAD_DIR = "/Users/varmaa/Archive/toolness-images/"
REMOTE_UPLOAD_DIR = "toolness.com:/home/varmaa/toolness.com/images/"
REMOTE_UPLOAD_URL = "http://www.toolness.com/images/"

@image_command
def cmd_upload_image(ensoapi, img):
    filename = "%s.jpg" % _get_filelike_timestamp()
    localfile = os.path.join(LOCAL_UPLOAD_DIR, filename)
    img.save(localfile, quality=90)

    ensoapi.display_message("Uploading image...")

    popen = subprocess.Popen(
        ["scp",
         localfile,
         "%s%s" % (REMOTE_UPLOAD_DIR, filename)]
        )
    while popen.poll() is None:
        yield
    if popen.returncode == 0:
        webbrowser.open("%s%s" % (REMOTE_UPLOAD_URL, filename))
    else:
        ensoapi.display_message("An error occurred.")
