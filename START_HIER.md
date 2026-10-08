# Jouw GitHub-profiel: ElitaZ98

Deze ZIP bevat een complete aangepaste versie van het oorspronkelijke geanimeerde profiel. De opmaak is behouden: een bijdragegrafiek bovenaan, een geanimeerd ASCII-portret links en een geanimeerde statistiekenkaart rechts. De gebruikersnaam, profielfoto en statistieken horen bij `ElitaZ98`.

## Installatie op Windows met GitHub Desktop

1. Controleer dat op GitHub een **openbare** repository bestaat die precies `ElitaZ98` heet, onder het account `ElitaZ98`. Ga naar `https://github.com/ElitaZ98/ElitaZ98`. Initialiseren met een README mag.
2. Kies in **GitHub Desktop** **File > Clone repository** en selecteer `ElitaZ98/ElitaZ98`. Gebruik een nieuwe, lege lokale map als je nog een oude kloon hebt. Je hoeft je oude bestanden niet zomaar te verwijderen.
3. **Pak deze ZIP uit in een tijdelijke map.** Selecteer alle uitgepakte bestanden en mappen en kopieer ze naar de **hoofdmap van de kloon**. Kies **Bestanden vervangen** bij `README.md`.
4. Controleer in die hoofdmap of je deze paden ziet:
   - `.github/workflows/update-profile-art.yml`
   - `scripts/fetch_contributions.py`
   - `scripts/generate_streak_svg.py`
   - `scripts/render_stats_svg.py`
   - `data/contributions.json`
   - `README.md`, `avi-ascii.svg`, `stats.svg` en `contrib-heatmap.svg`
5. Ga terug naar **GitHub Desktop > Changes**. Daar moeten onder andere de map `.github/workflows`, de scripts en de SVG's tussen de wijzigingen staan. Schrijf als samenvatting `Animated GitHub profile for ElitaZ98`, klik **Commit to main** en daarna **Push origin**.
6. Ga naar `https://github.com/ElitaZ98/ElitaZ98/actions`. Open **Update profile art** en kies **Run workflow** op branch **main**. Door de push kan deze workflow ook al automatisch zijn gestart.
7. Wacht tot de workflow een **groen vinkje** heeft en open `https://github.com/ElitaZ98`. Vernieuw met **Ctrl+F5**. De aanvankelijke tekst 'Awaiting first refresh' wordt dan door je echte bijdragen en grafiek vervangen.

**Let op:** de ZIP zelf uploaden als één bestand naar GitHub werkt niet. Je moet de **inhoud** plaatsen met behoud van de mappenstructuur. Vooral `.github` mag niet ontbreken. Het ZIP-bestand bevat de repositorybestanden al op het hoogste niveau; er zit geen extra `AVIVASHISHTA29-main`-map in.

## Als de GitHub Action faalt

- Bij **Permission denied / Resource not accessible by integration**: kijk onder **Repository > Settings > Actions > General > Workflow permissions** of **Read and write permissions** is toegestaan. Sla op en start de workflow opnieuw. Als de instelling niet aanpasbaar is, kan een repository- of organisatiebeleid dit blokkeren.
- Bij **No calendar cells / GitHub markup**: GitHub heeft mogelijk zijn HTML aangepast of blokkeert het verzoek tijdelijk. Het script stopt bewust in plaats van verzonnen nulbijdragen te publiceren.
- Ziet je profiel geen nieuwe afbeelding? Controleer eerst in de GitHub-repository of de drie SVG-bestanden werkelijk in de hoofdmap staan en gebruik Ctrl+F5.

## Persoonlijke gegevens

De foto in `source-photo.png` komt uit het gesprek. `scripts/prep_ascii_avatar.py` maakt hiervan `source-prepped.png`, en `scripts/make_ascii_svg.py` genereert `avi-ascii.svg` met dezelfde schrijfanimatie als het origineel. Dit hoeft niet dagelijks te gebeuren.

De oorspronkelijke maker heeft externe Portfolio-, LinkedIn- en Instagram-links. Die heb ik **niet** overgenomen, omdat dat niet jouw profielen zijn. In `README.md` staan alleen links naar jouw echte GitHub-account. Je kunt de externe links daar later vervangen door je eigen websites.

## Automatische updates

De workflow haalt elke dag rond **06:17 UTC** de publiek zichtbare bijdragen van `https://github.com/users/ElitaZ98/contributions` op, genereert daarna `contrib-heatmap.svg` en `stats.svg` en commit de nieuwe resultaten. Er is geen apart persoonlijk toegangstoken nodig; de standaard `GITHUB_TOKEN` van de workflow wordt gebruikt om in de repository te committen.

Het meegestuurde `data/contributions.json` is een **duidelijk gemarkeerde tijdelijke placeholder**. De cijfers zijn niet van een ander account en ook geen verzonnen statistieken: de echte data verschijnen pas na een succesvolle workflow-run.

## Herkomst

Dit pakket is aangepast op basis van `AVIVASHISHTA29-main(1).zip`, dat in het gesprek is aangeleverd. In die bron-ZIP stond geen LICENSE-bestand; controleer de hergebruikvoorwaarden van de oorspronkelijke auteur als je de code verder openbaar verspreidt.
