# import urllib2
# import urllib
# # import requests


# def smsmod_send(message, phone, port='TA', sender=''):

#     values = {
#         'api_id': 'OTU2Nzc3NzU1NA',
#         'senderid': sender,
#         'numbers': '{}'.format(phone),
#         'message': '{}'.format(urllib.quote_plus(message)),
#         'port': port
#     }

#     url = '''https://app.smsbits.in/api/user?id={api_id}&senderid={senderid}&to={numbers}&msg={message}&port={port}'''.format(
#         **values)
#     urllib2.urlopen(url)
