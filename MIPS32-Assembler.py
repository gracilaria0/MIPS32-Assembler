# code = utf-8

import sys



class Statement(object):
    '''语句类'''
    def __init__(self, type='COMMON', ) -> None:
        if type in [
            'COMMON',
            'COMMENT',
            'BLANK']:
            self.type = type
        else:
            self.type = 'BAD'

    
    @staticmethod
    def normalize(asmLine:str) -> tuple:
        l = asmLine.lower().split()


def CommonStatement(Statement):
    '''普通语句类'''
    def __init__(self) -> None:
        pass


def CommentStatement(Statement):
    '''注释语句类'''
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