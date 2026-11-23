# Releasing

Releases are CalVer (`YY.M.N`, for example `26.11.2`) and are almost fully automated. A maintainer only has to wait for the draft release to finish building, then run the **Release** workflow.

## How the pipeline fits together

1. **Release Drafter** (`.github/workflows/release-drafter.yml`) runs on every push to `main`. It computes the next CalVer version and creates or updates a single draft release, with the changelog grouped by PR label (see `.github/release-drafter.yml`). Until the firmware is built, the draft body starts with a "DO NOT PUBLISH THIS RELEASE YET!" caution.
2. **Build** (`.github/workflows/build.yml`) runs when Release Drafter completes. It builds every firmware in the `esp-web-tools` and `esphome-web` groups, uploads them to the draft release and removes the caution notice from the draft body once everything is uploaded.
3. **Release** (`.github/workflows/release.yml`) is run manually. It patches the draft's `*.manifest.json` assets with the final release notes and publishes the draft. It runs in the repository's `release` environment, so any protection rules (for example required reviewers) configured there apply.
4. **Publish** (`.github/workflows/publish.yml`) runs automatically on `release: published`. It downloads the release's firmware assets and uploads them to the Cloudflare R2 bucket served at `https://firmware.esphome.io/`. The beta channel is always updated, and the production channel only for releases that are not marked as a pre-release.

## Steps to make a release

1. Merge the PRs you want to ship into `main`. Label them (`breaking-change`, `enhancement`, `bugfix`, `dependencies`) so they land in the right changelog section.
2. Wait for the **Release Drafter** and **Build** runs triggered by the last merge to finish successfully (Actions tab).
3. Open the draft release on the Releases page and check that:
   - the version is the one you expect,
   - the "DO NOT PUBLISH THIS RELEASE YET!" caution is gone,
   - the firmware `.bin` and `*.manifest.json` assets are attached for every device,
   - the changelog looks right. Once the builds have been uploaded you can edit the draft body by hand (reword entries, add highlights or upgrade notes). Click **Save draft** when you are done, never **Publish release**. Publishing from the GitHub UI fails because a repository rule blocks anyone but the workflow from creating tags, and publishing a draft creates its tag. A release must only ever be published through the Release workflow in the next step. Your edits are kept, and the Release workflow uses the body as it stands when it runs, writing it into the manifests as the final release notes.
4. Run the **Release** workflow: Actions tab, **Release**, **Run workflow**, on `main`. Leave `tag` empty to publish the most recent draft, or enter a tag to publish a specific draft. Approve the run if the `release` environment requires it.
5. Wait for the **Publish** run to finish. A green run means the firmware is uploaded. The bucket itself cannot be browsed, so `https://firmware.esphome.io/` and directory URLs return a 404 even when everything worked. To check the result in a browser, open the latest manifests and confirm the `version` field is the release you just made:
   - <https://firmware.esphome.io/esp-web-tools/manifest.json>
   - <https://firmware.esphome.io/esphome-web/manifest.json>

## Troubleshooting

- **The draft still has the caution notice.** The build has not finished or failed. Check the **Build** run. Do not publish until the notice is removed. Re-running a failed Build run (or merging another PR to `main`) rebuilds and re-uploads the assets to the draft.
- **Release fails with "No draft release found".** There is no draft with a real tag. Merging any PR to `main` makes Release Drafter create one.
- **Publish did not run after the release was published.** A release published with the default `GITHUB_TOKEN` does not fire `release: published`. The Release workflow uses the ESPHome GitHub App token (`ESPHOME_GITHUB_APP_CLIENT_ID` variable and `ESPHOME_GITHUB_APP_PRIVATE_KEY` secret) to avoid this. If the App is not configured, the release is published but **Publish** never fires, and `publish.yml` has no manual trigger, so the firmware is not uploaded to R2 until one is added to that workflow.
- **Pull request and manual builds do not touch the draft.** `build.yml` only uploads to the draft when triggered by a Release Drafter run. On pull requests and manual dispatches it only builds, to check the configs compile.
