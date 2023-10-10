from twilio.rest import Client
import os
# Your Account SID from twilio.com/console
account_sid = os.environ['TWILIO_ACCOUNT_SID'].strip()
# Your Auth Token from twilio.com/console
auth_token  = os.environ['TWILIO_AUTH_TOKEN'].strip()

print("account_sid : ",account_sid)
print("auth_token : ",auth_token)

client = Client(account_sid, auth_token)

message = client.messages.create(
    to="+959795800315", 
    from_="+15855751220",
    body="Hello from Python!")

print(message.sid)