# Ikkunanpesun hallintajärjestelmä

Sovelluksen avulla ikkunanpesuyritys voi hallinnoida ovelta ovelle tapahtuvaa myyntiä, työn suoritusta ja laskutusta.

## Sovelluksen toiminnot

* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään uusia ikkunanpesutilauksia järjestelmään. Tilaukseen kirjataan osoite, hinta, ikkunoiden määrä sekä arvioitu pesuajankohta.
* Käyttäjä pystyy muokkaamaan ja poistamaan lisäämiään tilauksia (esim. yhteystietojen tai pesupäivän muuttuessa).
* Käyttäjä näkee listan kaikista tulevista ikkunanpesuista aikajärjestyksessä.
* Käyttäjä pystyy etsimään tilauksia hakusanalla (esim. osoitteen perusteella) tai suodattamaan niitä tilan mukaan.
* Sovelluksessa on käyttäjäsivut, jotka näyttävät myyjäkohtaisia tilastoja (esim. myytyjen pesujen määrä ja kokonaisarvo) sekä listan kyseisen käyttäjän lisäämistä kohteista.
* Käyttäjä pystyy valitsemaan tilaukselle yhden tai useamman luokittelun (esim. kohdetyyppi: omakotitalo, rivitalo tai liiketila).
* Käyttäjä pystyy päivittämään tilauksen tilaa työn edetessä: merkinnät työn suorittamisesta, laskun lähettämisestä ja maksun vastaanottamisesta.

## Sovelluksen asennus

Asenna `flask`-kirjasto:

```bash
$ pip install flask

Luo tietokannan

$ sqlite3 database.db < schema.sql

Voit käynnistää sovelluksen näin

$ flask run


