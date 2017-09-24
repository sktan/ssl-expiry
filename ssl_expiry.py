""" Script to determine the expiry of SSL certificates """
# pylint: disable=W0703
import socket
import ssl
import datetime

def ssl_expiry_datetime(hostname, port=443):
    ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'

    context = ssl.create_default_context()
    conn = context.wrap_socket(
        socket.socket(socket.AF_INET),
        server_hostname=hostname,
    )
    # 3 second timeout because Lambda has runtime limitations
    conn.settimeout(3.0)

    conn.connect((hostname, port))
    ssl_info = conn.getpeercert()
    # parse the string from the certificate into a Python datetime object
    return datetime.datetime.strptime(ssl_info['notAfter'], ssl_date_fmt)

def ssl_valid_time_remaining(hostname, port=443):
    """Get the number of days left in a cert's lifetime."""
    expires = ssl_expiry_datetime(hostname, port)
    return expires - datetime.datetime.utcnow()

def check_ssl_expiry(hostname, port=443, warning_buffer=30, critical_buffer=7):
    days = ssl_valid_time_remaining(hostname, port).days
    if days < 0:
        print("FAILED: Certificate for {0} has already expired".format(hostname))
    elif days < critical_buffer:
        print("CRITICAL: Certificate for {0} is nearing expiry ({1} days)".format(
            hostname, days
        ))
    elif days < warning_buffer:
        print("WARNING: Certificate for {0} is nearing expiry ({1} days)".format(
            hostname, days
        ))
    else:
        print("OK: Certificate for {0} is not anytime expiring soon ({1} days)".format(
            hostname, days
        ))

with open("hosts.txt") as file:
    for line in file:
        line = line.replace("\n", "")
        port = 443
        # Determine if a port exist:
        # www.example.com or www.example.com:8443
        if ":" in line:
            split_host = line.split(":")
            port = int(split_host[1])
            hostname = split_host[0]
        else:
            hostname = line
        # Attempt the SSL certificate check
        try:
            check_ssl_expiry(hostname, port)
        except Exception as err:
            print("WARNING: Could not connect to {0}: {1}".format(
                hostname,
                err
            ))
