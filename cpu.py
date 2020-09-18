"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.pc = 0
        self.reg = [0] * 8
        self.sp = 7
        self.fl = 0
    
    
    def ram_read(self,address):
        '''
        Read the information at the index in the RAM
        '''
        return self.ram[address]
    
    
    def ram_write(self,value,address):
        '''
        Writes a value in ram given the specified index
        '''
        self.ram[address] = value    
    def push(self,value):
        
        self.reg[self.sp] -= 1
        top_stack = self.reg[self.sp]
        self.ram[top_stack] = value

    def pop(self):
        top_stack = self.reg[self.sp]
        value = self.ram[top_stack]
        self.reg[self.sp] += 1
        return value
    def call(self):
        self.reg[self.sp] -= 1
        stack_address = self.reg[self.sp]

        return_address = self.pc + 2
        self.ram_write(stack_address,return_address)
        reg_num = self.ram_read(self.pc + 1)
        self.pc = self.reg[reg_num]
        return
    def ret(self):
        self.pc = self.ram_read(self.reg[self.sp])
        self.reg[self.sp] += 1
        return
    
    def cmp(self):
        r_a = self.ram_read(self.pc + 1)
        r_b = self.ram_read(self.pc + 2)

        val_a = self.reg[r_a]
        val_b = self.reg[r_b]

        if val_a == val_b:
            self.fl = 0b1
        elif val_a > val_b:
            self.fl = 0b10
        elif val_b > val_a:
            self.fl = 0b100
        self.pc += 3
        return           
    
    def jmp(self):
        reg_= self.ram_read(self.pc + 1)
        self.pc = self.reg[reg_]
        return
    
    def jne(self):
        if self.fl & 0b1:
            self.pc +=  2
        elif not self.fl & 0b0:
            reg_a = self.ram_read(self.pc + 1)
            self.pc = self.reg[reg_a]
        return
    
    def jeq(self):
        if not self.fl & 0b1:
            self.pc += 2
        elif self.fl & 0b1:
            reg_a = self.ram_read(self.pc + 1)
            self.pc  = self.reg[reg_a]
        return



    def load(self):
        """Load a program into memory."""
        if len(sys.argv) != 2:
            print('usage: ls8.py filename')
            sys.exit(1)
        try:
            address = 0
            with open(sys.argv[1]) as f:
                for line in f:
                    t = line.split('#')
                    n = t[0].strip()
                    if n == '':
                        continue
                    try:
                        n = '0b' + n
                        n = int(n,2)
                    except TypeError:
                        print(f'Number not valid {n}')
                        sys.exit(1)

                    self.ram_write(n,address)
                    address += 1
        except FileNotFoundError:
            print('file not found')
            sys.exit(2)                


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True
        # instructions!
        LDI = 0b10000010 
        PRN = 0b01000111
        MUL = 0b10100010
        HLT = 0b00000001
        PUSH = 0b01000101
        POP = 0b01000110
        CALL = 0b01010000
        RET = 0b00010001
        CMP = 0b10100111
        JMP = 0b01010100
        JNE = 0b01010110
        JEQ = 0b01010101
        


        
        while running:
            ir = self.ram[self.pc]
            
            
            if ir == LDI:
                reg_num = self.ram[self.pc + 1]
                value = self.ram[self.pc + 2]
                self.reg[reg_num] = value
                self.pc +=3
            
            elif ir ==  PRN:
                reg_num = self.ram[self.pc + 1]
                print(self.reg[reg_num])
                self.pc += 2
            
            elif ir ==  HLT:
                running = False

            elif ir == MUL:
                r1 = self.ram[self.pc + 1]
                r2 = self.ram[self.pc + 2]
                print(self.reg[r1] * self.reg[r2])
                self.pc += 3

            elif ir == POP:
                reg_num = self.ram[self.pc + 1]
                # top_stack = self.reg[self.sp]

                value = self.pop()
                
                self.reg[reg_num] = value
                # self.reg[self.sp] += 1
                
                self.pc += 2
            
            elif  ir == PUSH:
                # self.reg[self.sp] -= 1
                reg_num = self.ram[self.pc + 1]
                value = self.reg[reg_num]
                self.push(value)


                # top_stack = self.reg[self.sp]
                # self.ram[top_stack] = value
                self.pc += 2
            elif ir == CALL:
                self.call()
                # self.pc + 2
                # self.reg[self.sp] -= 1
                # stack_address = self.reg[self.sp]

                # return_address = self.pc + 2
                # self.ram_write(stack_address,return_address)
                # reg_num = self.ram_read(self.pc + 1)
                # self.pc = self.reg[reg_num]
                # retun_add = self.pc + 2

                # self.push(retun_add)

                # reg_num = self.ram[self.pc + 1]
                # value = self.reg[reg_num]
                # self.pc = value
            
            elif ir == RET:
                self.ret()
                # self.pc += 1
                # self.pc = self.ram_read(self.reg[self.sp])
                # self.reg[self.sp] += 1

            elif ir == JMP:
                self.jmp()
           
           
            elif ir == CMP:
                self.cmp()

            elif ir == JNE:
                self.jne()

            elif ir == JEQ:
                self.jeq()            





            
            else:
                print('unknown instruction')
                sys.exit(3)  


    




