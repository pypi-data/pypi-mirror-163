# trenalyze(PYTHON) V0.0.2

[Author](https://treasureuvietobore.com/) |
[Docs](https://github.com/Trenalyze/trenalyze__python#readme)


## Library Prerequisites

1. Python >=3.6
1. WhatsApp account.
1. Active Token - Get a Token [here](https://trenalyze.com).


## Installation


Using PIP:
```shell
$ pip install trenalyze__python
```

In PYTHON:

**Note:** You'll need to Import the Trenalyze Python Library after installation

```python
# Load the full build.
from trenalyze__python import Trenalyze
```

## API

### 1. Creating an instance of the Trenalyze class.

```python
# Creating an instance of the Trenalyze class.
trenalyze = Trenalyze()
```

| Param | Type | Description |
| --- | --- | --- |
| token | `string` | Use your Trenalyze Token from your [Dashboard](https://trenalyze.com). |

```python
# Setting the API key for the Trenalyze API.
trenalyze.setToken(token)
```

**Note:** Phone number should be in the following format `12345678912`, without `+` or any other symbols

### 2. Initialize needed variables 

| Param | Type | Description |
| --- | --- | --- |
| sender | `string` | Enter the WhatApp Number that has already been scanned on the Trenalyze [Dashboard](https://trenalyze.com). |
| receiver | `string` | Phone number should be in the international format `2348157002782`, without `+` or any other symbols. |
| msgtext | `string` | Enter the desired text message to send. |
| mediaurl | `string` | (OPTIONAL). **BUT MUST BE DECLARED** This should be a valid media/file link. [Learn More](https://trenalyze.com) |
| buttons | `array` | (OPTIONAL). **BUT MUST BE DECLARED** You can attach quick replies buttons to your message. [Learn More](https://trenalyze.com) |
| debug | `boolean` | (OPTIONAL). Default is false. But you can set it to be true and the debug message is passed onto the console. |

```python
# Set the Required Parameters for sending a message 
sender =  'YOUR_WHATSAPP_NUMBER'
receiver = 'RECIPIENT_NUMBER'
msgtext = 'Hello World'
mediaurl = 'https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png'
buttons = [
    ['index' => 1, 'urlButton' => ['displayText' => 'Visit my website!', 'url' => 'https://trenalyze.com']],
    ['index' => 2, 'callButton' => ['displayText' => 'Call me!', 'phoneNumber' => '+1 (234) 5678-9012']],
    ['index' => 3, 'quickReplyButton' => ['displayText' => 'This is a reply, just like normal buttons!', 'id' => 'id-like-buttons-message']]
]
```
**NOTE:** When not using **mediaurl** and **buttons** set to **NULL**
```python
mediaurl =  ''
buttons =  ''
```

### 3. Send The Required Variables

```python

trenalyze.setSender(sender)

trenalyze.setReceiver(receiver)

trenalyze.setMsgtext(msgtext)
```

**NOTE:** You can set Debug to True or False. It's False By default
```python
trenalyze.setDebug(True)
```

### 4. Initialize SendMessage

```python
# Initialize the send WhatsApp message functions
res = trenalyze.sendMessage()

print(res)
```

### 5. Sample Response

```js
{
    'status': True, 
    'response': {
        'message': 'Messages sent successfully'
    }
}
```