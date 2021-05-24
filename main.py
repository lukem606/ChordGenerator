import sys, os, copy
dpath = os.path.abspath('./Scripts')
sys.path.append(dpath)
import key_dict as kd
import numpy.random as rnd


def change_key(k):
    new = copy.deepcopy(k)
    while new == k:
        ind = rnd.randint(0, 11)
        new = kd.key["Chr"][ind]
    return new


def get_chord(ch, i):
    res = ch + kd.key["roman"][i]
    return res


def get_key():
    key = input("Enter a key: ")

    if key not in kd.key["Chr"]:
        got_key = False
    else:
        got_key = True

    while not got_key:
        key = input("Please try again. Letter must be capitalised and only use flats in lower case (no sharps): ")
        if key not in kd.key["Chr"]:
            got_key = False
        else:
            got_key = True

    return key


def new_chord(k, ch):
    new = copy.deepcopy(ch)
    while new == ch:
        ind = rnd.randint(0, 7)
        new = get_chord(kd.key[k][ind], ind)
    return new


def main():
    key = get_key()

    length = 16
    chords = []
    barsFilled = 0

    li = rnd.randint(0, 6)
    if li < 3:
        chords.append(get_chord(key, 0))
        barsFilled += 1
    elif li == 3:
        chords.append(get_chord(key, 0))
        barsFilled += 1
        chords.append("%")
        barsFilled += 1
    elif li == 4:
        chords.append([get_chord(key, 0), new_chord(key, get_chord(key, 0))])
        barsFilled += 1
    elif li == 5:
        tot = []
        tot.append(get_chord(key, 0))
        chr_list = kd.key["Chr"]
        ki = chr_list.index(key)
        if ki <= 6:
            key = kd.key["Chr"][ki+8]
        elif ki >= 4:
            key = kd.key["Chr"][ki-4]
        tot.append(get_chord(kd.key[key][4], 4))
        chords.append(tot)
        barsFilled += 1
        chords.append(get_chord(kd.key[key][0], 0))
        barsFilled += 1

    while barsFilled < length:
        changed = False
        if rnd.randint(0, 3) == 2:
            key = change_key(key)
            changed = True

        last = chords[-1]
        if last == "%":
            last = chords[-2]
        elif isinstance(last, list):
            last = last[1]

        li = rnd.randint(0, 6)
        if li < 3:
            chords.append(new_chord(key, last))
            barsFilled += 1
        elif li == 3:
            chords.append(new_chord(key, last))
            barsFilled += 1
            if barsFilled == length:
                continue
            chords.append("%")
            barsFilled += 1
        elif li == 4:
            tot = []
            tot.append(new_chord(key, last))
            tot.append(new_chord(key, tot[0]))
            chords.append(tot)
            barsFilled += 1
        elif li == 5:
            if changed == False:
                key = change_key(key)
            tot = []
            tot.append(get_chord(key, 0))
            chr_list = kd.key["Chr"]
            ki = chr_list.index(key)
            if ki < 4:
                key = kd.key["Chr"][ki + 8]
            elif ki >= 4:
                key = kd.key["Chr"][ki - 4]
            tot.append(get_chord(kd.key[key][4], 4))
            chords.append(tot)
            barsFilled += 1
            if barsFilled == length:
                continue
            else:
                chords.append(get_chord(kd.key[key][0], 0))
                barsFilled += 1

    final = []

    for ei, entry in enumerate(chords):
        if isinstance(entry, list):
            if ei % 4 == 0:
                final.append("|| {:<7}{:<8}|".format(entry[0], entry[1]))
            elif ei % 4 == 3:
                final.append(" {:<7}{:<8}||\n".format(entry[0], entry[1]))
            else:
                final.append(" {:<7}{:<8}|".format(entry[0], entry[1]))
        else:
            if ei % 4 == 0:
                final.append("|| {:<15}|".format(entry))
            elif ei % 4 == 3:
                final.append(" {:<15}||\n".format(entry))
            else:
                final.append(" {:<15}|".format(entry))

    return final

if __name__ == "__main__":
    out = main()
    print(''.join(out))
