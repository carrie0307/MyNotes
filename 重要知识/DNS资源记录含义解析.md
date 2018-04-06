# DNS资源记录解析


* 核心文档：[RFC-1035:DOMAIN NAMES - IMPLEMENTATION AND SPECIFICATION](https://www.ietf.org/rfc/rfc1035.txt)

* 相关文档：[RFC-1034: DOMAIN NAMES - CONCEPTS AND FACILITIES](https://www.ietf.org/rfc/rfc1034.txt)

---

## RR(资源记录) Format

|NAME|
|:--:|
|TYPE|
|CLASS|
|TTL|
|RDLENGTH|
|RDATA|

## Type Values

|TYPE|value and meaning|
|:--:|:--:|
|A         |  a host addressv|
|NS       |   an authoritative name server|
|MD       |   a mail destination (Obsolete - use MX)|
|MF       |   a mail forwarder (Obsolete - use MX)|
|CNAME    |   the canonical name for an alias|
|SOA      |   marks the start of a zone of authority|
|MB       |    a mailbox domain name (EXPERIMENTAL)|
|MG       |   a mail group member (EXPERIMENTAL)|
|MR       |    a mail rename domain name (EXPERIMENTAL)|
|NULL     |     a null RR (EXPERIMENTAL)|
|WKS      |    a well known service description|
|PTR      |    a domain name pointer|
|HINFO    |    host information|
|MINFO    |     mailbox or mail list information|
|MX       |   mail exchange|
|TXT      |     text strings|

## Class Values

|TYPE|value and meaning|
|:--:|:--:|
|IN  | the Internet|
|CS  |  the CSNET class (Obsolete - used only for examples in                some obsolete RFCs)|
|CH   | the CHAOS class|
|HS   |4 Hesiod [Dyer 87]|

## A记录
略

## NS记录
略

## 几个资源记录解释

### SOA

* SOA记录由7部分组成：


* MNAME :The <domain-name> of the name server that was the **original or primary source of data for this zone**.

* RNAME:A <domain-name> which specifies the mailbox of the person responsible for this zone.

* SERIAL:The unsigned 32 bit version number of the original copy
of the zone.  Zone transfers preserve this value. This value wraps and should be compared using sequence space arithmetic.

* REFRESH:A 32 bit time interval before the zone should be refreshed.

*RETRY:A 32 bit time interval that should elapse before a failed refresh should be retried.

* EXPIRE: A 32 bit time value that specifies the upper limit on
 the time interval that can elapse before the zone is no longer authoritative.


* 其他两篇参考文章：
    * http://www.sigma.me/2011/01/01/about_dns_soa.html
    * http://www.sigma.me/2011/01/01/about_dns_soa.html

### MX

* Definition: MR records cause no additional section processing.  The main use for MR is as a forwarding entry for a user who has moved to a different mailbox.

* MX记录包含两部分

    * PREFERENCE: A 16 bit integer which specifies the preference given to this RR among others at the same owner.  Lower values are preferred.

    * EXCHANGE : A <domain-name> which specifies a host willing to act as a mail exchange for the owner name.



### TXT

* Definition: TXT RRs are used to hold descriptive text.  The semantics of the text depends on the domain where it is found.



