import AddressBook

class SendEmail(object):

    def __init__(self):
        self._isFetchingArgs = False
        self.valid_args = []
        self.people = {}
        self.description = "Send the selected text by email to contact"
        
    def on_quasimode_start(self):
        if self._isFetchingArgs:
            return
        
        self._isFetchingArgs = True
        
        FIELD_NAMES=(
            ('First Name', AddressBook.kABFirstNameProperty),
            ('E-mail',     AddressBook.kABEmailProperty),
        )
        
        book = AddressBook.ABAddressBook.sharedAddressBook()
        
        for row in self.bookFields(book, [ f[1] for f in FIELD_NAMES]):
            yield
            self.people[row[0]] = row[1]
        
        self.valid_args = self.people.keys()
        
    def encode(self, value):
        if value is None:
            return ''

        if isinstance(value, AddressBook.ABMultiValue):
            # A multi-valued property, merge them into a single string
            result = []
            for i in range(len(value)):
                result.append(value.valueAtIndex_(i).encode('utf-8'))
            return ', '.join(result)

        return value.encode('utf-8').lower()
    
    
    def bookFields(self, book, fieldnames):
        for person in book.people():
            yield self.personToFields(person, fieldnames)
    
    def personToFields(self, person, fieldnames):
        return [ self.encode(person.valueForProperty_(nm)) for nm in fieldnames ]
        
    def __call__(self, ensoapi, to=None):
        text = ensoapi.get_selection().get("text", "").strip()
        if not text:
            ensoapi.display_message( "No selection." )
            return

        server = "smtp.gmail.com"
        port = 587
        username = "user@gmail.com"
        password = "passwd"
        
        to = self.people[to]
        print to

        text = text.encode("ascii", "xmlcharrefreplace")

        subject = text.splitlines()[0]
        
        def send_mail():
            import smtplib
            from email.MIMEMultipart import MIMEMultipart
            from email.MIMEBase import MIMEBase
            from email.MIMEText import MIMEText
            from email import Encoders

            try:
                msg = MIMEMultipart()

                msg['From'] = username
                msg['To'] = to
                msg['Subject'] = subject

                msg.attach(MIMEText(text))

                mailServer = smtplib.SMTP(server, 587)
                mailServer.ehlo()
                mailServer.starttls()
                mailServer.ehlo()
                mailServer.login(username, password)
                mailServer.sendmail(username, to, msg.as_string())
                mailServer.close()
            except:
                success[0] = False
                raise

        thread = ThreadedFunc(send_mail)
        ensoapi.display_message( "Sending message..." )
        while thread.isAlive():
            yield
        
        if thread.wasSuccessful():
            ensoapi.display_message( "Message sent." )
        else:
            ensoapi.display_message( "An error occurred when sending the message." )

cmd_send_email = SendEmail()