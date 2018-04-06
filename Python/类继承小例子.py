class Person(object):
    def __init__(self,name,sex):
        self.name = name
        self.sex = sex
        
    def print_title(self):
        if self.sex == "male":
            print("man")
        elif self.sex == "female":
            print("woman")

class Child(Person):     
    pass                       
    def __init__(self,name,sex,age):
        self.age = age
        Person.__init__(self,name,sex) # 注意这里

    def print_info(self):
        print 'age: ' + str(self.age)
        print 'name: ' + self.name
            
May = Child("May","female",3) # 注意这里的参数
Peter = Person("Peter","male")

print(May.name,May.sex,Peter.name,Peter.sex)    
May.print_title() # 调用父类方法
Peter.print_title()
May.print_info()

