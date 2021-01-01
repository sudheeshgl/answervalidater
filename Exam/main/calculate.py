import csv,os
from configparser import ConfigParser
from django.conf import settings

config = ConfigParser()
config.read('config.ini')
class HashTable():
    def __init__(self):
        self.max_students = int(config.get('exam','totalstudents'))
        self.table=[None] * self.max_students
        self.catogries=len(self.Splitcategories())
    def __setitem__(self, key, value):
        hashKey=self.__hash(key)
        newhashKey=self.__check(hashKey)
        data = (hashKey,key,value)
        try:
            if self.table[hashKey][1] != key:
                self.table[newhashKey] = data
            else:
                print(f'Already added {key}')
        except:
            self.table[newhashKey] = data

    def __getitem__(self, key):
        newkey=self.__hash(key)
        if self.table[newkey] is not None and self.table[newkey][0] == newkey and self.table[newkey][1] == key :
            return self.table[newkey]
        else:
            try:
                while self.table[newkey][1] != key:
                    newkey=self.__increment(newkey)
            except:
                return None
            return self.table[newkey]
    def __hash(self,key):
        hash=0
        for i in key:
            hash+=ord(i)
        return hash % self.max_students

    def __increment(self,key):
        return (key + 1) % self.max_students

    def __check(self,key):
        if self.table[key] is None:
            return key
        else:
            while self.table[key] is not None:
                key=self.__increment(key)
            return key

    def Splitcategories(self):
        categories = list(map(int, config.get('exam', 'categories').split(',')))
        totalcat=0
        for i in categories:
            totalcat+=i
        temp=[]
        for category in categories:
            temp.append(int(category*config.getint('exam','noofquestion')/totalcat))
        return temp

    def TotalQuickSort(self,arrs):
        arr=[]
        for i in range(0,len(arrs)):
            if arrs[i] is not None:
                arr.append(arrs[i])
        elements = len(arr)
        if elements < 2:
            return arr
        current_position = 0
        for i in range(1, elements):
            if arr[i] is None:
                pass
            elif arr[i][2][6] >= arr[0][2][6]:
                current_position += 1
                temp = arr[i]
                arr[i] = arr[current_position]
                arr[current_position] = temp
        temp = arr[0]
        arr[0] = arr[current_position]
        arr[current_position] = temp
        left = self.TotalQuickSort(arr[0:current_position])
        right = self.TotalQuickSort(arr[current_position + 1:elements])
        arr = left + [arr[current_position]] + right
        return arr

    def CatQuickSort(self,arrs,index=0):
        arr=[]
        for i in range(0,len(arrs)):
            if arrs[i] is not None:
                arr.append(arrs[i])
        elements = len(arr)
        if elements < 2:
            return arr
        current_position = 0

        for i in range(1, elements):
            if arr[i] is None:
                pass
            elif arr[i][2][7][index] >= arr[0][2][7][index]:
                current_position += 1
                temp = arr[i]
                arr[i] = arr[current_position]
                arr[current_position] = temp
        temp = arr[0]
        arr[0] = arr[current_position]
        arr[current_position] = temp
        left = self.CatQuickSort(arr[0:current_position],index)
        right = self.CatQuickSort(arr[current_position + 1:elements],index)
        arr = left + [arr[current_position]] + right
        return arr

def run():
    h=HashTable()
    with open(os.path.join(settings.MEDIA_ROOT,config.get('exam','answersheet')), 'r') as sheet, open(os.path.join(settings.MEDIA_ROOT,config.get('exam','answer')), 'r') as answer:
        datas = csv.DictReader(sheet)
        ans = csv.DictReader(answer)
        ans = [i for i in ans]
        categories = h.Splitcategories()
        for data in datas:
            student = []
            regNo = data['Register No']
            TotalScore=TempScore=TotalNegativeScore=TempNegativeScore=count2=unAnswer=0
            count=1
            NegativeScore=[]
            Score=[]
            for i in range(1, int(config.getint('exam','noofquestion')+1)):
                if len(data[str(i)]) == 0:
                    unAnswer+=1
                    pass
                elif ans[0][str(i)] == data[str(i)]:
                    TotalScore += 1
                    TempScore +=1
                else:
                    TotalNegativeScore += 1
                    TempNegativeScore += 1
                if count == categories[count2]:
                    Score.append(TempScore)
                    NegativeScore.append(TempNegativeScore)
                    TempNegativeScore = 0
                    TempScore = 0
                    count2+=1
                    count=0
                count+=1
                print(i)
            student.append(data['Name'])
            student.append(Score)
            student.append(NegativeScore)
            student.append(TotalScore)
            student.append(TotalNegativeScore)
            student.append(unAnswer)
            student.append(TotalScore-(0.5*float(TotalNegativeScore)))
            TotalCat=[]
            for i in range(0,len(Score)):
                TotalCat.append(Score[i]-(0.5*float(NegativeScore[i])))
            student.append(TotalCat)
            h[regNo]=student

        listcategories=[]
        total=h.TotalQuickSort(h.table)
        listcategories.append(total)
        for i in range(0,h.catogries):
            listcategories.append(h.CatQuickSort(h.table,i))

        return listcategories

