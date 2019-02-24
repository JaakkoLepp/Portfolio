# TIE-02100 Johdatus Ohjelmointiin
# 8.12.2017
# Jussi Åkerlind, jussi.akerlind@studen.tut.fi, #253468
# Jaakko Leppiniemi, jaakko.leppiniemi@student.tut.fi, #275649
# Graafinen käyttöliittymä huikean jännittävästä noppapelistä.
# Tähtäämme tämän ohjelman toteutuksessa skaalautuvaan ohjelmaan.
# Säännöt: Yksinkertaisuudessaan pelissä saa pisteitä kun arvaa nopan
#   silmäluvun oikein. Pelaaja voittaa kun saavuttaa tietyn voittopistemäärän.
#   Pelaajien ja voittopisteiden määrää voi muuttaa lähdekoodin alussa olevia
#   vakioita muuttamalla.
# Miten peli toimii: Aloita painamalla uusi peli, ja syötä arvaukset tekstin-
#   syöttökenttään. Lukitse arvaus painamalla vuorossa olevan pelaajan tekstiä.
#   Arvauksien syöttämisen jälkeen heitä noppaa ja jännitä!

from random import randint
from tkinter import *


NOPPAKUVAT = ["1.gif", "2.gif", "3.gif", "4.gif", "5.gif", "6.gif"]
PELAAJAT = 2
VOITTOPISTEET = 2

