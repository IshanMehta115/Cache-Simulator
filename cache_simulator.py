def is_binary(add):
    for i in add:
        if(not i in ('0','1')):
            return False
    return True
def to_decimal(a):
    a = a[::-1]
    dec = 0
    for i in range(len(a)):
        if(a[i]=='1'):
            dec+=2**i
    return dec
def log2(a):
    a = a>>1
    log=0
    while(a>0):
        a = a>>1
        log+=1
    return log
class cache:
    def __init__(self,space,lines,block_size,n):
        self.space = space
        self.lines = lines
        self.block_size = block_size
        self.n_way = n
    def display(self):
        for i in self.space:
            for j in range(len(i)):
                if(j!=1):
                    if(j!=len(i)-1):
                        print(i[j],end=' , ')
                    else:
                        print(i[j],end='')
            print()
        print()
    def read_cache(self,address):
        global counter
        if(not is_binary(address) or len(address)!=address_bit_count):
            print("invalid address")
            return False
        else:
            start_line,end_line,tag,block_offset_decimal,set_number=self.write_preprocess(address)
            #print("preprocess",start_line,end_line,tag,block_offset_decimal)
            for i in range(start_line,end_line):
                if(self.space[i][0]==tag):
                    print("cache hit")
                    self.space[i][1]=counter
                    counter+=1
                    print(self.space[i][2:])
                    if(self.space[i][block_offset_decimal+2]=='filled'):
                        print("value of word - not specified")
                    else:
                        print("value of word - "+self.space[i][block_offset_decimal+2])
                    return True
            print("cache miss")
            return False
    def write_preprocess(self,address):
        block_offset_bits = log2(self.block_size)
        block_offset_binary = address[address_bit_count-block_offset_bits:]
        block_offset_decimal = to_decimal(block_offset_binary)
        block_number_binary = address[:address_bit_count-block_offset_bits]
        block_number_decimal = to_decimal(block_number_binary)
        if(choice[mapping_choice]=='fully'):
            return 0,self.lines,block_number_binary,block_offset_decimal,''
        else:
            total_sets = int(self.lines/self.n_way)
            target_set = int(block_number_decimal%total_sets)
            start_line = self.n_way*target_set
            end_line = start_line+self.n_way
            line_bits = log2(total_sets)
            tag = address[:address_bit_count-block_offset_bits-line_bits]
            return start_line,end_line,tag,block_offset_decimal,target_set
    
    def write_cache(self,address,value):
        value = value.split(" ")
        if(len(value)!=self.block_size):
            print("invalid data size")
            return False
        for i in value:
            if(i.isnumeric()==False):
                print("invalid data values")
                return False
        global cache
        global counter
        if(not is_binary(address) or len(address)!=address_bit_count):
            print("invalid address")
            return
        else:
            start_line,end_line,tag,block_offset_decimal,set_number=self.write_preprocess(address)
            #print("preprocess",start_line,end_line,tag,block_offset_decimal)
            #print("len_cache",len(cache))
            for i in range(start_line,end_line):
                if(self.space[i][0]==tag):
                    print("block already present")
                    return True
            filled = False
            for i in range(start_line,end_line):
                #print("line_number",i)
                if(self.space[i][0]=='empty'):
                    self.space[i][0]=tag
                    self.space[i][1]=counter
                    counter+=1
                    for j in range(2,block_size+2):
                        self.space[i][j]=value[j-2]
                    filled = True
                    break;
            if(not filled):
                print('over writing existing block')
                replace_index = start_line
                min_counter = self.space[replace_index][1]
                for i in range(start_line+1,end_line):
                    if(self.space[i][1]<min_counter):
                        min_counter = self.space[i][1]
                        replace_index = i
                if(set_number==''):
                    print("replaced block number = "+str(to_decimal(self.space[replace_index][0])))
                else:
                    print("replaced block number = "+str((to_decimal(self.space[replace_index][0])<<log2(int(self.lines/self.n_way)))+to_decimal(address[len(tag):address_bit_count-log2(self.block_size)])))
                self.space[replace_index][0]=tag
                self.space[replace_index][1]=counter
                counter+=1
                for j in range(2,block_size+2):
                    self.space[replace_index][j]=value[j-2]
                filled = True
            if(filled):
                #print("written successfully")
                return True
            else:
                #print("failed to write")
                return False

def is_power_2(a):
    while(a>0):
        if a&1==1:
            if(a==1):
                return True
            else:
                return False
        a=a>>1
    return False
def set_cache():
    cache=[]
    for i in range(cache_lines):
        temp = []
        for j in range(block_size+2):
            temp.append('empty')
        cache.append(temp)
    return cache
        
cache_size = -1
cache_lines = -1
block_size = -1
address_bit_count=16
n = -1
counter = 0
while(not(is_power_2(cache_size) and is_power_2(cache_lines) and is_power_2(block_size) and cache_size==cache_lines*block_size)):
    cache_size = int(input("Enter cache size "))
    cache_lines = int(input("Enter cache lines "))
    block_size =int(input("Enter block size "))
mapping_choice = -1
choice = {1:"direct",2:"fully",3:"n-way"}
while(not mapping_choice in choice):
    mapping_choice= int(input("Press 1 for direct mapping/nPress 2 for Associative mapping/nPress 3 for n - way set associative/n"))
if(choice[mapping_choice]=='n-way'):
    while(not is_power_2(n)):
        n = int(input("Enter value of n in n-way mapping (number of blocks per set)\n"))
if(choice[mapping_choice]=='direct'):
    n = 1
if(choice[mapping_choice]=='fully'):
    n = cache_lines
print(choice[mapping_choice])
print(n)
empty_cache = set_cache()
cache1 = cache(empty_cache,cache_lines,block_size,n)
cache1.display()
operation = ''
while(operation!='q' and operation!='Q'):
    operation = input("Press 1 to read\nPress 2 to write\nPress q to quit\n")
    if(operation=='1'):
        cache_address = input("Enter address in binary\n")
        if(cache1.read_cache(cache_address)==True):
            print("success!")
        else:
            print("fail!")
    if(operation=='2'):
        physical_address = input("Enter the address in binary\n")
        value = input("Enter the value of words in binary")
        if(cache1.write_cache(physical_address,value)==True):
            print("success!")
        else:
            print("fail!")
    cache1.display()
