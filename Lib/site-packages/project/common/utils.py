# -*- coding: utf-8 -*-
# @Time     : 2020/7/24 9:56 上午
# @Author   : binger
import struct
import socket


def parse_boolean(s):
    """Takes a string and returns the equivalent as a boolean value."""
    s = s.strip().lower()
    if s in ('yes', 'true', 'on', '1'):
        return True
    elif s in ('no', 'false', 'off', '0', 'none'):
        return False
    else:
        raise ValueError('Invalid boolean value %r' % s)


def int_or_none(value):
    if value is None:
        return value

    return int(value)


def load_address_range(ip_section):
    import IPy
    ip_ran = IPy.IP(ip_section)
    return ip_ran[0].int(), ip_ran[-1].int()


def find_ip(start, end):
    assert type(start) == type(end)
    ip_struct = struct.Struct('>I')
    if not isinstance(start, int):
        start = ip_struct.unpack(socket.inet_aton(start))[0]
        end = ip_struct.unpack(socket.inet_aton(end))[0]
    return map(lambda i: socket.inet_ntoa(ip_struct.pack(i)), range(start, end + 1))


def ip2int(ip):
    ip_struct = struct.Struct('>I')
    return ip_struct.unpack(socket.inet_aton(ip))[0]


def combined_address(ip_section_list: list):
    def _load_address_ran(ips):
        return (*IP(ips=ips).ran, ips)

    from operator import itemgetter

    ip_section_list = sorted(
        map(lambda ip_section: _load_address_ran(ip_section), ip_section_list),
        key=itemgetter(0)
    )
    for i in range(len(ip_section_list) - 1, -1, -1):
        cur = ip_section_list[i]
        for dst in ip_section_list[:i]:
            if cur[1] <= dst[1]:
                # 合并
                ip_section_list.pop(i)
                break

    return (resp[-1] for resp in ip_section_list)


class IP(object):
    def __init__(self, ips: str):
        self._ips = ips
        sep = "-"
        if sep in ips:
            self.start, self.end = list(map(ip2int, ips.split(sep, 1)))
        else:
            self.start, self.end = load_address_range(ips)

    @property
    def ran(self):
        return self.start, self.end

    def to_list(self):
        return list(find_ip(self.start, self.end))

    def __str__(self):
        return self._ips

    def __iter__(self):
        return find_ip(self.start, self.end)


from funcy import colls


def project_cb(mapping, keys, handle_key):
    """Leaves only given keys in mapping, And convert the keys"""
    return colls._factory(mapping)((handle_key(k), mapping[k]) for k in keys if k in mapping)


def project_mapper(mapping, key_mapper: dict, keep_key=False):
    """Leaves only given keys in mapping, And map the keys"""
    if keep_key:
        return colls._factory(mapping)((v, mapping.get(k)) for k, v in key_mapper.items())
    else:
        return colls._factory(mapping)((v, mapping[k]) for k, v in key_mapper.items() if k in mapping)


def project_clear(mapping, keys, clear_value_at=None):
    """
    Leaves only given keys in mapping and clear value in clear_value_at'set
    :param mapping:
    :param keys:
    :param clear_value_at: [None, ]
    :return:
    """
    clear_value_at = clear_value_at or [None]

    def handle(k, sep="__"):
        v = mapping.get(k, "__")
        return not (v == sep or v in clear_value_at)

    return colls._factory(mapping)((k, mapping[k]) for k in keys if handle(k))


def project_require(mapping, keys, cb_at_no=None):
    """
    Leaves given keys must in mapping
    :param mapping:
    :param keys:
    :param cb_at_no:
    :return:
    """
    if not cb_at_no:
        def cb_at_no(k):
            raise ValueError("Expected key({}) does not exist！".format(k))

    def func(k):
        if k in mapping:
            return True
        else:
            cb_at_no(k)
            return False

    if isinstance(keys, dict):
        seq = [(v, mapping[k]) for k, v in keys.items() if func(k)]
    else:
        seq = [(k, mapping[k]) for k in keys if func(k)]
    return colls._factory(mapping)(seq)


if __name__ == "__main__":
    ip_section_list = ["192.168.0.100-192.168.0.130", '192.168.0.100', "192.168.0.102",
                       "192.168.0.120-192.168.0.130", "192.168.0.125-192.168.0.140", '192.168.0.150']
    a = combined_address(ip_section_list)
    print(a)
    print('192.168.0.171' in IP('192.168.0.100-192.168.0.252'))
