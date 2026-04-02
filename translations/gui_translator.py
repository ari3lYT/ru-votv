#!/usr/bin/env python3
"""Кроссплатформенный GUI-редактор переводов VotV без повторов.

Показывает каждую уникальную английскую строку один раз, а при сохранении
синхронизирует русский перевод по всем строкам с одинаковым english.
"""

from __future__ import annotations

import argparse
import csv
import subprocess
import sys
import tempfile
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

import tkinter as tk
from tkinter import filedialog, font as tkfont, messagebox, ttk


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="GUI для перевода Game_strings.csv без повторов.")
    parser.add_argument(
        "--csv",
        type=Path,
        default=Path("translations/Game/Game_strings.csv"),
        help="Путь до Game_strings.csv",
    )
    parser.add_argument(
        "--locres",
        type=Path,
        default=Path("VotV/Content/Localization/Game/en/Game.locres"),
        help="Путь до базового английского Game.locres",
    )
    parser.add_argument(
        "--output-locres",
        type=Path,
        default=Path("translations/output/Game_ru.locres"),
        help="Куда сохранять собранный Game_ru.locres",
    )
    parser.add_argument(
        "--output-pak",
        type=Path,
        default=Path("translations/output/ZZ_GameRuPatch_P.pak"),
        help="Куда сохранять собранный pak",
    )
    return parser.parse_args()


def normalized(text: str | None) -> str:
    return (text or "").strip()


@dataclass
class CsvRow:
    id: str
    english: str
    russian: str


@dataclass
class GroupRecord:
    english: str
    rows: list[CsvRow] = field(default_factory=list)
    edited_russian: str = ""
    dirty: bool = False

    def __post_init__(self) -> None:
        self.edited_russian = self.pick_best_russian()

    @property
    def count(self) -> int:
        return len(self.rows)

    @property
    def variants(self) -> list[str]:
        return sorted({normalized(row.russian) for row in self.rows if normalized(row.russian)})

    def pick_best_russian(self) -> str:
        values = [normalized(row.russian) for row in self.rows if normalized(row.russian)]
        if not values:
            return ""

        translated = [value for value in values if value != self.english]
        source = translated or values
        return Counter(source).most_common(1)[0][0]

    def status(self) -> str:
        variants = self.variants
        if not variants:
            return "untranslated"
        if len(variants) > 1:
            return "conflict"
        if variants[0] == self.english:
            return "untranslated"
        return "translated"

    def apply_current_translation(self) -> int:
        changed = 0
        for row in self.rows:
            if row.russian != self.edited_russian:
                row.russian = self.edited_russian
                changed += 1
        self.dirty = False
        return changed

    def revert_from_rows(self) -> None:
        self.edited_russian = self.pick_best_russian()
        self.dirty = False


class TranslationProject:
    def __init__(self, csv_path: Path) -> None:
        self.csv_path = csv_path
        self.rows: list[CsvRow] = []
        self.groups: list[GroupRecord] = []
        self.groups_by_english: dict[str, GroupRecord] = {}
        self.load(csv_path)

    def load(self, csv_path: Path) -> None:
        self.csv_path = csv_path
        with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            required = {"id", "english", "russian"}
            missing = required - set(reader.fieldnames or [])
            if missing:
                raise SystemExit(f"{csv_path} пропущены колонки: {', '.join(sorted(missing))}")
            self.rows = [
                CsvRow(
                    id=(row.get("id") or "").strip(),
                    english=row.get("english") or "",
                    russian=row.get("russian") or "",
                )
                for row in reader
            ]

        order: list[str] = []
        groups: dict[str, GroupRecord] = {}
        for row in self.rows:
            if row.english not in groups:
                groups[row.english] = GroupRecord(english=row.english)
                order.append(row.english)
            groups[row.english].rows.append(row)

        self.groups = [groups[key] for key in order]
        self.groups_by_english = groups

    def save(self, output_path: Path | None = None) -> None:
        target = output_path or self.csv_path
        with target.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "english", "russian"])
            writer.writeheader()
            for row in self.rows:
                writer.writerow({"id": row.id, "english": row.english, "russian": row.russian})

    def counts(self) -> tuple[int, int, int]:
        translated = sum(1 for group in self.groups if group.status() == "translated")
        conflicts = sum(1 for group in self.groups if group.status() == "conflict")
        untranslated = sum(1 for group in self.groups if group.status() == "untranslated")
        return translated, conflicts, untranslated

    def sync_all_conflicts(self) -> int:
        changed_groups = 0
        for group in self.groups:
            if group.status() != "conflict":
                continue
            best = group.pick_best_russian()
            if not best:
                continue
            group.edited_russian = best
            if group.apply_current_translation():
                changed_groups += 1
        return changed_groups

    def apply_all_dirty_groups(self) -> int:
        changed_groups = 0
        for group in self.groups:
            if not group.dirty:
                continue
            if group.apply_current_translation():
                changed_groups += 1
        return changed_groups


