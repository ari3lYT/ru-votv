# Polish pass 006: final latin/same-string audit

Scope:

* audited remaining strings where Russian equals English;
* left technical formats, URLs, corrupted in-game text and names untouched;
* fixed obvious real misses from the Latin audit: ATV controls, password prompt, help search names, floppy action, daily task summaries and custom assets wording.

Validation after the pass:

* CSV rows: 19263;
* translated rows: 19263;
* format mismatches for `{...}`, `<...>`, `/image`, `/imagesize`, `/align`: 0;
* bad drive / upgrade terminology hits in Russian text: 0;
* bad settings/UI terminology hits in Russian text: 0;
* exact bad help/final-audit terms checked: 0;
* raw `RMB` / `LMB` / `MMB` in Russian text: 0;
* NBSP / zero-width / BOM in Russian text: 0.
