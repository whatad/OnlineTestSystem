from exam.models import Glossary

class MyClass:
    def __init__(self, index, sememe, parent):
        self.index = index
        self.sememe = sememe
        self.parent = parent

    def __eq__(self, other):
        return self.sememe == other.sememe
    def __gt__(self, other):
        return self.sememe > other.sememe
    def __lt__(self, other):
        return self.sememe < other.sememe

class Calcu:
    def __init__(self, alpha, beta1, beta2, beta3, beta4):
        self.alpha = alpha
        self.beta1 = beta1
        self.beta2 = beta2
        self.beta3 = beta3
        self.beta4 = beta4
        self.semeList = []

    def init_sem_list(self, file_name):
        file = open(file_name, "r")
        for line in file:
            sections = line.split()
            index = sections[0]
            sememe = sections[1]
            parent = int(sections[2])
            self.semeList.append(MyClass(index, sememe, parent))
        file.close()

    def cal_word_sim(self, word1, word2):
        print("It's going to calculate the similarity between {} and {} ".format(word1,word2))
        finds1 = Glossary.objects.filter(word=word1)
        finds2 = Glossary.objects.filter(word=word2)
        list1 = [find.sememes for find in finds1]
        list2 = [find.sememes for find in finds2]
        len1 = len(list1)
        len2 = len(list2)
        if len1 == 0:
            print("{} is not in the dictionary".format(word1))
        if len2 == 0:
            print("{} is not in the dictionary".format(word2))
        maxsim = 0.0
        for i in range(len1):
            for j in range(len2):
                sim = self.cal_comcept_sim(list1[i], list2[j])
                if sim > maxsim:
                    maxsim = sim
        return maxsim

    def cal_comcept_sim(self, concept1, concept2):
        print("It's going to calculate the similarity between concept {} and concept {} ".format(concept1, concept2))
        if concept1[0]== '{':
            if concept2[0] != '{':
                return 0
            else:
                sem1 = concept1[1:]
                sem2 = concept2[1:]
                p1 = sem1.find("=")
                p2 = sem2.find("=")
                if (p1>0) ^ (p2>0):
                    return 0
                elif (p1 == -1) and (p2 == -1):
                    return self.cal_sim_base(sem1, sem2)
                else:
                    return self.cal_sim_real(sem1, sem2)
        else:
            if concept2[0] == '{':
                return 0
            else:
                sim1 = 0.0
                sim2 = 0.0
                sim3 = 0.0
                sim4 = 0.0
                pos11 = pos21 = 0
                sem1 = sem2 = ""
                for i in range(4):
                    pos12 = concept1.find("\n", pos11)
                    pos22 = concept2.find("\n", pos21)
                    if pos12 == -1 and pos22 == -1:
                        sem1 = concept1[pos11:]
                        sem2 = concept2[pos21:]
                    else:
                        sem1 = concept1[pos11:pos12]
                        sem2 = concept2[pos21:pos22]
                    if i == 0:
                        sim1 = self.cal_sim1(sem1, sem2)
                    elif i == 1:
                        sim2 = self.cal_sim2(sem1, sem2)
                    elif i == 2:
                        sim3 = self.cal_sim3(sem1, sem2)
                    else:
                        sim4 = self.cal_sim4(sem1, sem2)
                    pos11 = pos12 + 1
                    pos21 = pos22 + 1
                return self.beta1 * sim1 + self.beta2 * sim1*sim2 + self.beta3 * sim1*sim2*sim3 + \
                       self.beta4 * sim1*sim2*sim3*sim4

    #demo1
    def cal_sim_base(self, sem1, sem2):
        if (sem1[0] == 40) ^ (sem2[0] == 40):
            return 0
        if (sem1[0] == 40) and (sem2[0] == 40):
            if sem1 != sem2:
                return 0.0
        if sem1 == sem2:
            return 1.0
        print("It's going to calculate the similarity between base sememe {} and base sememe {}".format(sem1, sem2))
        stack1 = []
        stack2 = []
        mc1 = MyClass(0, sem1, 0)
        mc2 = MyClass(0, sem2, 0)
        if self.semeList.count(mc1)==0:
            print("{} is not in the dictionary".format(sem1))
            return 0
        stack1.append(sem1)
        find1 = self.semeList[self.semeList.index(mc1)]
        child = find1.index
        parent = find1.parent
        while child != parent:
            stack1.append(self.semeList[parent].sememe)
            child = parent
            parent = self.semeList[parent].parent
        if self.semeList.count(mc2) ==0:
            return 0
        stack2.append(sem2)
        find2 = self.semeList[self.semeList.index(mc2)]
        child = find2.index
        parent =find2.parent
        while child != parent:
            stack2.append(self.semeList[parent].sememe)
            child = parent
            parent = self.semeList[parent].parent
        tail1 = stack1.pop()
        tail2 = stack2.pop()
        if tail1 != tail2:
            print("{} and {} are in different tree".format(tail1, tail2))
            return 0
        while len(stack1) != 0 and len(stack2) != 0 and tail1 == tail2:
            tail1 = stack1.pop()
            tail2 = stack2.pop()
        dist = len(stack1) + len(stack2) +2
        result = self.alpha / (self.alpha + dist)
        print(result)
        return result



    '''
    #demo2
    def cal_sim_base2(sem1, sem2):
        if (sem1[0]==40) ^ (sem2[0]==40):
            return 0
        if (sem1[0]==40) and (sem2[0]==40):
            if sem1 != sem2:
                return 0.0
        if sem1 == sem2:
            return 1.0
        print("It's going to calculate the similarity between base sememe {} and base sememe {}".format(sem1, sem2))
        stack1 = []
        stack2 = []
        mc1 = MyClass(0, sem1, 0)
        mc2 = MyClass(0, sem2, 0)
        if semeList.count(mc1)==0:
            print("{} is not in the dictionary".format(sem1))
            return 0
        stack1.append(sem1)
        find1 = semeList[semeList.index(mc1)]
        child = find1.index
        parent = find1.parent
        while child != parent:
            stack1.append(semeList[parent].sememe)
            child = parent
            parent = semeList[parent].parent
        d1 = len(stack1)
        if semeList.count(mc2) ==0:
            return 0
        stack2.append(sem2)
        find2 = semeList[semeList.index(mc2)]
        child = find2.index
        parent =find2.parent
        while child != parent:
            stack2.append(semeList[parent].sememe)
            child = parent
            parent = semeList[parent].parent
        d2 = len(stack2)
        tail1 = stack1.pop()
        tail2 = stack2.pop()
        if tail1 != tail2:
            print("{} and {} are in different tree".format(tail1, tail2))
            return 0
        while len(stack1) != 0 and len(stack2) != 0 and tail1 == tail2:
            tail1 = stack1.pop()
            tail2 = stack2.pop()
        dist = len(stack1) + len(stack2) +2
        #result = alpha / (alpha + dist)
        result = alpha * (d1 + d2) / (alpha * (d1 + d2) + dist + abs(d1 - d2))
        print("*********************************")
        print(result)
        print("*********************************")
        return result
    '''


    def cal_sim_real(self, sem1, sem2):
        print("It's going to calculate the similarity between relative sememe {} and relative sememe {}".format(sem1, sem2))
        if sem1[0] == 40:
            sem1 = sem1[1:-1]
        if sem2[0] == 40:
            sem2 =sem2[1:-1]
        p1 = sem1.find("=")
        rela1 = sem1[0:p1]
        p2 = sem2.find("=")
        rela2 = sem2[0:p2]
        if rela1 == rela2:
            base1 = sem1[p1+1:]
            base2 = sem2[p2+1:]
            return self.cal_sim_base(base1, base2)
        else:
            return 0

    def cal_sim1(self, line1, line2):
        line1 = line1.strip()
        line2 = line2.strip()
        if line1 == "" or line2== "":
            return 0
        print("It's going to calculate the similarity of first independent sememes between {} and {}".format(line1, line2))
        return self.cal_sim_base(line1[:-1], line2[:-1])

    def cal_sim2(self, line1, line2):
        line1 = line1.strip()
        line2 = line2.strip()
        if line1 == "" or line2 == "":
            return 0
        print("It's going to calculate the similarity of other independent sememes between {} and {}".format(line1, line2))
        list1 = self.split_string(line1)
        list2 = self.split_string(line2)
        max_list =[]
        len1 = len(list1)
        len2 = len(list2)
        while len1 and len2:
            max_sim = 0.0
            m=n=0
            for i in range(len1):
                for j in range(len2):
                    simil = self.cal_sim_base(list1[i], list2[j])
                    if simil > max_sim:
                        m = i
                        n = j
                        max_sim = simil
            if max_sim == 0.0:
                break
            max_list.append(max_sim)
            del list1[m]
            del list2[n]
            len1 = len(list1)
            len2 = len(list2)
        if len(max_list) == 0:
            return 0.0
        s = 0.0
        for itr in max_list:
            s += itr
        return s / len(max_list)

    def cal_sim3(self, line1, line2):
        line1 = line1.strip()
        line2 = line2.strip()
        if line1 == "" or line2 == "":
            return 0
        print("It's going to calculate the similarity of relative sememes between {} and {}".format(line1, line2))
        list1 = self.split_string(line1)
        list2 = self.split_string(line2)
        sim_list = []
        len1 = len(list1)
        len2 = len(list2)
        while len1 and len2:
            for j in range(len2):
                ss = self.cal_sim_real(list1[len1-1], list2[j])
                if ss != 0:
                    sim_list.append(ss)
                    del list2[j]
                    break
            del list1[len1-1]
            len1 = len(list1)
            len2 = len(list2)
        if len(sim_list) == 0:
            return 0.0
        s = 0.0
        for itr in sim_list:
            s += itr
        return s / len(sim_list)

    def cal_sim4(self, line1, line2):
        if line1 == "" or line2 == "":
            return 0
        print("It's going to calculate the similarity of symbol sememes between {} and {}".format(line1, line2))
        list1 = self.split_string(line1)
        list2 = self.split_string(line2)
        sim_list = []
        len1 = len(list1)
        len2 = len(list2)
        while len1 and len2:
            sym1 = list1[len1-1][0]
            for j in range(len2):
                sym2 = list2[len2-1][0]
                print("sym", sym1, sym2)
                if sym1 == sym2:
                    base1 = list1[len1-1][1:]
                    base2 = list2[j][1:]
                    sim_list.append(self.cal_sim_base(base1, base2))
                    del list2[j]
                    break
            del list1[len1-1]
            len1 = len(list1)
            len2 = len(list2)
        if len(sim_list) == 0:
            return 0.0
        s = 0.0
        for itr in sim_list:
            s += itr
        return s / len(sim_list)

    def split_string(self, line):
        result = []
        pos1 = 0
        pos2 = line.find(",", pos1)
        while pos2 != -1:
            sem = line[pos1:pos2]
            result.append(sem)
            pos1 = pos2 + 1
            if pos1 > len(line):
                break
            pos2 = line.find(",", pos1)
        return result

    '''
    def main():
        init_sem_list("whole.dat")
        word1 = "开心"
        word2 = "伤心"
        sim = cal_word_sim(word1, word2)
        print("{} 和 {} 的相似度为 {}".format(word1, word2, sim))
    '''