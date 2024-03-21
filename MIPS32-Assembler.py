# code = utf-8

import json
import sys



class UsageException(Exception):
    def __init__(self, msg:str) -> None:
        self.msg = msg



class Statement(object):
    '''语句类'''
    @staticmethod
    def initLabelDict() -> None:
        Statement.labelAddress = {}


    @staticmethod
    def setCommands(COMMANDS:dict) -> None:
        Statement.COMMANDS = COMMANDS

    
    @staticmethod
    def setStartAddress(STARTADDRESS:int) -> None:
        Statement.STARTADDRESS = STARTADDRESS


    def __init__(self, initTuple:tuple[list, str], index:int) -> None:
        self.labels, self.statement = initTuple
        self.address = index
        for label in self.labels:
            Statement.labelAddress[label] = index
        

    @staticmethod
    def pretreat(asmLines:list[str]):
        for i in range(len(asmLines)):
            sharpIndex = asmLines[i].find('#')
            if sharpIndex == -1:
                asmLines[i] = asmLines[i].strip().replace(':', ':\n')
            else:
                asmLines[i] = asmLines[i][0 : sharpIndex].strip().replace(':', ':\n')
        
        asmLines = '\n'.join(asmLines)
        
        return (asmLine for asmLine in asmLines.split('\n') if asmLine != '')
    

    @staticmethod
    def formStatement(asmLines) -> tuple[list, str]:
        try:
            labels = []
            asmLine = next(asmLines)
            while asmLine.endswith(':'):
                labels.append(asmLine[0 : -1])
                asmLine = next(asmLines)

            return labels, asmLine
        
        except StopIteration:
            if labels == []:
                raise UsageException('End of asmLines')
            
            return labels, 'nop'
        

    @staticmethod
    def foundRegister(reg:str) -> int:
        if reg[1].isdigit():
            return int(reg[1 : ])
        
        match reg[1]:
            case 'z':
                return 0
            
            case 'a':
                if reg[2] == 't':
                    return 1
                return int(reg[2]) + 4
            
            case 'v':
                return int(reg[2]) + 2
            
            case 't':
                if int(reg[2]) <= 7:
                    return int(reg[2]) + 8
                return int(reg[2]) + 16
            
            case 's':
                if reg[2] == 'p':
                    return 29
                return int(reg[2]) + 16
            
            case 'g':
                return 28
            case 'f':
                return 30
            case 'r':
                return 31
        
        return Statement.REGISTERS[reg[1 : ]]
    

    @staticmethod
    def transImmediate(imm:str) -> int:
        if imm == '':
            return 0

        if imm[0] == '-':
            return -Statement.transImmediate(imm[1 : ])
        
        if imm[0] == '0':
            if imm[1] == 'x':
                return int(imm[2 : ], 16)
            
            if imm[1] == 'b':
                return int(imm[2 : ], 2)
            
            return int(imm[1 : ], 8)
        
        return int(imm)
                

    @staticmethod
    def judgeType(words:list) -> tuple[str, list]:
        argStr = ''
        pureContent = []

        for word in words:
            if word[0] == '$':
                pureContent.append(Statement.foundRegister(word))
                argStr += 'r'
            
            elif word[0].isdigit() or word[0] == '-' or word[0] == '(':
                leftParenIndex = word.find('(')
                if leftParenIndex == -1:
                    pureContent.append(Statement.transImmediate(word))
                    argStr += 'i'
                else:
                    pureContent.append(Statement.transImmediate(word[0 : leftParenIndex]))
                    argStr += 'o'
                    pureContent.append(Statement.foundRegister(word[leftParenIndex+1 : -1]))
                    argStr += 'b'
        
            else:
                pureContent.append(word)
                argStr += 'l'

        return argStr, pureContent
       
    
    def splitStatement(self) -> None:
        rwords = self.statement.split(' ')
        words = []
        [words.append(word.rstrip(',')) for word in rwords]
        self.cmd = words[0]
        
        try:
            cmdMsg = Statement.COMMANDS[self.cmd]
        except KeyError as keyerr:
            raise UsageException('Command ' + str(keyerr) + ' not in the command list')
        
        self.typ = cmdMsg[0]
        if self.typ in ['R', 'S', 'E']:
            self.funct = cmdMsg[3]
        elif self.typ == 'Z':
            self.branchType = cmdMsg[3]

        self.opcode = cmdMsg[2]
    
        self.argStr, self.pureContent = Statement.judgeType(words[1 : ])
        
        if self.argStr != cmdMsg[1]:
            raise UsageException('Unmatch Statement')

    
    @staticmethod
    def bitBin(i:int, bit:int) -> str:
        if i < 0:
            i += 2 ** bit

        b = bin(i)[2 : ]        
        return (bit - len(b)) * '0' + b
    

    def calcBranchOffset(self) -> str:
        if self.typ == 'B':
            offset = Statement.labelAddress[self.pureContent[2]] - self.address - 1
        else:
            offset = Statement.labelAddress[self.pureContent[1]] - self.address - 1
        return Statement.bitBin(offset, 16)
        

    def calcJumpAddress(self) -> str:
        target = Statement.labelAddress[self.pureContent[0]] * 4 + Statement.STARTADDRESS
        return Statement.bitBin(target, 28)[ : -2]


    def setHexMachineCode(self) -> None:
        xCode = hex(int(self.bMachineCode, base=2))[2 : ]
        self.xMachineCode = (8 - len(xCode)) * '0' + xCode


    def toMachineCode(self) -> None:
        self.bMachineCode = Statement.bitBin(int(self.opcode, base=16), 6)

        match self.typ:
            case 'R':
                for i in [1, 2, 0]:
                    if i < len(self.pureContent):
                        self.bMachineCode += Statement.bitBin(self.pureContent[i], 5)
                    else:
                        self.bMachineCode += '0' * 5
                self.bMachineCode += '0' * 5 \
                                   + Statement.bitBin(int(self.funct, base=16), 6)

            case 'I':
                self.bMachineCode += Statement.bitBin(self.pureContent[1], 5) \
                                   + Statement.bitBin(self.pureContent[0], 5) \
                                   + Statement.bitBin(self.pureContent[2], 16)

            case 'M':
                self.bMachineCode += Statement.bitBin(self.pureContent[2], 5) \
                                   + Statement.bitBin(self.pureContent[0], 5) \
                                   + Statement.bitBin(self.pureContent[1], 16)

            case 'B':
                self.bMachineCode += Statement.bitBin(self.pureContent[0], 5) \
                                   + Statement.bitBin(self.pureContent[1], 5) \
                                   + self.calcBranchOffset()

            case 'Z':
                self.bMachineCode += Statement.bitBin(self.pureContent[0], 5) \
                                   + Statement.bitBin(int(self.branchType, base=16), 5) \
                                   + self.calcBranchOffset()
                        
            case 'J':
                self.bMachineCode += self.calcJumpAddress()

            case 'L':
                self.bMachineCode += '0' * 5 \
                                   + Statement.bitBin(self.pureContent[0], 5) \
                                   + Statement.bitBin(self.pureContent[1], 16)
            
            case 'E':
                self.bMachineCode += Statement.bitBin(self.pureContent[0], 5) \
                                   + '0' * 15 \
                                   + Statement.bitBin(int(self.funct, base=16), 6)
                
            case 'S':
                self.bMachineCode += '0' * 5 \
                                   + Statement.bitBin(self.pureContent[1], 5) \
                                   + Statement.bitBin(self.pureContent[0], 5) \
                                   + Statement.bitBin(self.pureContent[2], 5) \
                                   + Statement.bitBin(int(self.funct, base=16), 6)
                

        self.setHexMachineCode()


    def getMachineCode(self) -> str:
        return self.xMachineCode

        


