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
* Käyttäjä pystyy kommentoimaan toisten käyttäjien luomiin tilauksiin.

## Sovelluksen asennus

### 1. Virtuaalisen ympäristön luominen ja aktivoiminen

Luo virtuaalinen ympäristö:

```bash
python -m venv venv
```

Aktivoi virtuaalinen ympäristö:

**Linux/macOS:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### 2. Riippuvuuksien asentaminen

Asenna kaikki vaadittavat kirjastot:

```bash
pip install -r requirements.txt
```

### 3. Tietokannan alustaminen

```bash
python init_db.py
```

### 4. Sovelluksen käynnistäminen

```bash
python -m flask run
```

Sovellus aukeaa osoitteessa `http://127.0.0.1:5000`

### Huomio: Salaisuuden hallinta

Sovellus käyttää `.env`-tiedostoa salaisuuksien hallintaan. Tämä tiedosto on otettu `.gitignore`-tiedostoon, eikä se lähde versionhallintaan. Sovellus lataa salaisuuksia automaattisesti `.env`-tiedostosta käynnistyksen yhteydessä.

Testaaminen

    Avaa sovellus selaimessa. Huomaat, että etusivu on tyhjä, koska et ole kirjautunut sisään.

    Mene Rekisteröidy-sivulle ja luo uusi käyttäjätunnus.

    Kirjaudu sisään juuri luomillasi tunnuksilla.

    Lisää uusi tilaus klikkaamalla + Lisää uusi tilaus.

    Kokeile muokata tai poistaa lisäämääsi tilausta etusivun taulukosta.

    Testaa hakutoimintoa kirjoittamalla osa osoitteesta hakukenttään.

Välipalautus 3: (Versio 2.0)

    Käyttäjäsivuja voi testata luomalla useampi käyttäjä jolla kirjautua.

    Näytä näkymän takana on kommenttimahdollisuudet.

    Luokitteluja (Tila "Odottaa") täytyy ensin olla kohde luotu jonka jälkeen muokkaa painikkeesta voi vaihtaa tilaa.






