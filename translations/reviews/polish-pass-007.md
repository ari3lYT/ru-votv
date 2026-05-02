# Polish pass 007: post-import technical audit

Scope:

* added `audit_translation.py` to make the post-import checks reproducible;
* added `apply_safe_fixes.py` for conservative fixes that should survive future imports;
* preserved source/control tokens in rich text commands: `/imagesize`, `/align`, `/padding`;
* fixed clear typos and consistency issues: `ОтменА`, `Нищюган`, `25 баллов`;
* corrected one interaction help row where `{E}` was introduced even though the source uses plain `E`;
* cleaned the repeated `Open Container` hint wording without changing its gameplay meaning.

Validation after the pass:

* CSV rows: 19263;
* empty Russian strings: 0;
* format/control token mismatches: 0;
* configured hard typo hits: 0 for `ОтменА`, `Нищюган`, `баллов`, `сломман`, `радивыш`;
* remaining review buckets are stylistic/contextual, mainly `Помощь и Инфа`, meme text, names, radio titles and duplicate English strings with context-specific Russian variants.