class Nopat:

    def __init__(self):
        self.__ikkuna = Tk()
        self.__ikkuna.title("Noppapeli")
        self.__ikkuna.option_add("*Font", "Times 16")

        # Ennen nopan kuvien lisäämistä listaan luodaan tyhjä kuva, joka on
        # listan ensimmäinen alkio, jotta nopan silmäluvut vastaavat listan
        # alkioita.

        tyhjakuva = PhotoImage(width=86, height=86)
        self.__noppakuvat = [tyhjakuva]

        for tiedosto in NOPPAKUVAT:
            kuva = PhotoImage(file=tiedosto)
            self.__noppakuvat.append(kuva)


        # Luodaan button-komponentit

        self.__heittonappula = Button(self.__ikkuna, text="Heitä",
                                      state=DISABLED, command=self.heitto,
                                      relief=RAISED, bg="red", fg="black")
        self.__heittonappula.grid(row=0, column=0, columnspan=2, sticky=W+E)

        self.__uusi_peli_nappula = Button(self.__ikkuna, text="Uusi peli",
                                        command=self.uusi_peli, relief=RAISED,
                                        background="red", foreground="black")
        self.__uusi_peli_nappula.grid(row=0, column=2,
                                      columnspan=2, sticky=E+W)

        self.__lopetusnappula = Button(self.__ikkuna, text="Lopeta",
                                     command=self.lopeta, relief=RAISED,
                                     bg="red", fg="black")
        self.__lopetusnappula.grid(row=0, column=4, columnspan=2,
                                   sticky=E+W)


        # Luodaan tekstikomponentteja sekä tila nopan kuvalle.

        self.__tulokset_teksti = Label(self.__ikkuna, text="Tulokset")
        self.__tulokset_teksti.grid(row=1, column=5, sticky=E)

        self.__arvaus_teksti = Label(self.__ikkuna, text="Arvaus (1-6)")
        self.__arvaus_teksti.grid(row=1, column=2)

        self.__noppalabel = Label(self.__ikkuna)
        self.__noppalabel.grid(row=1, column=0, rowspan=PELAAJAT)

        self.__tuloslabel = Label(self.__ikkuna, text="Aloita painamalla "
                                                      "Uusi peli.")
        self.__tuloslabel.grid(row=6, column=2, rowspan=3)

        self.__arvauslabel = Label(self.__ikkuna, text="Arvaus")
        self.__arvauslabel.grid(row=1, column=4)


        self.__pelaajalista = []        # Listassa buttoneita
        self.__lista_arvauksista = []   # Listassa labeleita


        # Luodaan pelaajista buttonkomponentit, joiden komentona lukitaan
        #   arvaukset. Lisätään pelaajat listaan jota voidaan käsitellä.
        for i in range(PELAAJAT):
            self.__pelaaja = Button(self.__ikkuna,
                                    text="Pelaaja "+str(i+1)+":",
                                    command=self.lukitse, state=DISABLED)
            self.__pelaaja.grid(row=3+i, column=3)
            self.__pelaajalista.append(self.__pelaaja)


        self.__arvaus = Entry(self.__ikkuna)
        self.__arvaus.grid(row=4, column=2)


    def uusi_peli(self):
        """
        Uusi peli -metodi alustaa pelissä käytettävät listat sekä laskurin ja
        indeksin.
        :return:
        """
        self.__lista_tuloksista = []    # Lista johon lisätään pelaajien
                                        #  tuloslabelit perustuen tuloslistaan.
        self.__lista = []   # Lista pelaajien arvauksista kokonaislukuina.
        self.__laskuri = 0  # Laskuri jota käytetään labeleiden sijoittamiseen
                            #  gridissä.
        self.__score = PELAAJAT * [0]   # Lista johon lisätään pelaajien
                                        #  tulokset kokonaislukuina.
        self.__indeksi = 0  # Indeksi jota käytetään vuorossa olevan arvaajan
                            #   buttonin normalisoimiseen.
        self.__tuloslabel.configure(text="Arvatkaa nopan silmäluku.")
        self.__pelaajalista[0].configure(state=NORMAL)

        # Luodaan pelaajien numeroiden kohdalle labelit arvauksia ja tuloksia
        #   varten.
        for i in range(PELAAJAT):
            self.__pelaajan_arvaus = Label(self.__ikkuna, text="0")
            self.__pelaajan_arvaus.grid(row=3 + i, column=4)
            self.__lista_arvauksista.append(self.__pelaajan_arvaus)
            self.__tulos = Label(self.__ikkuna,
                                 text="0")
            self.__tulos.grid(row=3 + i, column=5)
            self.__lista_tuloksista.append(self.__tulos)


    def lukitse(self):
        """
        Pelaajan nimeä painamalla suoritetaan metodi lukitse, joka lukitsee
        vuorossa olevan pelaajan arvauksen listaan.
        :return:
        """

        try:
            # Tarkistetaan että annettu arvo on kokonaisluku väliltä 1-6.
            alkio = int(self.__arvaus.get())
            if alkio >= 1 and alkio <= 6:
                # Lisätään arvaus listaan ja sijoitetaan se oikeaan kohtaan
                #   laskurin avulla.
                self.__lista.append(alkio)
                self.__pelaajan_arvaus = Label(self.__ikkuna, text="")
                self.__pelaajan_arvaus.grid(row=3 + self.__laskuri, column=4)
                self.__lista_arvauksista.append(self.__pelaajan_arvaus)
                self.__laskuri += 1
                self.__pelaajan_arvaus.configure(text=alkio)

                # Nollataan teksti- ja tekstinsyöttökentät.
                self.__tuloslabel.configure(text="")
                self.__arvaus.delete(0)

                # Miten saadaan vain tietty nappi avattua ja muut lukittua??
                try:
                    self.__pelaajalista[self.__indeksi].configure(state=DISABLED)
                    self.__pelaajalista[self.__indeksi+1].configure(state=NORMAL)
                    self.__indeksi += 1
                except IndexError:
                    self.__indeksi = 0
                    pass

                # Lukitaan pelaajanappulat ja avataan heittonappula.
                if len(self.__lista) == PELAAJAT:
                    self.__heittonappula.configure(state=NORMAL)
                    for pelaaja in self.__pelaajalista:
                        pelaaja.configure(state=DISABLED)

        # Virheellisistä arvoista huomautus.
            else:
                self.__tuloslabel.configure(text="Meidän nopassa on\n"
                                                 "silmäluvut 1-6.\n"
                                                 "Yritähän uudestaan.")
                self.__arvaus.delete(0,END)
        except ValueError:
            self.__tuloslabel.configure(text="Meidän nopassa on\n"
                                             "silmäluvut 1-6.\n"
                                             "Yritähän uudestaan.")
            self.__arvaus.delete(0,END)

        return self.__lista


    def heitto(self):
        """
        Arvauksien lukitsemisen jälkeen heitetään noppaa, ja sieltä tulee
        satunnaisesti yksi luku yhdestä kuuteen.
        :return:
        """

        silmaluku = randint(1, 6)
        self.__noppalabel["image"] = self.__noppakuvat[silmaluku]

        # Annetaan heitolle totuusarvo jota käytetään listojen alustamisessa.
        totuusarvo = 0

        # Jos useampi pelaaja on arvannut oikein, ne saa pisteet for-lenkissä.
        if self.__lista.count(silmaluku) > 1:
            for arvaus in range(len(self.__lista)):
                if self.__lista[arvaus] == silmaluku:
                    self.__score[arvaus] += 1
                    self.__lista_tuloksista[arvaus].configure(
                        text=self.__score[arvaus])

            self.__tuloslabel.configure(text="Useampi pelaaja arvasi oikein!")
            totuusarvo = 1

            self.__heittonappula.configure(state=DISABLED)
            self.__pelaajalista[0].configure(state=NORMAL)


        # Jos vain yksi pelaaja arvaa oikein, se saa pisteen indeksinsä
        #   perusteella.
        elif self.__lista.count(silmaluku) == 1:
            indeksi = self.__lista.index(silmaluku)
            self.__score[indeksi] += 1
            self.__tuloslabel.configure(text="Pelaaja " + str(indeksi + 1) +
                                             " arvasi oikein!")
            self.__lista_tuloksista[indeksi].configure(
                text=self.__score[indeksi])
            totuusarvo = 1

            self.__heittonappula.configure(state=DISABLED)
            self.__pelaajalista[0].configure(state=NORMAL)


        else:
            self.__tuloslabel.configure(text="")

        if totuusarvo == 1:
            # Nollaa arvauslistan ja laskurin jota käytetään uusien arvojen
            #   lukitsemisessa, sekä tarkistetaan pelin päättyminen.
            self.__lista = []
            self.__laskuri = 0
            for pelaaja in self.__lista_arvauksista:
                pelaaja.configure(text="0")
            if self.tarkasta_pelin_loppu():
                return


    def tarkasta_pelin_loppu(self):
        """
        Aina kun pelaaja arvaa oikein, tällä metodilla tarkastetaan voittaako
        oikein arvannut pelaaja, eli verrataan hänen pisteitään voittoon tar-
        vittavaan pistemäärään. Jos useampi pelaaja voittaa, tulee tasapeli.
        :return:
        """

        # Aluksi tehdään lista johon lisätään kaikki voittopistemäärän saavut-
        #   taneet pelaajat.
        voittajat = []
        for i in range(len(self.__score)):
            if self.__score[i] >= VOITTOPISTEET:
                voittajat.append(i)

        # Tarkistetaan onko voittajia ollenkaan ja onko niitä yksi vai useampi.
        if len(voittajat) == 0:
            return False
        elif len(voittajat) == 1:
            self.__tuloslabel.configure(text="Pelaaja "+
                                             str(voittajat[0]+1)+" voitti!")
            for pelaaja in self.__pelaajalista:
                pelaaja.configure(state=DISABLED)
        else:
            self.__tuloslabel.configure(text="Tasapeli!")
            for pelaaja in self.__pelaajalista:
                pelaaja.configure(state=DISABLED)



    def lopeta(self):
        """Lopettaa ohjelman toiminnan
        """
        self.__ikkuna.destroy()


    def aloita(self):
        """Aloittaa ohjelman.
        """
        self.__ikkuna.mainloop()

def main():

    ui = Nopat()
    ui.aloita()

main()