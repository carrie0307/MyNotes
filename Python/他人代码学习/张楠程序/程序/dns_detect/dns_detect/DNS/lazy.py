
# routines for lazy people.
import Base

from Base import ServerError

def revlookup(name):
    "convenience routine for doing a reverse lookup of an address"
    names = revlookupall(name)
    if not names: return None
    return names[0]     # return shortest name

def revlookupall(name):
    "convenience routine for doing a reverse lookup of an address"
    # FIXME: check for IPv6
    a = name.split('.')
    a.reverse()
    b = '.'.join(a)+'.in-addr.arpa'
    names = dnslookup(b, qtype = 'ptr')
    # this will return all records.
    names.sort(key=str.__len__)
    return names

def dnslookup(name,qtype):
    "convenience routine to return just answer data for any query type"
    if Base.defaults['server'] == []: Base.DiscoverNameServers()
    result = Base.DnsRequest(name=name, qtype=qtype).req()
    if result.header['status'] != 'NOERROR':
        raise ServerError("DNS query status: %s" % result.header['status'],
            result.header['rcode'])
    elif len(result.answers) == 0 and Base.defaults['server_rotate']:
        # check with next DNS server
        result = Base.DnsRequest(name=name, qtype=qtype).req()
    if result.header['status'] != 'NOERROR':
        raise ServerError("DNS query status: %s" % result.header['status'],
            result.header['rcode'])
    return [x['data'] for x in result.answers]

def mxlookup(name):
    """
    convenience routine for doing an MX lookup of a name. returns a
    sorted list of (preference, mail exchanger) records
    """
    l = dnslookup(name, qtype = 'mx')
    l.sort()
    return l


