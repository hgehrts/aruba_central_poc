# Firmware check

This page explains the **Firmware and security** dashboard of the app `aruba_network_insights`: what it does, how to
read it, and how to keep its data current. It assumes that you know Aruba (Central, AOS-10, AOS-8 Instant) but
not Splunk. Terms from Splunk are explained where they appear.

<!-- md-only -->
The same text is available inside the app under **Risk > Firmware check help**, together with live views of
the lists and a check for typing mistakes.
<!-- /md-only -->

## 1. What it does

The firmware check compares the software version of every access point that Aruba Central reports with two
reference lists:

1. **Fixed versions (baseline).** For each software train (for example AOS-10.8, AOS-10.7, AOS-8.13) the
   first version that contains the fix of an HPE security advisory. The shipped list holds the versions of
   advisory [HPESBNW05162](https://csaf.arubanetworking.hpe.com/2026/hpe_networking_-_hpesbnw05162.txt).
   An access point below the fixed version of its own train is rated **Below fixed version**.
2. **Documented issues.** Crash and reboot bugs that HPE lists as *resolved* in the AOS-10 release notes, per
   access point model and affected version range. An access point whose model and version fall into such a
   range is counted as **in a documented issue range**.

Both lists are plain tables with one row per fact and a link to the HPE source. Nothing is sent to HPE or
anywhere else: the check runs inside your Splunk against the data that the Aruba Central add-on collected.

## 2. What it helps with

- **Security:** which access points still run a version that is affected by an advisory, and which fixed
  version you need per software train.
- **Planning upgrades:** a list of the affected access points with model, site and current version, so that a
  maintenance window can be scoped.
- **Troubleshooting:** if access points reboot or crash, the check shows whether HPE already documents a bug
  for exactly that model and version, with the bug ID and a link to the release note.
- **Reporting:** the **Executive summary** shows the same numbers in its risk list, and every tile opens
  the detail.

It does **not** replace the HPE advisories and release notes. It is an indicator that points you to them
(see section 7).

## 3. How to use it

Open **Risk > Firmware and security** in the app menu.

| Element | Meaning |
| --- | --- |
| **APs at or above the fixed version** (gauge) | Share of rateable access points that run the fixed version of their train or later. |
| **APs below the fixed version** | Number of access points to upgrade because of the advisory. Green at 0. |
| **APs in a documented issue range** | Number of access points affected by at least one documented crash or reboot bug. |
| **APs checked** | Number of access points that reported in the last 30 minutes. Offline access points are not rated. |
| **Firmware versions by model** | Which versions run on which model. |
| **Compliance status** | Share of access points per status (see below). |
| **Access points below the fixed version** | The upgrade list. Click a row to open the access point. |
| **Access points in a documented issue range** | One row per access point and bug. Click a row to open the HPE release note of the bug. |
| **Switch and gateway firmware** | Versions in use. No baseline rows are shipped for them, see section 7. |

The **Site** field above the tiles accepts a site name or a wildcard (`*` for all, `Berlin*` for all
sites starting with Berlin).

The status of an access point is one of:

| Status | Meaning | What to do |
| --- | --- | --- |
| At or above fixed version | The version is the fixed version of its train or newer. | Nothing. |
| Below fixed version | The version is older than the fixed version of its train. | Plan the upgrade to the version in the column **Fixed in**. |
| Not in baseline | There is no row for the software train of this access point. | Check the HPE advisory for this train and add a row (section 5). |
| Unknown version | The version string could not be read. | Check the version in Central. Usually a test or custom build. |

### How a version is rated

Take an access point that reports the version `10.8.0.1_95221`:

1. The build suffix `_95221` is removed. The version is `10.8.0.1`.
2. The train is the first two numbers: `10.8`.
3. The baseline row for the train `10.8` says `min_fixed = 10.8.1.2`.
4. `10.8.0.1` is older than `10.8.1.2`, so the status is **Below fixed version**.

An access point on `10.7.2.5` is compared with the fix of the train `10.7` (`10.7.2.7`), not with `10.8.1.2`.
This is how HPE publishes the fixes: one fixed version per train.

For documented issues the rule is: the model name starts with `model_prefix`, the version is at least
`fw_from` and below `fixed_in`. The bug is listed for the release in which it first appeared as fixed, so
for an older train check the release notes of your own train (the link is in the row).

## 4. Where the data comes from

The check reads the access point inventory that the add-on **TA_hpe_aruba_central** collects from the Aruba
New Central API (field `firmwareVersion` and `model`). It uses the latest value per access point from the last
30 minutes. If a tile shows 0 checked access points, the Wireless input of the add-on does not deliver data:
see **Platform > Data health**.

The reference lists are four tables (in Splunk they are called *lookups*):

| List | Contains | Who maintains it | Survives an app upgrade |
| --- | --- | --- | --- |
| `aruba_firmware_baseline` | Fixed versions of the HPE advisory, one row per train | Shipped with the app | No, replaced by the new app version |
| `aruba_known_issues` | Documented crash and reboot bugs from HPE release notes | Shipped with the app | No, replaced by the new app version |
| `aruba_firmware_baseline_custom` | **Your** fixed versions. A row for a train replaces the shipped row of the same train. | You | Yes |
| `aruba_known_issues_custom` | **Your** additional issue rows | You | Yes |

> **Rule:** put your own rows only into the two `_custom` lists. Edits in the shipped lists are lost at the
> next app upgrade, because the upgrade installs the new version of those files.

## 5. How to maintain the data

### 5.1 Open a list for editing

The easiest editor is the Splunk app **Lookup Editor** (free, from Splunkbase:
[splunkbase.splunk.com/app/1724](https://splunkbase.splunk.com/app/1724)). Ask your Splunk administrator to
install it once. Then these links open the lists in an editor that works like a spreadsheet (add row, edit
cell, delete row, save):

| List | Editor link |
| --- | --- |
| Fixed versions, yours | [Edit aruba_firmware_baseline_custom](https://YOUR-SPLUNK/en-US/app/lookup_editor/lookup_edit?owner=nobody&namespace=aruba_network_insights&lookup=aruba_firmware_baseline_custom&type=kv&transform=aruba_firmware_baseline_custom) |
| Issues, yours | [Edit aruba_known_issues_custom](https://YOUR-SPLUNK/en-US/app/lookup_editor/lookup_edit?owner=nobody&namespace=aruba_network_insights&lookup=aruba_known_issues_custom&type=kv&transform=aruba_known_issues_custom) |
| Fixed versions, shipped (view only) | [Open aruba_firmware_baseline](https://YOUR-SPLUNK/en-US/app/lookup_editor/lookup_edit?owner=nobody&namespace=aruba_network_insights&lookup=aruba_firmware_baseline.csv&type=csv) |
| Issues, shipped (view only) | [Open aruba_known_issues](https://YOUR-SPLUNK/en-US/app/lookup_editor/lookup_edit?owner=nobody&namespace=aruba_network_insights&lookup=aruba_known_issues.csv&type=csv) |

<!-- md-only -->
In this document replace `YOUR-SPLUNK` with the address of your Splunk Web. The links in the app work as they are.
<!-- /md-only -->
You need a role that may write to the app (`admin` or `sc_admin`).

Without Lookup Editor you can still add a row with a search. Open **Search** in the app menu and run:

```
| makeresults
| eval model_prefix="AP-635", fw_from="10.7.2.1", fixed_in="10.8.0.2", bug_id="AOS-268983",
       issue="Random reboot with kernel panic",
       source_url="https://arubanetworking.hpe.com/techdocs/central/aos10rn/aos-10-8-0-x/resolved-issues-in-aos-10-8-0-2.html"
| fields - _time
| outputlookup append=true aruba_known_issues_custom
```

Use `aruba_firmware_baseline_custom` with the columns `scope`, `train`, `min_fixed`, `advisory`, `source_url`,
`note` for a fixed version. Use the same approach to correct a mistake: list the table with
`| inputlookup aruba_known_issues_custom`, remove or change the row and write it back with `| outputlookup`
(without `append`).

### 5.2 The columns

**Fixed versions** (`aruba_firmware_baseline` and `aruba_firmware_baseline_custom`)

| Column | Meaning | Example |
| --- | --- | --- |
| `scope` | What the row applies to. Only `ap` is evaluated today. | `ap` |
| `train` | First two numbers of the software train. | `10.7`, `8.13` |
| `min_fixed` | First version of the train that contains the fix. | `10.7.2.7` |
| `advisory` | Advisory number, shown in the tables. | `HPESBNW05162` |
| `source_url` | Link to the advisory. | `https://csaf.arubanetworking.hpe.com/...` |
| `note` | Free text, for example exceptions. | `FIPS AP-5xx: 8.13.3.2 FIPS` |

One row per train. If the shipped list and your list have a row for the same train, yours wins. Use this when
a newer advisory raises the fixed version of a train before the next app release does.

**Documented issues** (`aruba_known_issues` and `aruba_known_issues_custom`)

| Column | Meaning | Example |
| --- | --- | --- |
| `model_prefix` | Start of the model name. `AP-635` matches one model, `AP-7` the whole AP-7xx family. | `AP-635` |
| `fw_from` | First affected version, included. | `10.7.2.1` |
| `fixed_in` | First version with the fix, **not** included. Leave empty if there is no fix yet. | `10.8.0.2` |
| `bug_id` | HPE bug ID. | `AOS-268983` |
| `issue` | Short description in your words. | `Random reboot with kernel panic` |
| `source_url` | Link to the HPE page. It opens when you click the row in the dashboard. | release note URL |

Versions are written with 2 to 4 numbers separated by dots, without letters and without the build number:
`10.7.2.1`, not `10.7.2.1_95221`.

### 5.3 Check your entries

At the end of the help page in the app, the panel **Check of the lists** shows how many rows each list has and
reports rows with a typing mistake, for example a version with letters or a link without `https://`. After saving a
list, reload the dashboard **Firmware and security**: the change is effective immediately, no restart needed.

The panel **Firmware that cannot be rated yet** lists versions with the status *Not in baseline* or
*Unknown version*. Each entry there is a reason to add a row.

### 5.4 When to update

- **When HPE publishes a security advisory for Aruba / HPE Networking.** Look up the fixed version for each
  train and enter it as a row in `aruba_firmware_baseline_custom`. The advisory names the fixed versions per
  product and train. Advisories are listed in the
  [HPE Security Bulletin Library](https://support.hpe.com/connect/s/securitybulletinlibrary) and published
  in machine-readable form at [csaf.arubanetworking.hpe.com](https://csaf.arubanetworking.hpe.com/) (the file
  `changes.csv` there lists new and updated advisories).
- **When you adopt a new AOS release.** Read its *Resolved Issues* page in the
  [AOS-10 release notes](https://arubanetworking.hpe.com/techdocs/central/aos10rn/index.html). Add a row to
  `aruba_known_issues_custom` for each crash or reboot bug of a model that you run. Skip bugs without a model name
  and bugs that only affect gateways or switches. For AOS-8 Instant see the
  [AOS-8 release notes](https://arubanetworking.hpe.com/techdocs/ArubaOS/oxygen/AOS-8%20Consolidated%20Release%20Notes%20Portal/aos-8-13-x-x/resolved-issues-in-aos-8-13-3-2.html).
- **After an app upgrade.** The shipped lists were replaced by the new version with the newest HPE data. Your
  own lists are unchanged. Remove rows from your lists that duplicate the new shipped rows.
- **Regularly,** for example once a month, open the panel **Firmware that cannot be rated yet**.

## 6. Splunk terms used here

- **Lookup:** a table that Splunk reads when it runs a search. Here: the four lists above. The shipped ones are
  CSV files, your own ones are stored in the **KV Store**, a small database inside Splunk, so that app upgrades
  do not touch them.
- **Search:** the entry **Search** in the app menu opens the search bar. Searches are written in a language
  called SPL. You only need it for the optional examples in section 5.1.
- **Macro:** a named piece of search that the dashboards reuse. The check uses the macros `aruba_fw_key`,
  `aruba_fw_baseline` and `aruba_fw_issues`. You do not need to change them.
- **Dashboard:** a page with tiles and tables. Clicking a tile or a row opens the detail.

## 7. Limits

- **The shipped issue list is a selection, not the complete release notes.** It covers the crash and reboot bugs
  with a model name from the release notes of AOS-10.8.0.2 and AOS-10.8.1.2. Other releases and other bug
  types are not included. Add rows from the release notes of the releases you run. The absence of a row is
  not a statement that an access point is free of problems.
- **One fixed version per issue.** The row names the release in which HPE lists the fix. Maintenance releases of
  older trains (for example 10.7.x) may contain the fix earlier. Open the link of the row and check the release
  notes of your train. If the fix is already in your version, add a row to your own list or ignore the
  entry.
- **Access points only.** The advisory also covers Mobility Gateways managed by Central. Switches and
  gateways are listed under *Switch and gateway firmware* without a rating. You can add rows with
  another `scope`, but the dashboards evaluate only `ap` today.
- **End-of-Maintenance and End-of-Support versions.** The HPE advisory states that software versions that
  reached End of Maintenance are presumed to be affected, even when they are not named in the table. The check
  rates such versions as *Not in baseline* and does not count them as a risk. Treat them as affected.
- **The result depends on the data.** An access point is rated only if it reported in the last 30 minutes. The model
  name must be reported in Central.
- **Exceptions in advisories.** The baseline holds one version per train. An exception (for example FIPS
  AP-5xx on AOS-8.13 need 8.13.3.2 FIPS) is stated in the column `note`.

## 8. Sources

- HPE advisory HPESBNW05162 (fixed versions):
  [csaf.arubanetworking.hpe.com/2026/hpe_networking_-_hpesbnw05162.txt](https://csaf.arubanetworking.hpe.com/2026/hpe_networking_-_hpesbnw05162.txt)
- All Aruba advisories in machine-readable form: [csaf.arubanetworking.hpe.com](https://csaf.arubanetworking.hpe.com/)
- HPE Security Bulletin Library: [support.hpe.com/connect/s/securitybulletinlibrary](https://support.hpe.com/connect/s/securitybulletinlibrary)
- Software downloads of fixed versions: [HPE Networking Support Portal](https://networkingsupport.hpe.com)
- AOS-10 release notes: [arubanetworking.hpe.com/techdocs/central/aos10rn](https://arubanetworking.hpe.com/techdocs/central/aos10rn/index.html),
  for example [Resolved Issues in AOS-10.8.0.2](https://arubanetworking.hpe.com/techdocs/central/aos10rn/aos-10-8-0-x/resolved-issues-in-aos-10-8-0-2.html)
  and [Resolved Issues in AOS-10.8.1.2](https://arubanetworking.hpe.com/techdocs/central/aos10rn/aos-10-8-1-x/resolved-issues-in-aos-10-8-1-2.html)
- AOS-8 release notes (example, referenced by the advisory):
  [Resolved Issues in AOS 8.13.3.2](https://arubanetworking.hpe.com/techdocs/ArubaOS/oxygen/AOS-8%20Consolidated%20Release%20Notes%20Portal/aos-8-13-x-x/resolved-issues-in-aos-8-13-3-2.html)
- Lookup Editor app: [splunkbase.splunk.com/app/1724](https://splunkbase.splunk.com/app/1724)
- Add-on that collects the data: **TA_hpe_aruba_central** (HPE Aruba Central Add-on for Splunk)

<!-- panel:baseline -->
<!-- panel:issues -->
<!-- panel:validation -->
<!-- panel:unrated -->
