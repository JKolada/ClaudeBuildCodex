# 0002 — Monetyzacja i integracja płatności

> Status: **planowany / niezrealizowany.** Brak hands-on experience — **świadomie nie powstał rozdział
> doktryny** o płatnościach. Data: 2026-06-18.

## Dlaczego to plan, a nie rozdział

The Craft opisuje to, co **przeżyte i zweryfikowane** (Przykazanie III: *weryfikuj, nie deklaruj*).
Monetyzacji i integracji płatności **jeszcze nie wdrożyliśmy** w projekcie referencyjnym — więc nie
piszemy o nich reguł, bo nie mamy z czego destylować antywzorców. Ten plan trzyma **kierunek i pytania
do rozstrzygnięcia**, gdy realnie to zrobimy. Dopiero **lekcje z wdrożenia** awansują do rozdziału
(np. „15 — Płatności") z prawdziwymi „dlaczego" i antywzorcami z życia.

> Brief (rozdz. 07) już **pyta** o monetyzację — ale „zaplanować" to nie „mieć wdrożone". Tu trzymamy
> granicę: pytanie o monetyzację jest w doktrynie, *implementacja płatności* czeka na hands-on.

## Zakres do pokrycia (gdy ruszymy)

- **Model**: jednorazowo / subskrypcja / freemium / usage-based; kiedy płatność (Dzień 1 vs po trakcji).
  Spina się z briefem (→ [07](../../07-new-project-day-0.md)) i prawem (→ [09](../../09-law-and-protecting-the-creator.md)).
- **Dostawca**: domyślnie zarządzany (Stripe / Paddle / LemonSqueezy). **Nigdy nie przechowuj danych
  karty** — deleguj do dostawcy (PCI poza naszym zakresem). Klucze w secret store, nie w repo (→ [08](../../08-stack-and-technologies.md)).
- **Webhooks**: weryfikacja podpisu, **idempotencja po `event id`**, retry, kolejność zdarzeń,
  reconciliation ze stanem w bazie (→ [04](../../04-scripts-and-databases.md), [14](../../14-operational-resilience.md)).
- **Model danych**: subskrypcje / faktury / transakcje jako osobne tabele, stabilne klucze (slug),
  status jako active-row, brak denormalizacji bez źródła prawdy (→ [11](../../11-data-model-and-normalization.md)).
- **Podatki i prawo**: VAT/OSS, miejsce świadczenia, faktury; merchant-of-record (Paddle/LemonSqueezy)
  vs własne rozliczanie VAT; zgody i RODO przy danych płatniczych (→ [09](../../09-law-and-protecting-the-creator.md)).
- **Bezpieczeństwo i nadużycia**: kwoty/rate-limit na płatnych endpointach (już w [14](../../14-operational-resilience.md)),
  idempotentne tworzenie zamówień, ochrona przed fraudem i double-charge.
- **Testy**: tryb testowy dostawcy, webhooki w CI, scenariusze brzegowe (płatność nieudana, chargeback,
  anulowanie, proracja, zwrot) (→ [03](../../03-testing-and-verification.md)).
- **Wdrożenie**: środowiska test/live, runbook + rollback, monitoring nieudanych płatności (→ [05](../../05-git-and-deployments.md)).

## Otwarte pytania

- Dostawca: Stripe (pełna kontrola, własny VAT) vs merchant-of-record (Paddle/LemonSqueezy — VAT na nich)?
- Płatność w MVP czy później?
- Self-service billing vs faktury ręczne na start?

## Następny krok

**Brak — czekamy, aż realny projekt wprowadzi płatności.** Wtedy: zbieramy lekcje w runbooku
(→ [05](../../05-git-and-deployments.md), [06](../../06-collaboration-and-memory.md)), a sprawdzone reguły
awansują do rozdziału doktryny. Do tego czasu ten plik jest jedynym miejscem, gdzie temat „żyje".
