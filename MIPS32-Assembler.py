# code = utf-8

import json
import sys
import re


ty = ['COMMON', 'BLANK', 'LABEL']



class UsageException(Exception):
    def __init__(self, msg:str) -> None:
        self.msg = msg



class Statement(object):
    '''语句类'''
    def __init__(self, initStruct) -> None:
        pass
        

    @staticmethod
    def normalize(asmLine:str, COMMANDS:list) -> dict:
        content = Statement.getContent(asmLine)

        initStruct = Statement.splitContent(content.lower(), COMMANDS)
        
        return initStruct
    

    @staticmethod
    def getContent(asmLine:str) -> str:
        return asmLine[0 : asmLine.find('#')]
    

    @staticmethod
    def splitContent(content:str, COMMANDS:list) -> list:
        initStruct = {'isBlank':True,}

        for word in re.split('[ ,]+', content):
            if word:
                if word in COMMANDS:
                    initStruct['isBlank'] = False
                    initStruct['command'] = word
                    
                else:
                    pass
        


        


def CommonStatement(Statement):
    '''普通语句类'''
    def __init__(self) -> None:
        pass
        


def Blank(Statement):
    '''空行类'''
    def __init__(self) -> None:
        pass



def argManage(argv:list) -> (str,):
    if len(argv) != 2:
        raise UsageException('ArgNum Error')
    
    return argv[1]



def readCommand(jsonFilename) -> dict:
    try:
        fp = open(jsonFilename, 'r')
        commandsJson = fp.read()
        return json.loads(commandsJson)
        
    except FileNotFoundError:
        raise UsageException('jsonFile Not Found')
    
    finally:
        fp.close()



def openAsm(asmFilename:str):
    try:
        fp = open(asmFilename, 'r')
        return (l for l in fp.readlines())

    except FileNotFoundError:
        raise UsageException('asmFile Not Found')
    
    finally:
        fp.close()



def formStatements(asmLines, COMMANDS:list) -> list:
    l = next(asmLines)
    print(l)
    l = Statement.normalize(l, COMMANDS)
    print(l)
    return []




def main():
    try:
        asmFilename = argManage(sys.argv)

        COMMANDS = readCommand('./command.json')
        
        asmLines = openAsm(asmFilename)

        statements = formStatements(asmLines, COMMANDS.keys())

        



    except UsageException as e:
        print(e.msg)
    




if __name__ == '__main__':
    main()