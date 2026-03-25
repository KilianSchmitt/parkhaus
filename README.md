# Parkhaus Domain Modell

Parkhaus ist das Aggregate-Root und steht mit der Adresse in einer 1:1 Beziehung. Desweiteren steht Parkhaus mit Auto in einer 1:N Beziehung.

```json
{
  "parkhaus": {
    "name": "Zentral-Garage Bellheim",
    "kapazitaet": 150,
    "tarif_pro_stunde": 2.50,
    "adresse": {
      "plz": "10115",
      "ort": "Berlin",
      "straße": "Müllerstraße",
      "hausnummer": "42"
    },
    "autos": [
      {
        "kennzeichen": "B-MW-1234",
        "einfahrtszeit": "2026-03-25T10:30:00Z",
        "kundentyp": "PREMIUM"
      },
      {
        "kennzeichen": "S-AU-88",
        "einfahrtszeit": "2026-03-25T11:15:00Z",
        "kundentyp": "BASIS"
      },
      {
        "kennzeichen": "D-OR-123",
        "einfahrtszeit": "2026-03-25T08:00:00Z",
        "kundentyp": "ANWOHNER"
      }
    ]
  }
}