# What does this implement/fix?

<!-- Quick description and explanation of changes -->

## Types of changes

<!-- Release notes are generated from PR labels, so apply the matching label as well. -->

- [ ] Bugfix (non-breaking change which fixes an issue) — label: `bugfix`
- [ ] Enhancement (non-breaking change which improves an existing configuration) — label: `enhancement`
- [ ] Breaking change (fix or change that alters existing behaviour, e.g. renamed entities) — label: `breaking-change`
- [ ] Dependency update (actions, reusable workflows or ESPHome version) — label: `dependencies`
- [ ] Other

**Related issue (if applicable):**

- fixes <link to issue>

## Checklist

- [ ] The configuration compiles and has been tested on a real device where possible.
- [ ] `yamllint --strict .` passes.

If `esphome-web` configurations were changed:

- [ ] The change was made in `scripts/generate_esphome_web_configs.py` (not by hand-editing the generated YAML) and the configs were regenerated with `python3 scripts/generate_esphome_web_configs.py`.

If a configuration was added or renamed:

- [ ] It follows the naming convention CI discovers automatically: `esp-web-tools/<chip>.yaml` or `esphome-web/<chip>.factory.yaml` — no `build.yml` edits needed.
