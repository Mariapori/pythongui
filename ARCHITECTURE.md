# Arkkitehtuurikuvaus: Runescape GUI Application

## 1. Projektin yleiskuvaus
Kyseessä on Python-pohjainen työpöytäsovellus, joka on suunniteltu hakeen ja näyttämään RuneScape-pelaajien tilastoja RuneMetrics-rajapinnan (API) kautta. Sovellus tarjoaa visuaalisen käyttöliittymän pelaajan perustietojen (kuten nimi, sijoitus ja kokonais-XP) sekä yksityiskohtaisten taitotietojen tarkasteluun.

## 2. Teknologiapino (Technology Stack)
*   **Ohjelmointikieli:** Python 3
*   **Käyttöliittymäkirjasto:** `tkinter` (standardi Pythonin GUI-kirjasto)
*   **Tyylittely:** `ttk` (Themed Tkinter) modernimman ulkoasun saavuttamiseksi (`clam`-teema).
*   **Verkkokutsu:** `requests` (HTTP-pyynnöt API-rajapintaan).
*   **Tiedon käsittely:** `json` (API-vastauksien jäsentämiseen).
*   **Kehitysympäristö:** Linux, mahdollista hyödyntäen agenttiavusteista työnkulkua (esim. Gemma-malli).

## 3. Ohjelmistoarkkitehtuuri
Sovellus noudattaa yksinkertaista **Client-Server** -mallia, jossa sovellus toimii asiakasohjelmana (Client) ja RuneMetrics toimii palveluna (Server).

### Komponentit:
1.  **Käyttöliittymäkerros (Frontend - `RunescapeGUI` luokka):**
    *   **Input Frame:** Käyttäjän syöttökenttä tilaston hakemista varten.
    *   **Stats Frame:** Näyttää perustiedot (Nimi, Rank, Total XP, Combat Level) tekstielementteinä.
    *   **Skill Treeview:** Taulukkomuotoinen näkymä, joka listaa taitojen nimet, tasot ja kokonais-XP:t.
    *   **Scrollbar:** Mahdollistaa pitkän taitolistan selaamisen.

2.  **Logiikkakerros (Backend/Logic):**
    *   **Data Fetching:** `fetch_player_data`-metodi hoitavat asynkronisen (tai synkronisen tässä tapauksessa) HTTP-pyynnön API-rajapintaan.
    *   **Data Processing:** `process_and_display_data`-metodi muuntaa JSON-muotoisen datan sovelluksen sisäiseen muotoon ja yhdistää taitojen ID-numerot ihmiselle ymmärrettäviin nimiin (`SKILL_MAP`).
    *   **Error Handling:** Sisältää virheiden hallinnan (verkkovirheet, JSON-virheet, API-virheet), jotka näytetään käyttäjälle `messagebox`-ikkunoilla.

3.  **Ulkoiset palvelut (External API):**
    *   **RuneMetrics API:** Toimittaa reaaliaikaisen datan pelaajien tilastoista.

## 4. Tiedon kulku (Data Flow)
1.  **Käyttäjän toiminta:** Käyttäjä kirjoittaa tilastonimen ja painaa "Fetch Profile" -painiketta.
2.  **Pyyntö:** Sovellus muodostaa URL-osoitteen käyttäjän syötteen perusteella ja lähettää GET-pyynnön RuneMetrics-palvelimelle.
3.  **Vastaus:** Palvelin palauttaa JSON-muotoista dataa.
4.  **Jäsennys:** Sovellus lukee JSON-datan, tarkistaa mahdolliset virheet ja hakee taitojen nimet `SKILL_MAP`-sanakirjasta.
5.  **Päivitys:** GUI-komponentit (Labelit ja Treeview) päivitetään uudella tiedolla.

## 5. Keskeiset rakenteet
*   **`SKILL_MAP`:** Sanakirja, joka toimii sovelluksen sisäisenä tietokantana taitojen ID-tunnusten ja nimien välillä.
*   **`Treeview`:** Käytetään tehokkaana tapana esittää monimutkaista, taulukkomuotoista tietoa (Skill, Level, XP).
