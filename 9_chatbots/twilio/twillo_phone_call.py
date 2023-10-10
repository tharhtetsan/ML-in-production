from twilio.rest import Client
import os
# Your Account SID from twilio.com/console
account_sid = os.environ['TWILIO_ACCOUNT_SID']
# Your Auth Token from twilio.com/console
auth_token  = os.environ['TWILIO_AUTH_TOKEN']




print("account_sid : ", account_sid)
print("auth_token : ",auth_token)

client = Client(account_sid, auth_token)



call = client.calls.create(
                        url='http://demo.twilio.com/docs/voice.xml',
                        to="+959783847610", 
                        from_="+15855751220",
                    )

print(call.sid)