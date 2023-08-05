import csv 

class Reader():
    def __init__(self, fpath:str):
        self.fpath = fpath 
        self.fd = open(self.fpath)
        self.csvrd = csv.reader(self.fd, delimiter=',', quotechar='"', escapechar='\\')
        self.headers = next(self.csvrd)
    
    def Read(self) -> dict:
        r = next(self.csvrd)

        row = {}
        for idx in range(len(self.headers)):
            row[self.headers[idx]] = r[idx]
        
        return row
    
    def __iter__(self):
        while True:
            try:
                yield self.Read()
            except StopIteration:
                return 
        
class Writer():
    def __init__(self, fpath:str, mode:str="w"):
        self.fpath = fpath
        self.fd = open(self.fpath, mode, newline='')
        self.csvwd = csv.writer(self.fd, delimiter=',', quotechar='"', escapechar='\\', doublequote=False)# , quoting=csv.QUOTE_NONE)
        self.headers = None
        self.fdmode = mode
    
    def SetHeaders(self, headers:list[str]):
        self.headers = headers
        if self.fdmode == "w":
            self.csvwd.writerow(headers)
    
    def Write(self, row:dict[str]):
        if not self.headers:
            raise Exception("Set header by SetHeaders method first")

        r = []
        for header in self.headers:
            if header in row:
                r.append(row[header])
            else:
                r.append("")
        
        self.csvwd.writerow(r)

    def Close(self):
        self.fd.close()
    
    def Flush(self):
        self.fd.flush()

if __name__ == "__main__":
    w = Writer("test.csv")

    w.SetHeaders(["h1", "h2"])

    w.Write({"h1": "v1", "h2": '"v2,kkk|'})
    w.Write({"h1": "v,1", "h2": '"v222'})
    w.Write({"h1": "3", "h2": '"99kkk'})
    
    w.Close()

    r = Reader("test.csv")
    print(r.Read())

    for row in r:
        print(row)