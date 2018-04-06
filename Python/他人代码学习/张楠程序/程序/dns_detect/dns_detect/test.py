import os
import re
def jp_manage(domain):
    

    # command = 'whois ' + domain
    command = 'whois ureru.co.jp'
    result = os.popen(command)
    data_result = result.read()

    domain_info = {}
    pattern = re.compile(r'(\[Name\].*|\[Phone\].*|\[Email\].*|\[Administrative Contact\].*)')
    match = pattern.findall(data_result)
    # print match[0].split(']')
    # print match[0].split('')[2:]
    count = len(match)
    # print data_result
    for i in range(count):

        if match[i].split(' ')[0].strip()=='[Name]':
            domain_info['reg_name'] = match[i][6:].strip()
        elif match[i].split(' ')[0].strip()=='[Phone]':
            domain_info['reg_phone'] = match[i][7:].strip()
        elif match[i].split(' ')[0].strip()=='[Email]':
            domain_info['reg_email'] = match[i][7:].strip()
        elif match[i].split(']')[0].strip()=='[Administrative Contact':
            domain_info['reg_name'] = match[i][24:].strip()
    # domain_info['detail'] = str(data_result)
    # print domain_info
    
    return domain_info

jp_manage(domain = 'ureru.co.jp')
