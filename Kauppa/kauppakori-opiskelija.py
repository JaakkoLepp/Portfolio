# TIE-02100 Johdatus ohjelmointiin
# 1.11.2017
# Jaakko Leppiniemi, jaakko.leppiniemi@student.tut.fi, #275649
# Projekti: Kauppakori-opiskelija
# Tarkastellaan lähikauppojen antimia tekstitiedostosta.
# Viimeksi muokattu 24.2.2019

def tiedoston_luku():

    tiedosto = open("tuotetiedot.txt", "r", encoding="utf-8")
    kauppakori = {}

    try:
        try:
            for rivi in tiedosto:
                rivi = rivi.rstrip()
                osat = rivi.split(":")
                kauppa = osat[0]
                tuote = osat[1]
                hinta = float(osat[2])

                if kauppa not in kauppakori:
                    kauppakori[kauppa] = {}
                    if tuote not in kauppakori[kauppa]:
                        kauppakori[kauppa][tuote] = hinta
                    else:
                        pass
                else:
                    if tuote not in kauppakori[kauppa]:
                        kauppakori[kauppa][tuote] = hinta
                    else:
                        pass

            for kauppa in sorted(kauppakori):
                print(kauppa)
                for tuote in sorted(kauppakori[kauppa]):
                    print(4*" ", "{:<15} {:>10.2f} e" .format(tuote,
                                            kauppakori[kauppa][tuote]))

        except IndexError:
            print("Tiedostoa luettaessa tapahtui virhe!")
        except ValueError:
            print("Tiedostoa luettaessa tapahtui virhe!")
    except OSError:
        print("Tiedostoa luettaessa tapahtui virhe!")

    tiedosto.close()


def tuotteiden_listaus():

    tiedosto = open("tuotetiedot.txt", "r", encoding="utf-8")
    tuotteet = {}

    try:
        try:
            for rivi in tiedosto:
                rivi = rivi.rstrip()
                osat = rivi.split(":")
                tuote = osat[1]
                hinta = float(osat[2])

                if tuote not in tuotteet:
                    tuotteet[tuote] = hinta
                else:
                    if hinta < tuotteet[tuote]:
                        tuotteet[tuote] = hinta

            print("Saatavilla olevat eri tuotteet:")

            for tuote in sorted(tuotteet):
                print(4*" ", "{:<15} {:>10.2f} e" .format(tuote,
                                                          tuotteet[tuote]))

        except IndexError:
            print("Tiedostoa luettaessa tapahtui virhe!")
        except ValueError:
            print("Tiedostoa luettaessa tapahtui virhe!")
    except OSError:
        print("Tiedostoa luettaessa tapahtui virhe!")

    tiedosto.close()


def halvin_myyja():

    tiedosto = open("tuotetiedot.txt", "r", encoding="utf-8")
    kauppakori = {}

    try:
        try:
            for rivi in tiedosto:
                rivi = rivi.rstrip()
                osat = rivi.split(":")
                kauppa = osat[0]
                tuote = osat[1]
                hinta = float(osat[2])

                if kauppa not in kauppakori:
                    kauppakori[kauppa] = {}
                    if tuote not in kauppakori[kauppa]:
                        kauppakori[kauppa][tuote] = hinta
                    else:
                        pass
                else:
                    if tuote not in kauppakori[kauppa]:
                        kauppakori[kauppa][tuote] = hinta
                    else:
                        pass

            print("Anna tuotteet eroteltuna välilyönneillä:")
            syote = input()
            ostoslista = syote.split(" ")
            dict = {}

            for kauppa in kauppakori:
                lista = []
                summa = 0
                for tuote in ostoslista:
                    if tuote in kauppakori[kauppa]:
                        lista.append(tuote)
                        summa += kauppakori[kauppa][tuote]
                if len(lista) == len(ostoslista):
                    dict[kauppa] = summa

            kaupat = []
            hinta = 0
            for kauppa in dict:
                if len(kaupat) == 0 or dict[kauppa] < hinta:
                    kaupat.clear()
                    kaupat.append(kauppa)
                    hinta = dict[kauppa]
                elif hinta == dict[kauppa]:
                    kaupat.append(kauppa)

            if len(dict) == 0:
                print("Yksikään kauppa ei myy kaikkia kauppakorin tuotteita!")

            elif len(kaupat) == 1:
                print("Halvin kauppa tälle korille on", kaupat[0],
                      "{:.2f} e hinnallaan!" .format(hinta))

            else:
                print("Seuraavat kaupat myyvät yhtä halvalla "
                      "{:.2f} e hinnalla:".format(hinta),
                      ", ".join(sorted(kaupat)))


        except IndexError:
            print("Tiedostoa luettaessa tapahtui virhe!")
        except ValueError:
            print("Tiedostoa luettaessa tapahtui virhe!")
    except OSError:
        print("Tiedostoa luettaessa tapahtui virhe!")

    tiedosto.close()


def main():

    print("Tervetuloa kauppakorisovellukseen!\n"
          "Käytettävissä olevat komennot:\n"
          " T ulosta kaupat tuotteineen\n"
          " S aatavilla olevien tuotteiden listaus\n"
          " K auppakorin halvin myyjä\n"
          " Q uit\n")

    syöte = ""
    while syöte != "Q":
        syöte = input("\nAnna komento (T, S, K, Q): ").upper()

        if syöte == "T":
            tiedoston_luku()

        elif syöte == "S":
            tuotteiden_listaus()

        elif syöte == "K":
            halvin_myyja()

        elif syöte == "Q":
            print("Hei hei!")
            return

        else:
            print("Virheellinen komento!")

main()
