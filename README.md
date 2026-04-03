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
pip install flask
```

Tietokannan alustaminen:

```bash
python init_db.py
```

Voit käynnistää sovelluksen näin:

```bash
set FLASK_APP=app.py
python -m flask run
```

Testaaminen

    Avaa sovellus selaimessa. Huomaat, että etusivu on tyhjä, koska et ole kirjautunut sisään.

    Mene Rekisteröidy-sivulle ja luo uusi käyttäjätunnus.

    Kirjaudu sisään juuri luomillasi tunnuksilla.

    Lisää uusi tilaus klikkaamalla + Lisää uusi tilaus.

    Kokeile muokata tai poistaa lisäämääsi tilausta etusivun taulukosta.

    Testaa hakutoimintoa kirjoittamalla osa osoitteesta hakukenttään.

