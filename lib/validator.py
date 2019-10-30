import re


def is_valid_ipv4(ip):
    if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip):
        return True
    return False


def is_valid_ipv6(ip):
    """Validates IPv6 addresses.
    """
    pattern = re.compile(
        r"""
        ^
        \s*                         # Leading whitespace
        (?!.*::.*::)                # Only a single whildcard allowed
        (?:(?!:)|:(?=:))            # Colon iff it would be part of a wildcard
        (?:                         # Repeat 6 times:
            [0-9a-f]{0,4}           #   A group of at most four hexadecimal digits
            (?:(?<=::)|(?<!::):)    #   Colon unless preceeded by wildcard
        ){6}                        #
        (?:                         # Either
            [0-9a-f]{0,4}           #   Another group
            (?:(?<=::)|(?<!::):)    #   Colon unless preceeded by wildcard
            [0-9a-f]{0,4}           #   Last group
            (?: (?<=::)             #   Colon iff preceeded by exacly one colon
             |  (?<!:)              #
             |  (?<=:) (?<!::) :    #
             )                      # OR
         |                          #   A v4 address with NO leading zeros 
            (?:25[0-4]|2[0-4]\d|1\d\d|[1-9]?\d)
            (?: \.
                (?:25[0-4]|2[0-4]\d|1\d\d|[1-9]?\d)
            ){3}
        )
        \s*                         # Trailing whitespace
        $
    """, re.VERBOSE | re.IGNORECASE | re.DOTALL)
    if re.match(r'(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])', ip):
        return True
    return False


def is_valid_ip(ip):
    """Validates IP addresses.
		"""
    return is_valid_ipv4(ip) or is_valid_ipv6(ip)


def is_domain(value):
    pattern = re.compile(
        r'(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]'
    )

    if pattern.match(value):
        return True
    return False


def is_valid_host(host):
    return is_domain(host) or is_valid_ipv4(host)


def is_valid_port(port):
    if not str(port).isnumeric():
        return False
    if int(port) <= 65535 and int(port) >= 1:
        return True
    return False
