
import os

acceptedFiles = ['.java', '.kt', '.cpp', '.swift', '.py', '.h', '.hpp']
doNotCount = ['Generated from', 'The ANTLR Project. All rights reserved']

class Statistics:

    def __init__(self, path):
        self.path = path

    def list(self):
        walk = os.walk(self.path)
        result = ''
        count = 0
        for path, _, flist in walk:
            for fname in flist:
                if os.path.splitext(fname)[-1] in acceptedFiles and 'Antlr4' not in path:
                    with open(os.path.join(path, fname), 'r') as f:
                        try:
                            content = f.read()
                        except:
                            continue
                        ok = True
                        for str in doNotCount:
                            if str in content:
                                ok = False
                    if ok:
                        count += 1
                        result += (content + '\n')

        arr = [x for x in result.split('\n') if x and not x.strip().startswith('//') and not x.strip().startswith('#')]

        return count, len(arr), len(result)

