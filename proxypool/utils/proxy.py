import requests

from proxypool.schemas import Proxy


def test_ip_active(ip):
    try:
        _ = requests.get('http://icanhazip.com/', proxies={"http": 'http://' + ip}, timeout=0.1)
        return True
    except:
        print("失效代理：" + ip)
        return False


def is_valid_proxy(data):
    if not test_ip_active(data):
        return False

    """
    check this string is within proxy format
    """
    if data.__contains__(':'):
        ip = data.split(':')[0]
        port = data.split(':')[1]
        return is_ip_valid(ip) and is_port_valid(port)
    else:
        return is_ip_valid(data)


def is_ip_valid(ip):
    """
    check this string is within ip format
    """
    a = ip.split('.')
    if len(a) != 4:
        return False
    for x in a:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True


def is_port_valid(port):
    return port.isdigit()


def convert_proxy_or_proxies(data):
    """
    convert list of str to valid proxies or proxy
    :param data:
    :return:
    """
    if not data:
        return None
    # if list of proxies
    if isinstance(data, list):
        result = []
        for item in data:
            # skip invalid item
            item = item.strip()
            if not is_valid_proxy(item): continue
            host, port = item.split(':')
            result.append(Proxy(host=host, port=int(port)))
        return result
    if isinstance(data, str) and is_valid_proxy(data):
        host, port = data.split(':')
        return Proxy(host=host, port=int(port))
