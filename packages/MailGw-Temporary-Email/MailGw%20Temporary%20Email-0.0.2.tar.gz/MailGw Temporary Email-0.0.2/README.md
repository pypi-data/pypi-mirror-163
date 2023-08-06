# MailGW API Wrapper



Mail.gw is a free 10 minute temporary mail service, This library is useful for automation tasks such as making accounts that needs email verification.

Account delete itself after 10 minutes

## Installation

Windows:

```
pip install MailGw-Temporary-Email
```

Linux/Mac OS:

```
pip3 install MailGw-Temporary-Email
```

## Example

```python
from mailgw_temporary_email import Email

def listener(message):
    print("\nSubject: " + message['subject'])
    print("Content: " + message['text'] if message['text'] else message['html'])

# Get Domains
test = Email()
print("\nDomain: " + test.domain)

# Make new email address
test.register()
print("\nEmail Adress: " + str(test.address))

# Start listening
test.start(listener)
print("\nWaiting for new emails...")
```

# Documentation

API: [https://mail.gw](https://docs.mail.gw/)

`register(username=None, password=None, domain=None)` | Make an email account with random credentials, You can also pass a username, password and domain to use the same account.

`start(listener, interval=3)` | Start listening for new emails, Interval means how many seconds takes to sync, And you also need to pass a function for `listener`, This function gets called when new email arrive.

`stop()` | Stop listening for new emails.
