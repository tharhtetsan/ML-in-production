from twilio.rest import Client
import os
# Your Account SID from twilio.com/console
account_sid = os.environ['TWILIO_ACCOUNT_SID']
#"AC220d8ead16bbd5037a83db62a79137e4"
# Your Auth Token from twilio.com/console
auth_token  = os.environ['TWILIO_AUTH_TOKEN']
#"1b3854a65bc4f1157230122758af932f"





client = Client(account_sid, auth_token)



call = client.calls.create(
                        url='http://demo.twilio.com/docs/voice.xml',
                        to='+15855751220',
                        from_='+959783847610'
                    )

print(call.sid)