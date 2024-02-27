# code = utf-8

import json
import sys
import re



class UsageException(Exception):
    def __init__(self, msg:str) -> None:
        self.msg = msg



class Statement(object):
    '''语句类'''
    def __init__(self, initTuple:tuple[list, str]) -> None:
        self.labels = initTuple[0]
        

    @staticmethod
    def pretreat(asmLines:list):
        for i in range(len(asmLines)):
            asmLines[i] = asmLines[i][0 : asmLines[i].find('#')].strip().replace(':', ':\n')
        
        asmLines = '\n'.join(asmLines)
        
        return (asmLine for asmLine in asmLines.split('\n') if asmLine != '')
    

    @staticmethod
    def formStatement(asmLines) -> tuple[list, str]:
        try:
            labels = []
            asmLine = next(asmLines)
            while asmLine.endswith(':'):
                labels.append(asmLine[0 : -2])
                asmLine = next(asmLines)

            return labels, asmLine
        
        except StopIteration:
            if labels == []:
                raise UsageException('End')
            
            return labels, 'nop'
        

    @staticmethod
    def judgeType(words:list) -> str:
        typeStr = ''

        for word in words:
            if word.startswith('$'):
                typeStr += 'r'
            
            elif word.startswith(re.compile(r'[0-9]')):
                typeStr += 'i'
        
            else:
                typeStr += 'l'

        return typeStr
    

    @staticmethod
    def foundReg(reg:str) -> int:
        pass
        
    
    @staticmethod
    def splitStatement(statement:str, COMMANDS:dict) -> tuple[int, ]:
        words = statement.split(' ')
        
        try:
            cmd = COMMANDS[words[0]]
        except KeyError as ke:
            raise UsageException(ke)
        
        typeStr = Statement.judgeType(words[1 : -1])
        
        if typeStr != cmd[1]:
            raise UsageException('Unmatch Statement')
        

            
        



        


def argManage(argv:list) -> tuple[str,]:
    if len(argv) != 2:
        raise UsageException('ArgNum Error')
    
    return (argv[1],)



def readCommand(jsonFilename:str) -> dict:
    try:
        fp = open(jsonFilename, 'r')
        commandsJson = fp.read()
        return json.loads(commandsJson)
        
    except FileNotFoundError:
        raise UsageException('jsonFile Not Found')
    
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




def main():
    try:
        asmFilename = argManage(sys.argv)

        COMMANDS = readCommand('./command.json')
        
        asmLines = openAsm(asmFilename[0])

        asmLines = Statement.pretreat(asmLines)

        try:
            s = Statement.formStatement(asmLines)


        except UsageException:
            pass

        

        



    except UsageException as e:
        print(e.msg)
    




if __name__ == '__main__':
    main()