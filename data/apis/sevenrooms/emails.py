import smtplib, ssl
from email.message import EmailMessage
from datetime import datetime, date, timedelta

class APIEmail:
    
    def __init__(self):
        
        self.sender = 'SevenRooms API'
        self.recipients = ['domgunewardena@gmail.com', 'domg@danddlondon.com']
        self.subject = 'SevenRooms API Confirmation'
        self.message = 'Email message'
        
    def send(self):
        
        email = EmailMessage()
        email['from'] = self.sender
        email['to'] = self.recipients
        email['subject'] = self.subject

        email.set_content(self.message)

        with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login("domgunewardenadev@gmail.com", 'd;3d;3d;3')
            smtp.send_message(email)
            
            
class CompletionEmail(APIEmail):
    
    def __init__(self,page,reservations_count,cursor,api_log,start):
        
        super().__init__()
        
        self.subject = "SevenRooms API Request - " + str(reservations_count)
        
        self.message = """Request finished on page """ + str(page-1) + " at " + datetime.now().strftime("%d-%b-%Y (%H:%M:%S)") + """
        
        Total Reservations: """ + str(reservations_count) + """
        Total Duration: """ + str(datetime.now() - start) + """
        
        API Log: """ + str(api_log) + """

        Cursor used: """ + cursor
        
        
class ErrorEmail(APIEmail):
    
    def __init__(self,page,reservations_count,error_text,cursor,api_log,start):
        
        super().__init__()
        
        self.subject = "Subject: SevenRooms API Request Error - " + str(reservations_count)
        
        self.message = """Request finished on page """ + str(page-1) + " at " + datetime.now().strftime("%d-%b-%Y (%H:%M:%S)") + """
        
        Total Reservations: """ + str(reservations_count) + """
        Total Duration: """ + str(datetime.now() - start) + """

        Error: """ + error_text + """

        API Log: """ + str(api_log) + """

        Cursor used: """ + cursor
