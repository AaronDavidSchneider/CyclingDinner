import numpy as np
from source.combination import combination
from source.couple import couple
from source.group import group
from import_data import import_data
import source.config as c
import itertools

gd = {"H": 1, "V": 0, "N": 2}
gd_inv = {1: "H", 0: "V", 2: "N"}


def Diff(li1, li2):
    return (list(set(li1) - set(li2)))


def main(file):
    V, H, N = import_data(file)
    data_sorted = [V, H, N]
    N_couples = np.sum([len(x) for x in data_sorted])

    total_comb = []
    loss_comb = []
    loss_comb_geodesic = []
    for i in range(c.iterations):
        course = 0
        temp_total = []
        while course < 3:
            np.random.shuffle(V)
            np.random.shuffle(H)
            np.random.shuffle(N)
            temp = []
            for j in range(len(V)):
                temp.append([V[j], H[j], N[j]])
            temp_dup = False
            for p in itertools.permutations(temp):
                if list(p) in total_comb: temp_dup = True
            for a in temp:
                for b in [item for sublist in temp_total for item in sublist]:
                    if len(Diff(a, b)) < 2: temp_dup = True
            if not temp_dup:
                temp_total.append(temp)
                course += 1
        total_dup = False
        for p in itertools.permutations(temp_total):
            if list(p) in total_comb: total_dup = True
        if not total_dup:
            comb = combination(temp_total)
            #comb.print_combination()
            total_comb.append(comb)
            loss_comb_geodesic.append(comb.get_loss())

    if c.max_api_calls != 0:
        max_gmaps = int(c.max_api_calls / (N_couples * c.N_courses))
        winner_comb_geodesic = [
            total_comb[i] for i in np.argsort(loss_comb_geodesic)
        ]
        if (max_gmaps < len(winner_comb_geodesic)) and (max_gmaps > 0):
            winner_comb_geodesic = winner_comb_geodesic[:max_gmaps]
            loss_comb = [
                comb.get_loss(gmaps=True) for comb in winner_comb_geodesic
            ]
            winner_comb = winner_comb_geodesic[np.argmin(loss_comb)]
        else:
            winner_comb = total_comb[np.argmin(loss_comb)]
            loss_comb = loss_geodesic
            print("using geodesic loss")
    else:
        loss_comb = loss_comb_geodesic
        winner_comb = total_comb[np.argmin(loss_comb)]
        print("using geodesic loss")

    winner_comb.print_combination()
    winner_comb.write_emails(
        np.array(data_sorted).reshape(N_couples), "einladung.txt")

    for couple in np.array(data_sorted).reshape(N_couples):
        couple.print_map()
        couple.print_met_people(winner_comb)

    print("\n\n total possible combinations: {:d}".format(len(total_comb)))

    return winner_comb, loss_comb, loss_comb_geodesic


if __name__ == "__main__":
    _, loss, loss_geodesic = main(c.ANMELDUNGEN)

    with open('output_loss.txt', 'w') as f:
        for item in loss:
            f.write("%s\n" % item)
    with open('output_loss_geodesic.txt', 'w') as f:
        for item in loss_geodesic:
            f.write("%s\n" % item)
