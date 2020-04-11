import json

data = {
    "giant eagle": {
        "login": "",
        "password": ""
    },
    "twilio": {
        "account_sid": "",
        "auth_token": "",
        "from_phone": "+1",
        "to_phones": ["+1", "+1"],
        "test": {
            "account_sid": "",
            "auth_token ": "",
            "test_from": "+15005550006"
        }
    },
    "store_comment": "taken from URL when reserve button is clicked - https://curbsideexpress.gianteagle.com/store/BB361095#/landing",
    "store": "BB361095",
    "mode_comment": "mode should be 'continuous' or 'single'",
    "mode": "continuous",
    "delay_comment": "delay is in seconds",
    "delay": 1200
}

with open('GiantEagle.json', 'w') as outfile:
    json.dump(data, outfile, indent=4)

print(json.dumps(data, indent=4))
