# AUAG NAV – AppDaemon (Home Assistant)

Denne AppDaemon-appen:
- beregner estimert NAV for AUAG-portefølje
- kjører automatisk hver kveld kl. 22:30
- sender resultatet som pushmelding

---

## 1. Krav
- Home Assistant
- AppDaemon addon
- Push-varsling satt opp (mobile_app)

---

## 2. Filplassering

Legg koden i:

/config/appdaemon/apps/auag_nav.py


---

## 3. apps.yaml

Rediger eller lag:

/config/appdaemon/apps/apps.yaml


Innhold:
```yaml
auag_nav:
  module: auag_nav
  class: AUAGNav
```
---
## 4. Push-varsling

I koden, bytt:

```yaml
notify/mobile_app_din_telefon
```

til riktig notify-tjeneste fra Home Assistant.
---
## 5. Hvordan kjører den?

Koden inneholder:

self.run_daily(self.run_report, "22:30:00")

Det betyr:

    ingen automasjon i Home Assistant

    AppDaemon kjører jobben selv hver kveld
---
## 6. Test manuelt (valgfritt)

For å teste med én gang, legg midlertidig i initialize():

self.run_report({})

Restart AppDaemon → du får pushmelding.
Fjern linjen etter test.

---
## 7. Endre innhold

    Aksjer og vekter: HOLDINGS

    Tidspunkt: "22:30:00"

    Tittel / tekst: run_report()

## 8. Ferdig

Når AppDaemon kjører:

    NAV beregnes daglig

    pushmelding sendes automatisk

    ingen videre oppfølging nødvendig


    ---

    ## Eksempel på sensorkort

    self.set_state(
    "sensor.auag_nav_change",
    state=round(avg_change, 2),
    attributes={
        "unit_of_measurement": "%",
        "friendly_name": "AUAG NAV endring"
    }
)
