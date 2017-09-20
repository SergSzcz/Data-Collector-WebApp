from email.mime.text import MIMEText
import smtplib

def send_email(email,height,av_height,av_height_m,av_height_f,gender):

    from_email = "xxx"
    from_password = "xxx"
    to_email = email

    if gender == 'male':
        gender = "mężczyzną"
    elif gender == 'female':
        gender = "kobietą"
    elif gender == 'other':
        gender = "kimś"

    subject = "Średnia wzrostu"
    text = "Cześć!<br><br> Dzięki za zgłoszenie! <br><br> Jesteś <strong>%s</strong> o wzroście: <strong>%s</strong> cm. <br><br>Średni wzrost kobiet:<strong> %s </strong>cm,\
        a średni wzrost mężczyzn:<strong>%s</strong>cm.<br><br> Średnia wzrostu ogółem:<strong> %s</strong> cm." % (gender,height,av_height_f,av_height_m,av_height)

    msg = MIMEText(text, 'html')

    msg['Subject'] = subject
    msg['To'] = to_email
    msg['From'] = from_email

    onet = smtplib.SMTP('smtp.poczta.onet.pl', 587)
    onet.ehlo()
    onet.starttls()
    onet.ehlo()
    onet.login(from_email, from_password)
    onet.send_message(msg)
    onet.quit()
