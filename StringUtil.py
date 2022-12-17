class StringUtil:
    @staticmethod
    def escapeString(string):
        #去除转义字符中的\
        charList=[]
        i=0
        while(i < len(string)):
            if(string[i]=='\\'):
                charList.append(string[i+1])
                i=i+2
            else:
                charList.append(string[i])
                i=i+1
        return ''.join(charList)