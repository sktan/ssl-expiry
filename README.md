# SSL Expiry
Checks a list of URLs to determine their HTTPS certificate expiry

## Usage
1. Download or clone this repo
2. Install Python
3. Modify hosts.txt to include your hosts
4. Run the script via Python

``` 
python ssl_expiry.py
```

## Example hosts.txt
```
# Google
www.google.com

# Example
www.example.com

# Non Existant
www.non-existant.com:1234
```

## Example Output
```
OK: Certificate for www.google.com is not anytime expiring soon (73 days)
OK: Certificate for www.example.com is not anytime expiring soon (429 days)
WARNING: Could not connect to www.non-existant.com: [Errno 11001] getaddrinfo failed
```
