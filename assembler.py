def mot(op):
        if op == "stop":
                return "00"
        elif op == "add":
                return "01"
        elif op == "sub":
                return "02"
        elif op == "mult":
                return "03"
        elif op == "mover":
                return "04"
        elif op == "movem":
                return "05"
        elif op == "comp":
                return "06"
        elif op == "bc":
                return "07"
        elif op == "div":
                return "08"
        elif op == "read":
                return "09"
        elif op == "print":
                return "10"
        elif op == "jmp":
                return "11"
        elif op == "xchg":
                return "12"
        elif op == "store":
                return "13"
        elif op == "int":
                return "14"
        else:
                return ""

def pot1(op):
        if op == 'start':
                return "01"
        elif op == "end":
                return "02"
        elif op == "equ":
                return "03"
        elif op == "origin":
                return "04"
        elif op == "ltorg":
                return "05"
        else:
                return ""

def pot2(op):
        if op == "dc":
                return "01"
        elif op == "ds":
                return "02"
        else:
                return ""
        
def regt(re):
        if re == "reg1" or re == "areg":
                return "1"
        elif re == "reg2" or re == "breg":
                return "2"
        elif re == "reg3" or re == "creg":
                return "3"
        elif re == "reg4" or re == "dreg":
                return "4"
        else:
                return ""

def brin(bi):
        if bi == "lt":
                return "1"
        elif bi == "le":
                return "2"
        elif bi == "eq":
                return "3"
        elif bi == "gt":
                return "4"
        elif bi == "ge":
                return "5"
        elif bi == "any":
                return "6"
        else:
                return ""

with open("alp.txt", "r") as f:
        content = f.readlines()

content = [x.strip() for x in content]

lbl = [None] * len(content)
list1 = [""] * len(content)
list2 = [""] * len(content)
op = [None] * len(content)
oprd = [None] * len(content)
oprd1 = [None] * len(content)
oprd2 = [""] * len(content)
oprd3 = [""] * len(content)
op_l = [None] * len(content)
brin_li = [""] * len(content)
li = [""] * len(content)
sy = [""] * len(content)
lc = [0] * len(content)
smbl = [0] * len(content)
adr = [0] * len(content)
lit = [0] * len(content)
adr_l = [0] * len(content)
clc = 0
counter = 0
counter_l = 0
for i in range(len(content)):
        lbl[i], op[i], oprd[i] = content[i].split()
        try:
                oprd1[i], oprd2[i] = oprd[i].split(',') 
        except ValueError:
                oprd1[i] = "xxx"                
                oprd2[i] = oprd[i]
        if lbl[i] == ".":
                del smbl[-1]
                del adr[-1]
        if oprd[i][0] != "=":
                del lit[-1]
                del adr_l[-1]

for i in range(len(content)):
        #Setting opcodes for the Mnemonics in the below section of if/else statements   
        if op[i] == "start" or op[i] == "end" or op[i] == "equ" or op[i] == "origin" or op[i] == "ltorg":
                op_l[i] = "(AD,"+pot1(op[i])+")"
                list1[i] = pot1(op[i])
        elif op[i] == "dc" or op[i] == "ds":
                op_l[i] = "(DL,"+pot2(op[i])+")"
                list1[i] = pot2(op[i])
        elif op[i] == "stop" or op[i] == "add" or op[i] == "sub" or op[i] == "mult" or op[i] == "mover" or op[i] == "movem" or op[i] == "comp" or op[i] == "bc" or op[i] == "div" or op[i] == "read" or op[i] == "print" or op[i] == "jmp" or op[i] == "xchg" or op[i] == "store" or op[i] == "int":
                op_l[i] = "(IS,"+mot(op[i])+")"
                list1[i] = mot(op[i])
        else:
                op_l[i] = ""
                list1[i] = ""
        

        #Setting Location for the following Mnemonics in the below section of i/e statements
        if  op[i] == "start":
                lc[i] = ""
                clc = int(oprd[i])
                li[i]= "(c,"+oprd[i]+")"
        elif op[i] == "start" or op[i] == "end" or op[i] == "equ" or op[i] == "origin" or op[i] == "ltorg":
                lc[i] = ""
                if op[i] == "origin":
                        j = smbl.index(oprd[i])
                        clc = adr[j]
        elif op[i] == "ds":
                clc = clc + int(oprd[i])
                lc[i] = clc
        elif op[i-1] == "start":
                lc[i] = clc
        else:
                clc = clc + 1
                lc[i] = clc

        #Setting symbols and address for the symbol table
        if lbl[i] != ".":
                if op[i] == "equ":
                        j = smbl.index(oprd[i])
                        adr[counter] = adr[j]
                        smbl[counter] = lbl[i]
                        counter = counter + 1
                else:
                        smbl[counter] = lbl[i]
                        adr[counter] = lc[i]
                        counter = counter + 1
        #Setting Literal table
        if oprd[i][0] == "=":
                lit[counter_l] = oprd[i]
                adr_l[counter_l] = lc[i]
                counter_l = counter_l + 1
        #setting branch instructions
        if oprd1[i] == "lt" or oprd1[i] == "le" or oprd1[i] == "eq" or oprd1[i] == "gt" or oprd1[i] == "ge" or oprd1[i] == "any":
                brin_li[i] = brin(oprd1[i])
        else:
                brin_li[i] = regt(oprd1[i])

for i in range(1,len(content)):   
        if oprd2[i] == '.' or oprd2[i][0] == "'" or oprd2[i].isdigit() == True:
                continue
        else:
                if oprd2[i][0] == "=":
                        li[i] = "(L,"+str(lit.index(oprd2[i])+1)+")"
                        list2[i] = adr_l[lit.index(oprd2[i])]
                        continue
                li[i] = "(S,"+str(smbl.index(oprd2[i])+1)+")"
                list2[i] = adr[smbl.index(oprd2[i])]

        if oprd1 != "xxx":
                li[i] = "(S,"+str(smbl.index(oprd2[i])+1)+")"
                list2[i] = adr[smbl.index(oprd2[i])]


f.close()

with open("pass1/target_code.csv", "w") as f1:
        f1.write("Location counter;Intermediate code\n")
        for i in range(len(content)):
                f1.write(str(lc[i])+";"+str(op_l[i])+" "+str(brin_li[i])+str(li[i]))
                f1.write("\n")
f1.close()
with open("pass1/symbol_table.csv", "w") as f2:
        f2.write("S.no; Symbol;Address\n")
        for i in range(len(smbl)):
                f2.write(str(i+1)+";"+str(smbl[i])+";"+str(adr[i]))
                f2.write("\n")
f2.close()
with open("pass1/literal_table.csv", "w") as f3:
        f3.write("S.no;Literal;Address\n")
        for i in range(len(lit)):
                f3.write(str(i+1)+";"+str(lit[i])+";"+str(adr_l[i]))
                f3.write("\n")
f3.close()
with open("pass2/pass2.csv", "w") as f4:
        f4.write("opcode;reg/branch ins.;Address\n")
        for i in range(len(content)):
                f4.write(str(list1[i]+";"+str(brin_li[i])+";"+str(list2[i])))
                f4.write("\n")
f4.close()
