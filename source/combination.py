from source.couple import couple
from source.group import group
import source.config as c
import numpy as np

# see https://stackoverflow.com/questions/5775352/python-return-2-ints-for-index-in-2d-lists-given-item
def index_2d(myList, v):
    for i, x in enumerate(myList):
        if v in x:
            return (i, x.index(v))
# Eine Kombination pro Gang, drei Kombinationen insgesamt
class combination:
    def __init__(self, comb):
        self.groups = [[]]
        for i in range(c.N_courses):
            self.groups.append([])
            for j in range(len(comb[i])):
                for k in range(len(comb[i][j])):
                    if i==0:
                        comb[i][j][k].pre = comb[i][j][k]
                    elif i>0:
                        temp_j, temp_k = index_2d(comb[i-1],comb[i][j][k])
                        comb[i][j][k].pre = comb[i-1][temp_j][temp_k]

                self.groups[i].append(group(comb[i][j],i))

    def get_loss(self, gmaps=False):
        loss = 0
        for course in range(len(self.groups)):
            for g in self.groups[course]:
                loss += np.square(g.get_loss(gmaps))
        return np.sqrt(loss)


    def print_combination(self):
        result = ""
        i = 0
        for course in self.groups[:-1]:
            i+=1
            result += ".....................\n"
            result += "Gang {}\n".format(i)
            result += ".....................\n"
            j = 0
            for g in course:
                j += 1
                result += "Gruppe {}\n".format(j)
                for couple in g.couples:
                    result += couple.print_info(i-1)
                result += "\n"

        print(result)

    def combination_get_host(self,couple, course):
        for group in self.groups[course]:
            if couple in group.couples:
                return group.couples[group.host]

    def combination_get_guests(self,couple):
        for course in range(3):
            for group in self.groups[course]:
                if group.couples[group.host] == couple:
                    couples = group.couples
        return dict(zip(["V","H","N"],couples))

    def write_emails(self,couples,file):
        f = open(file, "r")
        mail = f.read()
        f.close()

        form_dict = {}
        for couple in couples:
            couple.set_final_combination(self)

            for c in ["V","H","N"]:
                form_dict["O_"+c] = couple.dinner[c].address
                form_dict["N_"+c] = couple.dinner[c].name
                form_dict["H_"+c] = couple.dinner[c].phone
                form_dict["Notes_"+c] = str(couple.guests[c].note).replace("nan","N/A")
                form_dict["G_H_"+c] = couple.guests[c].phone

            out = open("mails/mail_{}.txt".format(couple.name),"w+")
            out.write(mail.format(**form_dict))
            out.close()

    def met_people(self,couple):
        couples = []
        for course in range(3):
            for group in self.groups[course]:
                if couple in group.couples:
                    for temp in group.couples:
                        couples.append(temp)
        return list(set(couples))
