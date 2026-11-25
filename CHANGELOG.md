# Changelog

## 1.4.2

- The author in `app.conf` is Hans-Henning Gehrts (was Splunk Services (Cisco)). No other change.

## 1.4.1

First release under the name Aruba Network Insights. Version 1.4.0 was never published; 1.4.1 contains everything listed
below. The package and the repository history were checked for customer data (host names, site names, IP addresses,
serial numbers, tokens). There is none.

- New page **Network map** below Overview: sites, device types and devices as a Studio network graph with green,
  amber and red status, icons per device type, tooltips and drilldown into the other dashboards. Shows membership,
  not cabling (the data contains no neighbor information).
- **Configuration** has a source check: one row per Aruba Central sourcetype and one for syslog with a traffic light,
  last event, age and an hourly sparkline. It refreshes when the macros are saved.
- Data health shows how many access point readings have CPU or memory outside 0 to 100 %.
- Fixes: the Overview and Sites tables call the site health values "Poor %", "Fair %" and "Good %" (they are percentages
  of the site, not counts), the client histogram on Capacity labels its buckets "0 to 9" instead of "0-9" (which
  was drawn as 0.9), and the model chart on Access points uses whole numbers on its axis.
- Syslog page: the description says that Aruba syslog is optional and points to the source check.

- **Renamed** to **Aruba Network Insights** (app ID `aruba_network_insights`, was `aruba_central_poc`). The
  data now comes from Aruba Central and, optionally, from device syslog, and it is no longer a proof of
  concept. A new app ID is a new app: install it, remove `aruba_central_poc`, and set the index macros on the
  Configuration page again. Macros, lookups and sourcetypes keep their names.
- Documented issues: 18 more rows for 15 more crash and reboot bugs with a model name from the AOS-10.8.0.2 and AOS-10.8.1.2
  release notes (27 rows in total). Checked against the release notes. The list stays a selection.
- Fixed versions: the 8.13 row notes the FIPS exception of advisory HPESBNW05162 revision 2 (AP-5xx in FIPS
  environments need 8.13.3.2 FIPS).
- Your own rows: new KV Store lookups `aruba_firmware_baseline_custom` and `aruba_known_issues_custom`. An app
  upgrade replaces the shipped CSV files, the custom lookups stay. A custom row for a train replaces the
  shipped fixed version. The macros `aruba_fw_baseline` and `aruba_fw_issues` read both.
- New page **Risk > Firmware check help**: what the check does, how to use it, how to maintain the data, limits
  and sources, with live views of the lists, a check for typing mistakes and a list of firmware versions that
  cannot be rated. The text is `docs/firmware-check.md` (generated into the view by `scripts/build_help.py`).
- The Firmware and security page links to the help and to the Lookup Editor for both custom lists.

## 1.3.0

- All dashboards use the full browser width (Studio grid layout).
- Visual rework: gauges and colored tiles with thresholds, section headers on the executive summary, colored
  severity, status and threshold cells in tables, fixed series colors (severity, online and offline), and a
  dropdown to pick the access point.
- More drilldowns: tiles and rows open the related dashboard, chart clicks set filters on the same page
  (severity, alert type, config status, device type, process), and rows open the raw events in Search in a
  new tab. Documented firmware issues open the HPE release note.
- Optional Aruba syslog: new macros `aruba_syslog_index` (default `index=netops`), `aruba_syslog` and
  `aruba_syslog_fields`; the Configuration page sets the syslog index too.
- New **Syslog events** dashboard (Operations): severity, processes, devices with their Central site, event
  IDs, authentication failures, client disconnect reasons, rogue and interfering access points.
- Syslog panels on Overview, Executive summary (security signals), Offline devices (offline in Central but
  still sending syslog), AP stability (crash and watchdog messages), Capacity and load (disconnect reasons,
  resource constrained), Config sync (local changes and admin logins), Access point (its syslog) and Data
  health (syslog freshness and volume).

## 1.2.0

- New menu structure: Management, Operations, Troubleshooting, Risk and Platform.
- New dashboards: Executive summary, Offline devices, AP stability, Capacity and load, Config sync,
  Firmware and security, Data health.
- Alerts and Sites are extended. Alerts shows open alerts, age, time to clear, a noise ranking and the
  root cause and recommended action of a selected alert. Sites ranks sites by poor health and shows a trend.
- Two editable lookups: `aruba_firmware_baseline` (fixed versions from HPE advisory HPESBNW05162) and
  `aruba_known_issues` (documented issue ranges from the AOS-10.8.0.2 and AOS-10.8.1.2 release notes).
- New macros for firmware comparison and ISO timestamps. See the README.

## 1.1.0

- New **Configuration** page in the app menu. It lists the indexes that contain `aruba:central:*` data,
  saves the macro `aruba_central_index` without a restart and shows the events per sourcetype for the
  saved value. The app declares it as its `setup_view`.

## 1.0.0

First standalone release. The dashboards come from the companion app that shipped with
`TA_hpe_aruba_central` up to 1.3.0.

- Seven Dashboard Studio dashboards: overview, access points, one access point, throughput, devices, sites
  and alerts, with drilldowns between them.
- All searches use the macro `aruba_central_index` (default `index=main`).
- App icon is the divi-divi tree (*Libidibia coriaria*).
- Apache-2.0 license.
- Requires the data collected by `TA_hpe_aruba_central` (tested with 1.3.0).
