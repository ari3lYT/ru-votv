# Polish pass 005: long help/tutorial strings

Scope:

* cleaned long tutorial pages for HOLD/GRAB wording;
* fixed repeated sponge, pencil and disassembly descriptions;
* rewrote data reel, garbage bag, precise placement, concrete repair, camera and coughing help pages;
* fixed printer custom-model help so required filenames and prefixes stay exact.

Validation after the pass:

* CSV rows: 19263;
* translated rows: 19263;
* format mismatches for `{...}`, `<...>`, `/image`, `/imagesize`, `/align`: 0;
* exact bad help terms checked: 0;
* raw `RMB` / `LMB` / `MMB` in Russian text: 0;
* translated printer filename tokens such as `диффузный_`, `ТестМодель`, `emmissive_`: 0;
* NBSP / zero-width / BOM in Russian text: 0.
