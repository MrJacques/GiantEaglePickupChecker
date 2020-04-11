import json

from twilio.rest import Client

with open('GiantEagle.json') as f:
    data = json.load(f)

assert (len(data['twilio']['account_sid']) > 0)
assert (len(data['twilio']['auth_token']) > 0)
assert (len(data['twilio']['from_phone']) > 0)
assert (len(data['twilio']['to_phones']) > 0)

twilio_sid = data['twilio']['account_sid']
twilio_token = data['twilio']['auth_token']
twilio_from_phone = data['twilio']['from_phone']
twilio_to_phones = data['twilio']['to_phones']
# twilio_test_sid = data['twilio']['test']['account_sid']
# twilio_test_token = data['twilio']['test']['auth_token']
# twilio_test_from = data['twilio']['test']['testst_from']

# live creds
client = Client(twilio_sid, twilio_token)

# test credentials
# client = Client(twilio_test_sid, twilio_test_token)
# twilio_from_phone = twilio_test_from

for to_phone in twilio_to_phones:
    client.messages.create(
        to=to_phone,
        from_=twilio_from_phone,
        body="TEST IGNORE - Giant Eagle Alert, Pickups for the following dates found: ")