def argManage(argv:list[str]) -> tuple[str,]:
    if len(argv) not in [2, 3]:
        raise UsageException('ArgNum Error')
    
    match len(argv):
        case 2:
            return (argv[1], argv[1][0 : argv[1].rfind('.')] + '.txt')
        
        case 3:
            return (argv[1], argv[2])



def readJsonFile(filename:str, content:str) -> dict:
    try:
        fp = open(filename, 'r')
        return json.loads(fp.read())
    
    except FileNotFoundError:
        raise UsageException(content + ' Not Found')
    
    finally:
        fp.close()



def openAsm(asmFilename:str) -> list:
    try:
        fp = open(asmFilename, 'r')
        return fp.readlines()

    except FileNotFoundError:
        raise UsageException('asmFile Not Found')
    
    finally:
        fp.close()



def writeMacineCode(outputFilename:str, statements:list[Statement]) -> None:
        fp = open(outputFilename, 'w')

        [fp.write(statement.getMachineCode() + '\n') for statement in statements]

        return
        



def main():
    try:
        asmFilename, outputFilename = argManage(sys.argv)

        COMMANDS = readJsonFile('./command.json', 'commandFile')
        Statement.setCommands(COMMANDS)
        
        asmLines = openAsm(asmFilename)

        Statement.initLabelDict()

        asmLines = Statement.pretreat(asmLines)

        statements = []
        index = 0
        try:
            while True:
                initTuple = Statement.formStatement(asmLines)
                statements.append(Statement(initTuple, index))
                index += 1

        except UsageException:
            pass

        [statement.splitStatement() for statement in statements]

        STARTADDRESS = 0x400000
        Statement.setStartAddress(STARTADDRESS)

        [statements[i].toMachineCode() for i in range(len(statements))]

        writeMacineCode(outputFilename, statements)


    except UsageException as e:
        print(e.msg)
    
if __name__ == '__main__':
    main()