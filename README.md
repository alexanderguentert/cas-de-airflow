# CAS Data Engineering Airflow
Dies ist ein Proof of Concept für Datenaktualsierungspipelines mit Airflow für OpenDataZurich. Es wurde erstellt als Prüfungsleistung im Rahmen des [CAS Data Engineering der FHNW](https://www.fhnw.ch/de/weiterbildung/informatik/cas-data-engineering). Die Prüfungsleistung wird beurteilt von [Tobias Kaymak](https://github.com/tkaymak).

# Lokales Testen
- In diesem Repo wird die Astronomer Version von Airflow verwendet. Um das lokal ausprobieren zu können sollte vorher das `astro` CLI installiert werden, wie [hier](https://www.astronomer.io/docs/astro/cli/install-cli) beschrieben.
- Dieses Repo in einen lokalen Ordner klonen und den Ordner in der Console öffnen.
- Initialisieren des astro Projektes mit `astro dev init`. Man wird gefragt, ob man das wirklich möchte, weil es im Ordner schon Dateien hat. Antwort `y`.
- Das Projekt starten mit `astro dev start`
- Nötigen Container werden geladen und gestartet. Wenn alles klappt, öffnet sich eine Seite im Browser mit Airflow. Die Adresse ist: [http://localhost:8080/](http://localhost:8080/).
- Beenden mit `astro dev stop`

**Secrets:**
Damit der DAG komplett durchläuft, werden Zugangsdaten gebraucht. Diese können in einer `.env` lokal im Ordner abgelegt werden. Folgende Variablen werden benötigt:
```
CKAN_BASE_URL_INT=https://ckan-staging.zurich.datopian.com/
CKAN_API_KEY_INT=...
GOOGLE_API=...
```
Die CKAN Variablen werden benötigt, um den Datensatz auf den Open Data Katalog der Stadt Zürich zu laden. Der Google-API Key wird benötigt, weil beim Updateprozess auch eine Dokumentenzusammenfassung über [Gemini](https://gemini.google.com) gemacht werden. Einen API Key dafür kann man hier anlegen: https://aistudio.google.com/api-keys


# Ist-Zustand

# Zielarchitektur

# Technologie Entscheidungen

# Fazit/Ausblick
