import pymongo
import dns
import random
import telnetlib
import re
import time
from dns import resolver

class verification():
    def __init__(self,address):
        """
        initialize the usual mx server
        :param address:the address of email
        """
        # print("init")
        #the list is got from the dig tool in linux
        self.address = address
        #get the domain of the email address
        self.domain = self.address.split('@')[-1]
        #database initialization
        self.client = pymongo.MongoClient('localhost',27017)
        self.db = self.client.email
        self.collection = self.db.mx_server
        self.posts = self.db.posts
        self.failed_times = 0

    def get_mx_server(self,domain):
        """
        find it and insert it into database
        :return: a list of mx server
        """
        # print("get mx server")
        try:
            ans = resolver.query(domain,"MX")
            list_mx = []
            for i in ans.response.answer:
                line = str(i).split('\n')
                for l in line:
                    # print(l.split(' ')[-1])
                    mx_server = l.split(' ')[-1]
                    list_mx.append(mx_server)
            self.collection.insert_one({"domain":self.domain,"mx_server":list_mx})
        except dns.resolver.NXDOMAIN:
            list_mx = []
        except dns.resolver.NoAnswer :
            list_mx = []
        except dns.resolver.NoNameservers:
            list_mx = []
        return list_mx

    def get_random_server(self,domain):
        """
        just get a server randomly...
        :return: a server which is selected randomly
        """
        # print("get server randomly")
        js= self.collection.find_one({"domain":self.domain})
        # print(type(js))
        server_list = js["mx_server"]
        num = random.randint(0,len(server_list)-1)
        return server_list[num]

    def find(self,domain):
        """
        confirm if the domain is in the db
        :return: a bool value
        """
        # print("finding")
        r = self.collection.find_one({"domain":domain})
        if r == None:
            result = False
        else:
            result = True
        return result

    def telnet_handle(self,address,server):
        # print("telnet handling")
        try:
            tn = telnetlib.Telnet(server, 25)
        except Exception as e:
            print(e)
            return False
        try:
            tn = telnetlib.Telnet(server, 25)
            #just some normal telnet operation
            tn.write("HELO verify.com".encode('ascii')+b'\r\n')
            tn.write(("MAIL FROM:<noreply@verifyemailaddress.com>").encode('ascii')+b"\n")
            tn.write((("RCPT TO:<%s>")%(address)).encode('ascii')+b"\r\n")
            out =str(tn.read_until(b"/r/n/r/n#>",4)).lower()
            if len(re.findall(r"550|not found|501",out)) > 0:
                result = False
            else:
                result = True
            tn.close()
            time.sleep(0.2)
            return result
        except Exception as e:
            tn.close()
            print(e)
            time.sleep(5)
            self.failed_times = self.failed_times + 1
            if self.failed_times > 5:
                pass
            else:
                self.telnet_handle(self.address,server)
            return False


    def verify(self):
        """
        the main function to verify the email address
        :return: a bool value
        """
        # print("verifying")
        #the first branch is to choose mx server by the way to confirm if the domain exists
        mx_server = []
        if not self.find(self.domain):
            #if the domain isn't in the db,then write it in the db or..find if it doesn't exist
            mx_server = self.get_mx_server(self.domain)
        else:
            mx_server = self.collection.find_one({"domain":self.domain})

        if mx_server == []:
                result = False
        else:
            server = self.get_random_server(self.domain)
            result = self.telnet_handle(self.address,server)

        return result



if __name__ == "__main__":
    a = verification("009@usa.com").verify()
    print(a)#true or false
    # print(type(str(a)))
    """
    with open("/home/scy/temp/China_emails.txt",'r') as f:
        for line in f:
            a = time.time()
            print(verification(line.strip('\n')).verify(),line.strip("\n"))
            b = time.time()
            print(b-a)
    """