class TranslatorApp:
    FILTER_LABELS = {
        "all": "Все",
        "untranslated": "Непереведённые",
        "conflict": "Конфликты",
        "translated": "Переведённые",
    }

    def __init__(
        self,
        root: tk.Tk,
        csv_path: Path,
        locres_path: Path,
        output_locres: Path,
        output_pak: Path,
    ) -> None:
        self.root = root
        self.enable_hidpi_awareness()
        self.configure_scaling()
        self.configure_fonts_and_style()
        self.root.title("VotV Translation GUI")
        self.configure_window()

        self.repo_root = Path(__file__).resolve().parents[1]
        self.project = TranslationProject(csv_path)
        self.current_group: GroupRecord | None = None
        self.displayed_groups: list[GroupRecord] = []

        self.csv_var = tk.StringVar(value=str(csv_path))
        self.locres_var = tk.StringVar(value=str(locres_path))
        self.output_locres_var = tk.StringVar(value=str(output_locres))
        self.output_pak_var = tk.StringVar(value=str(output_pak))
        self.search_var = tk.StringVar()
        self.filter_var = tk.StringVar(value="all")
        self.status_var = tk.StringVar()
        self.group_summary_var = tk.StringVar()

        self._build_ui()
        self.refresh_tree()
        self.update_status_bar()

    def enable_hidpi_awareness(self) -> None:
        if sys.platform != "win32":
            return
        try:
            import ctypes

            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            try:
                import ctypes

                ctypes.windll.user32.SetProcessDPIAware()
            except Exception:
                pass

    def configure_scaling(self) -> None:
        try:
            dpi = float(self.root.winfo_fpixels("1i"))
        except Exception:
            dpi = 96.0
        scaling = max(1.15, min(2.2, dpi / 96.0))
        self.ui_scale = scaling
        self.root.tk.call("tk", "scaling", scaling)

    def configure_fonts_and_style(self) -> None:
        style = ttk.Style(self.root)
        try:
            if "clam" in style.theme_names():
                style.theme_use("clam")
        except Exception:
            pass

        base_size = max(12, int(round(11 * self.ui_scale)))
        small_size = max(11, base_size - 1)
        mono_size = max(11, base_size - 1)
        heading_size = max(13, base_size + 1)
        title_size = max(14, base_size + 2)

        ui_family = self.pick_font_family(
            [
                "Noto Sans",
                "DejaVu Sans",
                "Segoe UI",
                "Cantarell",
                "Liberation Sans",
                "Arial",
                "Helvetica",
            ]
        )
        mono_family = self.pick_font_family(
            [
                "Cascadia Mono",
                "Consolas",
                "Noto Sans Mono",
                "DejaVu Sans Mono",
                "Liberation Mono",
                "Courier New",
                "Courier",
            ]
        )

        default_font = tkfont.nametofont("TkDefaultFont")
        text_font = tkfont.nametofont("TkTextFont")
        fixed_font = tkfont.nametofont("TkFixedFont")
        heading_font = tkfont.nametofont("TkHeadingFont")
        menu_font = tkfont.nametofont("TkMenuFont")

        default_font.configure(family=ui_family, size=base_size)
        text_font.configure(family=ui_family, size=base_size)
        fixed_font.configure(family=mono_family, size=mono_size)
        heading_font.configure(family=ui_family, size=heading_size, weight="bold")
        menu_font.configure(family=ui_family, size=base_size)

        self.ui_fonts = {
            "default": default_font,
            "text": text_font,
            "fixed": fixed_font,
            "heading": heading_font,
            "title": tkfont.Font(family=ui_family, size=title_size, weight="bold"),
            "bold": tkfont.Font(family=ui_family, size=base_size, weight="bold"),
            "small": tkfont.Font(family=ui_family, size=small_size),
        }

        rowheight = max(26, int(round(24 * self.ui_scale)))
        padding = max(6, int(round(6 * self.ui_scale)))
        style.configure(".", font=self.ui_fonts["default"])
        style.configure("Treeview", font=self.ui_fonts["default"], rowheight=rowheight)
        style.configure("Treeview.Heading", font=self.ui_fonts["bold"])
        style.configure("TButton", padding=(padding, padding // 2))
        style.configure("TEntry", padding=(padding // 2, padding // 3))
        style.configure("TCombobox", padding=(padding // 2, padding // 3))
        style.configure("TLabelframe.Label", font=self.ui_fonts["bold"])

    def pick_font_family(self, candidates: list[str]) -> str:
        available = {name.lower(): name for name in tkfont.families(self.root)}
        for candidate in candidates:
            if candidate.lower() in available:
                return available[candidate.lower()]
        return tkfont.nametofont("TkDefaultFont").cget("family")

    def configure_window(self) -> None:
        screen_w = max(1280, self.root.winfo_screenwidth())
        screen_h = max(800, self.root.winfo_screenheight())
        width = min(int(screen_w * 0.92), 2200)
        height = min(int(screen_h * 0.9), 1400)
        self.root.geometry(f"{width}x{height}")
        self.root.minsize(1200, 760)

    def _build_ui(self) -> None:
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        outer_pad = max(10, int(round(10 * self.ui_scale)))
        block_pad = max(8, int(round(8 * self.ui_scale)))
        text_height = max(10, int(round(8 * self.ui_scale)))
        ids_height = max(12, int(round(10 * self.ui_scale)))

        toolbar = ttk.Frame(self.root, padding=outer_pad)
        toolbar.grid(row=0, column=0, sticky="nsew")
        toolbar.columnconfigure(1, weight=1)

        ttk.Label(toolbar, text="CSV").grid(row=0, column=0, sticky="w")
        ttk.Entry(toolbar, textvariable=self.csv_var).grid(row=0, column=1, sticky="ew", padx=4)
        ttk.Button(toolbar, text="Открыть CSV", command=self.choose_csv).grid(row=0, column=2, padx=4)
        ttk.Button(toolbar, text="Сохранить", command=self.save_csv).grid(row=0, column=3, padx=4)
        ttk.Button(toolbar, text="Сохранить как", command=self.save_csv_as).grid(row=0, column=4, padx=4)
        ttk.Button(toolbar, text="Синхр. конфликты", command=self.sync_all_conflicts).grid(row=0, column=5, padx=4)

        ttk.Label(toolbar, text="Поиск").grid(row=1, column=0, sticky="w", pady=(8, 0))
        search_entry = ttk.Entry(toolbar, textvariable=self.search_var)
        search_entry.grid(row=1, column=1, sticky="ew", padx=4, pady=(8, 0))
        search_entry.bind("<KeyRelease>", lambda _event: self.refresh_tree())

        filter_box = ttk.Combobox(
            toolbar,
            textvariable=self.filter_var,
            values=list(self.FILTER_LABELS.keys()),
            state="readonly",
            width=20,
        )
        filter_box.grid(row=1, column=2, padx=4, pady=(8, 0))
        filter_box.bind("<<ComboboxSelected>>", lambda _event: self.refresh_tree())
        ttk.Button(toolbar, text="Пред. непереведённый", command=lambda: self.jump_to_status("untranslated", -1)).grid(
            row=1, column=3, padx=4, pady=(8, 0)
        )
        ttk.Button(toolbar, text="След. непереведённый", command=lambda: self.jump_to_status("untranslated", 1)).grid(
            row=1, column=4, padx=4, pady=(8, 0)
        )
        ttk.Button(toolbar, text="След. конфликт", command=lambda: self.jump_to_status("conflict", 1)).grid(
            row=1, column=5, padx=4, pady=(8, 0)
        )

        main = ttk.Panedwindow(self.root, orient=tk.HORIZONTAL)
        main.grid(row=1, column=0, sticky="nsew")

        left = ttk.Frame(main, padding=outer_pad)
        left.columnconfigure(0, weight=1)
        left.rowconfigure(0, weight=1)
        main.add(left, weight=5)

        right = ttk.Frame(main, padding=outer_pad)
        right.columnconfigure(0, weight=1)
        right.rowconfigure(7, weight=1)
        main.add(right, weight=6)

        columns = ("status", "count", "english", "russian")
        self.tree = ttk.Treeview(left, columns=columns, show="headings", selectmode="browse")
        self.tree.heading("status", text="Статус")
        self.tree.heading("count", text="Повт.")
        self.tree.heading("english", text="English")
        self.tree.heading("russian", text="Russian")
        self.tree.column("status", width=120, stretch=False)
        self.tree.column("count", width=70, stretch=False, anchor="center")
        self.tree.column("english", width=420)
        self.tree.column("russian", width=420)
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        tree_scroll = ttk.Scrollbar(left, orient="vertical", command=self.tree.yview)
        tree_scroll.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=tree_scroll.set)

        ttk.Label(right, textvariable=self.group_summary_var, font=self.ui_fonts["title"]).grid(
            row=0, column=0, sticky="w"
        )

        ttk.Label(right, text="English").grid(row=1, column=0, sticky="w", pady=(10, 2))
        self.english_text = tk.Text(
            right,
            height=text_height,
            wrap="word",
            font=self.ui_fonts["text"],
            padx=10,
            pady=10,
        )
        self.english_text.grid(row=2, column=0, sticky="nsew")
        self.english_text.configure(state="disabled")

        ttk.Label(right, text="Russian").grid(row=3, column=0, sticky="w", pady=(10, 2))
        self.russian_text = tk.Text(
            right,
            height=text_height,
            wrap="word",
            font=self.ui_fonts["text"],
            padx=10,
            pady=10,
        )
        self.russian_text.grid(row=4, column=0, sticky="nsew")
        self.russian_text.bind("<<Modified>>", self.on_russian_modified)

        buttons = ttk.Frame(right)
        buttons.grid(row=5, column=0, sticky="w", pady=(8, 0))
        ttk.Button(buttons, text="Применить к группе", command=self.apply_current_group).pack(side=tk.LEFT, padx=(0, 6))
        ttk.Button(buttons, text="Откатить группу", command=self.revert_current_group).pack(side=tk.LEFT, padx=(0, 6))

        ttk.Label(right, text="ID строк в группе").grid(row=6, column=0, sticky="w", pady=(10, 2))
        self.ids_list = tk.Listbox(
            right,
            height=ids_height,
            font=self.ui_fonts["fixed"],
        )
        self.ids_list.grid(row=7, column=0, sticky="nsew")

        build_frame = ttk.LabelFrame(right, text="Сборка", padding=block_pad)
        build_frame.grid(row=8, column=0, sticky="ew", pady=(12, 0))
        build_frame.columnconfigure(1, weight=1)

        ttk.Label(build_frame, text="Base locres").grid(row=0, column=0, sticky="w")
        ttk.Entry(build_frame, textvariable=self.locres_var).grid(row=0, column=1, sticky="ew", padx=4)
        ttk.Button(build_frame, text="...", width=4, command=self.choose_locres).grid(row=0, column=2)

        ttk.Label(build_frame, text="Output locres").grid(row=1, column=0, sticky="w", pady=(6, 0))
        ttk.Entry(build_frame, textvariable=self.output_locres_var).grid(row=1, column=1, sticky="ew", padx=4, pady=(6, 0))
        ttk.Button(build_frame, text="...", width=4, command=self.choose_output_locres).grid(row=1, column=2, pady=(6, 0))

        ttk.Label(build_frame, text="Output pak").grid(row=2, column=0, sticky="w", pady=(6, 0))
        ttk.Entry(build_frame, textvariable=self.output_pak_var).grid(row=2, column=1, sticky="ew", padx=4, pady=(6, 0))
        ttk.Button(build_frame, text="...", width=4, command=self.choose_output_pak).grid(row=2, column=2, pady=(6, 0))

        build_buttons = ttk.Frame(build_frame)
        build_buttons.grid(row=3, column=0, columnspan=3, sticky="w", pady=(8, 0))
        ttk.Button(build_buttons, text="Build locres", command=self.build_locres).pack(side=tk.LEFT, padx=(0, 6))
        ttk.Button(build_buttons, text="Pack pak", command=self.pack_pak).pack(side=tk.LEFT)

        status = ttk.Label(
            self.root,
            textvariable=self.status_var,
            padding=outer_pad,
            relief=tk.SUNKEN,
            anchor="w",
            font=self.ui_fonts["small"],
        )
        status.grid(row=2, column=0, sticky="ew")

    def set_status(self, text: str) -> None:
        self.status_var.set(text)

    def update_status_bar(self) -> None:
        translated, conflicts, untranslated = self.project.counts()
        self.set_status(
            f"Групп: {len(self.project.groups)} | Переведено: {translated} | Конфликтов: {conflicts} | Непереведено: {untranslated}"
        )

    def choose_csv(self) -> None:
        path = filedialog.askopenfilename(
            title="Открыть Game_strings.csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialdir=str(Path(self.csv_var.get()).resolve().parent),
        )
        if not path:
            return
        self.load_project(Path(path))

    def choose_locres(self) -> None:
        path = filedialog.askopenfilename(title="Выбрать базовый Game.locres")
        if path:
            self.locres_var.set(path)

    def choose_output_locres(self) -> None:
        path = filedialog.asksaveasfilename(title="Куда сохранить Game_ru.locres", defaultextension=".locres")
        if path:
            self.output_locres_var.set(path)

    def choose_output_pak(self) -> None:
        path = filedialog.asksaveasfilename(title="Куда сохранить pak", defaultextension=".pak")
        if path:
            self.output_pak_var.set(path)

    def load_project(self, csv_path: Path) -> None:
        try:
            self.project = TranslationProject(csv_path)
        except Exception as exc:
            messagebox.showerror("Ошибка загрузки", str(exc))
            return

        self.csv_var.set(str(csv_path))
        self.current_group = None
        self.refresh_tree()
        self.update_status_bar()
        self.group_summary_var.set("")
        self.set_english_text("")
        self.set_russian_text("")
        self.ids_list.delete(0, tk.END)

    def filtered_groups(self) -> list[GroupRecord]:
        query = self.search_var.get().strip().lower()
        filter_value = self.filter_var.get()
        results: list[GroupRecord] = []
        for group in self.project.groups:
            status = group.status()
            if filter_value != "all" and status != filter_value:
                continue
            haystack = f"{group.english}\n{group.edited_russian}".lower()
            if query and query not in haystack:
                continue
            results.append(group)
        return results

    def refresh_tree(self) -> None:
        self.commit_editor_to_group()
        current_english = self.current_group.english if self.current_group else None

        for item in self.tree.get_children():
            self.tree.delete(item)

        self.displayed_groups = self.filtered_groups()
        selected_item = None
        for index, group in enumerate(self.displayed_groups):
            russian_preview = group.edited_russian.replace("\n", " ")
            english_preview = group.english.replace("\n", " ")
            item_id = self.tree.insert(
                "",
                "end",
                iid=str(index),
                values=(
                    group.status(),
                    group.count,
                    self.truncate(english_preview, 90),
                    self.truncate(russian_preview, 90),
                ),
            )
            if current_english and group.english == current_english:
                selected_item = item_id

        if selected_item is None and self.displayed_groups:
            selected_item = "0"

        if selected_item is not None:
            self.tree.selection_set(selected_item)
            self.tree.focus(selected_item)
            self.show_group(self.displayed_groups[int(selected_item)])

        self.update_status_bar()

    def truncate(self, text: str, limit: int) -> str:
        return text if len(text) <= limit else text[: limit - 1] + "…"

    def on_tree_select(self, _event: tk.Event | None = None) -> None:
        selection = self.tree.selection()
        if not selection:
            return
        index = int(selection[0])
        if not (0 <= index < len(self.displayed_groups)):
            return
        self.commit_editor_to_group()
        self.show_group(self.displayed_groups[index])

    def show_group(self, group: GroupRecord) -> None:
        self.current_group = group
        self.group_summary_var.set(
            f"Статус: {group.status()} | Повторов: {group.count} | Вариантов перевода: {len(group.variants)}"
        )
        self.set_english_text(group.english)
        self.set_russian_text(group.edited_russian)
        self.ids_list.delete(0, tk.END)
        for row in group.rows:
            self.ids_list.insert(tk.END, row.id)

    def set_english_text(self, text: str) -> None:
        self.english_text.configure(state="normal")
        self.english_text.delete("1.0", tk.END)
        self.english_text.insert("1.0", text)
        self.english_text.configure(state="disabled")

    def set_russian_text(self, text: str) -> None:
        self.russian_text.delete("1.0", tk.END)
        self.russian_text.insert("1.0", text)
        self.russian_text.edit_modified(False)

    def on_russian_modified(self, _event: tk.Event | None = None) -> None:
        if not self.russian_text.edit_modified():
            return
        if self.current_group is not None:
            self.current_group.edited_russian = self.russian_text.get("1.0", tk.END).rstrip("\n")
            self.current_group.dirty = True
        self.russian_text.edit_modified(False)

    def commit_editor_to_group(self) -> None:
        if self.current_group is None:
            return
        current_text = self.russian_text.get("1.0", tk.END).rstrip("\n")
        if self.current_group.edited_russian != current_text:
            self.current_group.edited_russian = current_text
            self.current_group.dirty = True

    def apply_current_group(self) -> None:
        if self.current_group is None:
            return
        self.commit_editor_to_group()
        changed = self.current_group.apply_current_translation()
        self.refresh_tree()
        self.set_status(f"Группа применена: изменено строк {changed}")

    def revert_current_group(self) -> None:
        if self.current_group is None:
            return
        self.current_group.revert_from_rows()
        self.show_group(self.current_group)
        self.refresh_tree()
        self.set_status("Изменения группы отменены.")

    def sync_all_conflicts(self) -> None:
        self.commit_editor_to_group()
        changed_groups = self.project.sync_all_conflicts()
        self.refresh_tree()
        self.set_status(f"Синхронизировано конфликтующих групп: {changed_groups}")

    def save_csv(self) -> None:
        self.commit_editor_to_group()
        self.project.apply_all_dirty_groups()
        try:
            self.project.save()
        except Exception as exc:
            messagebox.showerror("Ошибка сохранения", str(exc))
            return
        self.refresh_tree()
        self.set_status(f"CSV сохранён: {self.project.csv_path}")

    def save_csv_as(self) -> None:
        self.commit_editor_to_group()
        self.project.apply_all_dirty_groups()
        path = filedialog.asksaveasfilename(
            title="Сохранить CSV как",
            defaultextension=".csv",
            initialfile=self.project.csv_path.name,
        )
        if not path:
            return
        target = Path(path)
        try:
            self.project.save(target)
        except Exception as exc:
            messagebox.showerror("Ошибка сохранения", str(exc))
            return
        self.project.csv_path = target
        self.csv_var.set(str(target))
        self.refresh_tree()
        self.set_status(f"CSV сохранён: {target}")

    def jump_to_status(self, status: str, direction: int) -> None:
        if not self.displayed_groups:
            return
        selection = self.tree.selection()
        start = int(selection[0]) if selection else 0
        indices = range(start + direction, len(self.displayed_groups), direction) if direction > 0 else range(start + direction, -1, direction)
        for index in indices:
            if self.displayed_groups[index].status() == status:
                self.tree.selection_set(str(index))
                self.tree.focus(str(index))
                self.tree.see(str(index))
                self.show_group(self.displayed_groups[index])
                return
        messagebox.showinfo("Поиск", f"Больше нет групп со статусом {status}.")

    def build_locres(self) -> None:
        self.save_csv()
        command = [
            sys.executable,
            str(self.repo_root / "translations" / "build_game_locres.py"),
            "--strings",
            self.csv_var.get(),
            "--locres",
            self.locres_var.get(),
            "--output",
            self.output_locres_var.get(),
        ]
        self.run_command(command, success_message="Game_ru.locres собран.")

    def pack_pak(self) -> None:
        output_locres = Path(self.output_locres_var.get())
        if not output_locres.exists():
            if not messagebox.askyesno(
                "locres не найден",
                "Сначала нужно собрать Game_ru.locres. Собрать сейчас?",
            ):
                return
            self.build_locres()
            if not output_locres.exists():
                return

        with tempfile.TemporaryDirectory(prefix="votv-pack-") as temp_dir:
            stage = Path(temp_dir) / "Game_ru"
            locres_target = stage / "Localization" / "Game" / "ru" / "Game.locres"
            locres_target.parent.mkdir(parents=True, exist_ok=True)
            locres_target.write_bytes(output_locres.read_bytes())

            command = [
                sys.executable,
                str(self.repo_root / "tools" / "pack.py"),
                str(stage),
                self.output_pak_var.get(),
                "--mount-point",
                "../../../VotV/Content/",
            ]
            self.run_command(command, success_message="Pak собран.")

    def run_command(self, command: list[str], success_message: str) -> None:
        try:
            result = subprocess.run(
                command,
                cwd=self.repo_root,
                check=True,
                text=True,
                capture_output=True,
            )
        except subprocess.CalledProcessError as exc:
            message = exc.stderr.strip() or exc.stdout.strip() or str(exc)
            messagebox.showerror("Ошибка команды", message)
            self.set_status(f"Ошибка: {message}")
            return

        stdout = result.stdout.strip()
        if stdout:
            self.set_status(stdout.splitlines()[-1])
        else:
            self.set_status(success_message)
        messagebox.showinfo("Готово", stdout or success_message)


def main() -> None:
    args = parse_args()
    root = tk.Tk()
    app = TranslatorApp(
        root=root,
        csv_path=args.csv.resolve(),
        locres_path=args.locres.resolve() if args.locres.exists() else args.locres,
        output_locres=args.output_locres.resolve() if args.output_locres.exists() else args.output_locres,
        output_pak=args.output_pak.resolve() if args.output_pak.exists() else args.output_pak,
    )
    root.mainloop()


if __name__ == "__main__":
    main()
