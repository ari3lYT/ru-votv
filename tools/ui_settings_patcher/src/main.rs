use std::collections::HashMap;
use std::fs::{self, File, OpenOptions};
use std::path::PathBuf;

use anyhow::{bail, Context, Result};
use unreal_asset::engine_version::EngineVersion;
use unreal_asset::exports::ExportNormalTrait;
use unreal_asset::properties::Property;
use unreal_asset::Asset;

#[derive(Default)]
struct Stats {
    text_properties: usize,
    str_properties: usize,
    text_updates: usize,
    str_updates: usize,
}

fn apply_translation(value: &mut Option<String>, translations: &HashMap<String, String>) -> bool {
    let Some(current) = value.as_deref() else {
        return false;
    };
    let Some(translated) = translations.get(current) else {
        return false;
    };
    if translated.is_empty() || translated == current {
        return false;
    }
    *value = Some(translated.clone());
    true
}

fn visit_property(prop: &mut Property, translations: &HashMap<String, String>, stats: &mut Stats) {
    match prop {
        Property::TextProperty(text) => {
            stats.text_properties += 1;
            let mut updated = false;
            updated |= apply_translation(&mut text.culture_invariant_string, translations);
            updated |= apply_translation(&mut text.value, translations);
            if updated {
                stats.text_updates += 1;
            }
        }
        Property::StrProperty(text) => {
            stats.str_properties += 1;
            if apply_translation(&mut text.value, translations) {
                stats.str_updates += 1;
            }
        }
        Property::StructProperty(value) => {
            for child in &mut value.value {
                visit_property(child, translations, stats);
            }
        }
        Property::ArrayProperty(value) => {
            for child in &mut value.value {
                visit_property(child, translations, stats);
            }
        }
        Property::SetProperty(value) => {
            for child in &mut value.removed_items.value {
                visit_property(child, translations, stats);
            }
            for child in &mut value.value.value {
                visit_property(child, translations, stats);
            }
        }
        Property::MapProperty(value) => {
            if let Some(keys) = &mut value.keys_to_remove {
                for child in keys {
                    visit_property(child, translations, stats);
                }
            }
            for (_, _key, map_value) in value.value.iter_mut() {
                visit_property(map_value, translations, stats);
            }
        }
        _ => {}
    }
}

fn main() -> Result<()> {
    let mut args = std::env::args_os().skip(1);
    let input_uasset = PathBuf::from(args.next().context("missing input .uasset path")?);
    let input_uexp = PathBuf::from(args.next().context("missing input .uexp path")?);
    let map_path = PathBuf::from(args.next().context("missing ui_settings_map.json path")?);
    let output_uasset = PathBuf::from(args.next().context("missing output .uasset path")?);
    let output_uexp = PathBuf::from(args.next().context("missing output .uexp path")?);
    if args.next().is_some() {
        bail!("too many arguments");
    }

    let map_data = fs::read_to_string(&map_path)
        .with_context(|| format!("failed to read {}", map_path.display()))?;
    let translations: HashMap<String, String> = serde_json::from_str(&map_data)
        .with_context(|| format!("failed to parse {}", map_path.display()))?;

    let uasset = File::open(&input_uasset)
        .with_context(|| format!("failed to open {}", input_uasset.display()))?;
    let uexp = File::open(&input_uexp)
        .with_context(|| format!("failed to open {}", input_uexp.display()))?;
    let mut asset = Asset::new(uasset, Some(uexp), EngineVersion::VER_UE4_27)
        .with_context(|| format!("failed to parse {}", input_uasset.display()))?;

    let mut stats = Stats::default();
    for export in &mut asset.asset_data.exports {
        if let Some(normal) = export.get_normal_export_mut() {
            for property in &mut normal.properties {
                visit_property(property, &translations, &mut stats);
            }
        }
    }

    if stats.text_updates == 0 && stats.str_updates == 0 {
        bail!("no ui_settings strings were updated; the map probably does not match this asset");
    }

    if let Some(parent) = output_uasset.parent() {
        fs::create_dir_all(parent)?;
    }
    if let Some(parent) = output_uexp.parent() {
        fs::create_dir_all(parent)?;
    }

    let mut out_uasset = OpenOptions::new()
        .read(true)
        .write(true)
        .create(true)
        .truncate(true)
        .open(&output_uasset)
        .with_context(|| format!("failed to create {}", output_uasset.display()))?;
    let mut out_uexp = OpenOptions::new()
        .read(true)
        .write(true)
        .create(true)
        .truncate(true)
        .open(&output_uexp)
        .with_context(|| format!("failed to create {}", output_uexp.display()))?;

    asset
        .write_data(&mut out_uasset, Some(&mut out_uexp))
        .with_context(|| format!("failed to write {}", output_uasset.display()))?;

    println!(
        "patched text={}/{} str={}/{}",
        stats.text_updates, stats.text_properties, stats.str_updates, stats.str_properties
    );
    Ok(())
}
