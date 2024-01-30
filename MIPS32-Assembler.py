# code = utf-8

import sys


ty = ['COMMON', 'BLANK', 'LABEL']


class Statement(object):
    '''语句类'''
    def __init__(self, asmLine) -> None:
        self.asmLine = asmLine
        self.comment = ''
        self.comment, b = Statement.normalize
        

    @staticmethod
    def normalize(asmLine:str) -> (str,str):
        sharpIndex = asmLine.find('#')
        if sharpIndex == -1:
            pass
        # l = asmLine.
        return '',''
    

    @staticmethod
    def splitComment(asmLine:str) -> (str, str):
        sharpIndex = asmLine.find('#')
        return (asmLine[0 : sharpIndex]), asmLine[sharpIndex : -1]
        


def CommonStatement(Statement):
    '''普通语句类'''
    def __init__(self) -> None:
        pass


def LabelStatement(Statement):
    '''标签语句类'''
    def __init__(self) -> None:
        pass


def Blank(Statement):
    '''空行类'''
    def __init__(self) -> None:
        pass



def fopen(asmFilename:str):
    try:
        fp = open(asmFilename, 'r')
        return fp.readlines

    except FileNotFoundError:
        return 'FileNotFound'



def asmNormalize(asmLines:list) -> list:
    for asmLine in asmLines:
        asmLine.lower()
        asmLine.split()



def main():
    if len(sys.argv) != 2:
        print(-1)
        return -1
    
    asm = fopen(sys.argv[1])
    if asm == 'FileNotFound':
        print(-2)
        return -2
    




if __name__ == '__main__':
    main()