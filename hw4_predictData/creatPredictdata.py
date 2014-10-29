import glob
import os
import pandas as pd

class CTD(object):
    """docstring for CTD"""
    def __init__(self):
        self.format_l = []
        self.td_l = []
        self.iternum = 0
        self.formatname = ""

    def feature(self,index):
        format_l = self.format_l
        feature = ((float(format_l[index+1][1])-float(format_l[index+3][1]))/float(format_l[index+1][1]))+((float(format_l[index+1][4])-float(format_l[index+3][4]))/float(format_l[index+1][4]))
        if (feature == 0):
            feature = 0.0001        
        return feature

    def format(self,path):
        a = path.split('/')
        self.formatname = a[2]
        with open(path, 'r') as f:
            a = f.read()
        f = a.split('\n')
        f.pop(0)        
        self.iternum = len(f)-3
        for a in range(len(f)):
            a = f[a].split(',')
            a.pop(0)
            self.format_l.append(a)

    def trainData(self):
        for index in range(self.iternum):
            try:
                format_l = self.format_l
                classify = (float(format_l[index][3])-float(format_l[index+1][3]))/float(format_l[index+1][3])*100
                feature = self.feature(index)
                
                a = ['0']+format_l[index+1]+format_l[index+2]+format_l[index+3]+[feature]
                self.td_l.append(a)
            except:
                pass

    def storage_csv(self):
        rowname=['classify','feature','1-open','1-high','1-low','1-close','1-volume','1-adj close','2-open','2-high','2-low','2-close','2-volume','2-adj close','3-open','3-high','3-low','3-close','3-volume','3-adj close']
        df = pd.DataFrame(self.td_l,columns=rowname)
        with open('./traindata/td_'+self.formatname+'.csv', 'w') as f:
            df.to_csv(f)
            print('td_'+self.formatname+'.csv is creat!')

    def storage_txt(self,pathname):
        with open('./predict/data/'+pathname,'ab') as f:    
            for a in self.td_l:
                b = str(a[0])+'\t'
                for c in range(1,20):
                    d = str(c)+':'+str(a[c])+'\t'
                    b += d
                f.write(b+'\n')

    def run(self):
        path = './stock/*'   
        paths=glob.glob(path)
        for index,path in enumerate(paths,1):
            print(index)
            self.format_l = []
            self.td_l = []
            self.format(path)
            self.trainData()

            path = path.split('/')
            pathname = path[2]

            self.storage_txt(pathname)

            print os.popen("./bin/svm-scale -s predict_scale_model ./predict/data/"+pathname+" > ./predict/scale/"+pathname+"predict_data.scale").read()
            print os.popen("./bin/rvkde --best --predict --classify -v ./train/scale/"+pathname+"train_data.scale -V ./predict/scale/"+pathname+"predict_data.scale > ./predict/result/"+pathname+"predict_result").read()

def main():
    ctd = CTD()
    ctd.run()

if __name__ == '__main__' :
    main()


