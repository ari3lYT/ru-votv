# Polish pass 008: strict contextual polish

Scope:

* standardized `Help & Info` / `Hints and Tips` as `Справка и советы`;
* removed visible machine wording around custom content, TV, 3D printers, keypads and controls;
* fixed the 3D printer size loss from `200x300` back to `200x200x300`;
* translated remaining obvious same-as-English UI/color terms: `Auto`, `Red`, `Green`, `Charcoal`, `Snap`, `Towers`, `Wip`, `Unknown device`, etc.;
* normalized repeated duplicate translations where the English source and context were the same;
* left intentionally corrupted/stylized strings, file paths, radio names, brands, commands and IDs untouched.

Validation after the pass:

* CSV rows: 19263;
* empty Russian strings: 0;
* format/control token mismatches: 0;
* configured suspicious term hits: 0;
* duplicate English groups with variant Russian: 34, mostly context-sensitive or intentionally stylized.
