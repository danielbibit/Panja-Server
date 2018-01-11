from panja import common


if common.settings['SMS_PROVIDER'] == 'TWILIO':
    import twilio
elif common.settings['SMS_PROVIDER'] == 'PLIVO':
    import plivo
elif common.settings['SMS_PROVIDER'] == 'NEXMO':
    import nexmo


if common.settings['SMS_PROVIDER'] == 'TWILIO':
    client = Client(common.settings[TWILIO_SID], common.settings[TWILIO_AUTHTOKEN])
    
    def send_sms(destination=[], message, template):
        message = client.messages.create(
            to='00000',
            from_=common.settings['TWILIO_NUMBER'],
            body='cachorro loco')

        return message.sid

elif common.settings['SMS_PROVIDER'] == 'PLIVO':
    def send_sms(destination=[], message, template):
        pass

elif common.settings['SMS_PROVIDER'] == 'NEXMO':
    def send_sms(destination=[], message, template):
        pass
        
else:
    def send_sms(destination=[], message, template):
        pass