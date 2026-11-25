# Aruba Network Insights

<img src="aruba_network_insights/static/appIcon_2x.png" alt="App icon" width="72">

Splunk search-head app (`aruba_network_insights`) with Dashboard Studio dashboards for HPE Aruba Networking.
It combines the New Central (GreenLake) data from `TA_hpe_aruba_central` with optional Aruba device syslog:
management summary, operations, troubleshooting and risk views.

> **Requires the data from [`TA_hpe_aruba_central`](https://github.com/hgehrts/TA_hpe_aruba_central).**
> This app does not collect anything. Install and configure that add-on first, let its inputs run, then
> point this app to the index that holds the data (see below).

| | |
| --- | --- |
| App ID | `aruba_network_insights` |
| Version | 1.4.1 |
| Data source | `TA_hpe_aruba_central` (tested with 1.3.0); optional Aruba syslog (SC4S, `TA-aruba_networks`) |
| Install on | Search head |
| License | Apache-2.0 |

## Menu and dashboards

The menu follows the people who use it.

| Menu | Dashboard | Question it answers |
| --- | --- | --- |
| | Overview | What is the state right now? Access points, switches and gateways, throughput, alerts, sites, syslog |
| | Network map | Sites, device types and devices as a graph: green reachable, amber partly reachable, red unreachable, with icons per device type and a drilldown into the other dashboards |
| Management | Executive summary | Availability, open critical alerts, firmware compliance, reboots, config state, security signals from syslog and the top risks, with drilldown |
| Operations | Offline devices | Which devices are offline, for how long, did many go offline together, and do they still send syslog? |
| Operations | Alerts | Open alerts, age, time to clear, noisy alert types, root cause and recommended action |
| Operations | Sites | Worst sites first, health trend, all sites |
| Operations | Syslog events | Aruba syslog by severity, process and device, event IDs, authentication failures, client disconnects, rogue and interfering access points |
| Troubleshooting | AP stability | Reboots derived from uptime, reboot reasons, crash and watchdog messages from syslog, reboot rate by model and firmware |
| Troubleshooting | Capacity and load | Clients, CPU, memory and PoE draw per access point and site, memory rising without a reboot, client disconnect reasons from syslog |
| Troubleshooting | Access points, Access point | Fleet table, and one access point with firmware check, reboots and its syslog |
| Troubleshooting | Throughput | Total throughput by interface, top 10 access points |
| Troubleshooting | Devices | Monitored devices by type, device inventory |
| Troubleshooting | Config sync | Devices whose configuration is not synchronized, local changes and admin logins from syslog |
| Risk | Firmware and security | Access points below the fixed version of a security advisory, or in a documented release-note issue range |
| Risk | Firmware check help | What the firmware check does, how to read it and how to maintain its lists, with live views of the lists and a check for typing mistakes |
| Platform | Data health | Is data arriving? Freshness, volume, input runs, add-on warnings and errors, readings outside 0 to 100 % |
| Platform | Configuration | Find the indexes, set the index macros, and check per source whether data arrives (traffic light, last event, hourly trend) |

The dashboards use the full browser width (Studio grid layout) and the dark theme. Studio keeps the theme in
the view, so it does not follow the user preference. Search and the app chrome do.

Most tiles, rows and chart elements are links. They open the related dashboard, set a filter on the same page,
or open the raw events in Search in a new tab (for example the Central events and syslog of an offline device,
the syslog of one event ID, or the HPE release note of a documented issue). The panel titles say what a click does.

## Install

1. Install and configure `TA_hpe_aruba_central` and make sure data arrives.
2. Install the package `aruba_network_insights-<version>.tar.gz` from the
   [releases](https://github.com/hgehrts/aruba_network_insights/releases) on the search head
   (**Apps > Manage Apps > Install app from file**).
3. Open **Configuration** in the app menu and set the index macros.

Upgrading from `aruba_central_poc` (releases 1.0.0 to 1.2.0)? This app was renamed in 1.4.1. A new app ID is a
new app: install `aruba_network_insights`, remove `aruba_central_poc`, and set the index macros on the
Configuration page again. The old app held no data that has to be moved.

## Network map

The **Network map** page (menu entry below Overview) draws the sites and devices of Aruba Central as a graph
(Dashboard Studio visualization `splunk.networkGraph`, verified on Splunk 10.6; the page needs a Splunk version that has
this visualization). Node colors: green when everything below is reachable, amber when only some devices are, red when
none are. Reachable means that Central reports the status `ONLINE`. Icons show the device type: Wi-Fi symbol for access points,
switch symbol for switches, router symbol for gateways, building for sites and cloud for Aruba Central. A click opens
the access point page, the access points or devices page filtered by site and type, or the overview of the site. The
tooltip shows status, type, model, IP address, firmware and site.

The lines show membership (Central, site, device type, device) and **not** physical cabling: the Aruba Central data that
the add-on collects contains no uplink or LLDP neighbor information. The inputs are the site wildcard, whether to show only
sites with unreachable devices, the detail level (device types or every device) and the direction of the tree.

## Index macros and Configuration page

Searches on Aruba Central data use the macro `aruba_central_index` (default `index=main`). Searches on Aruba
syslog use `aruba_syslog`, which is the index macro `aruba_syslog_index` (default `index=netops`, the SC4S
default for Aruba) plus a sourcetype filter.

The **Configuration** page in the app menu helps to set both. It lists the indexes that contain the
`aruba:central:*` sourcetypes and the Aruba syslog sourcetypes of the last 24 hours, saves the macros without
a restart and shows a source check for the saved values: one row per Aruba Central sourcetype and one for syslog with a traffic light (green fresh, amber delayed, red no data, grey optional), the last event, its age and a sparkline of the events per hour over 24 hours. The macros are stored in
`local/macros.conf` of the app. Users who can write to the app (`admin`, `sc_admin`) can use the page.

You can also set them by hand in `local/macros.conf` or under **Settings > Advanced search > Search macros**:

```
[aruba_central_index]
definition = index=aruba

[aruba_syslog_index]
definition = index=netops
```

For several indexes use `definition = (index=aruba OR index=network)`.

## Aruba syslog (optional)

Syslog is a second, independent source next to the API data. The app adds syslog panels to the overview,
executive summary, offline devices, AP stability, capacity, config sync, access point and data health pages,
and a **Syslog events** page. Without syslog these panels stay empty; everything else works as before.

- **Collection:** send syslog from gateways, controllers and access points to Splunk Connect for Syslog (SC4S).
  SC4S tags Aruba messages as sourcetype `aruba:syslog` (index `netops` by default).
- **Parsing:** the Splunkbase add-on `TA-aruba_networks` renames `aruba:syslog` to one sourcetype per process
  (`aruba:authmgr`, `aruba:stm`, `aruba:wms`, `aruba:sapd`, ...), adds CIM fields and event types, and shows
  events it could not rename as sourcetype `aruba`. The macro `aruba_syslog` covers `aruba` and `aruba:*`
  and excludes `aruba:central:*`.
- **Fields used by the dashboards** come from the macro `aruba_syslog_fields`, which extracts them from the raw
  event. The panels therefore also work on a search head without `TA-aruba_networks`. The event description
  column on the Syslog events page needs that add-on (lookup `aruba_events`).
- **Matching with Central:** syslog devices are matched with New Central by device name or IP address. An
  offline device that still sends syslog is up and has lost its path to Central (uplink, DNS, proxy, firewall).
- The extractions follow the AOS 8 / AOS 10 message format (`process[pid]: <event id> <level> ...`). Check them
  with your own data; message texts differ between releases.

## Firmware check and its lists

The **Firmware and security** page compares the version of every access point with fixed versions from an HPE
advisory and with documented crash and reboot bugs from the HPE release notes. The full customer documentation
(what it does, how to read it, how to maintain the data, limits and sources) is in
[docs/firmware-check.md](docs/firmware-check.md). It is also in the app under **Risk > Firmware check help**.

Four lookups hold the reference data. Each row has a source link.

| Lookup | Content | Columns | Upgrade |
| --- | --- | --- | --- |
| `aruba_firmware_baseline` (CSV) | Lowest fixed version per release train, from HPE advisory HPESBNW05162 (AOS-10 and AOS-8 access points). | `scope`, `train`, `min_fixed`, `advisory`, `source_url`, `note` | Replaced by the new app version |
| `aruba_known_issues` (CSV) | Crash and reboot bugs with a model name, resolved in the AOS-10.8.0.2 and AOS-10.8.1.2 release notes: model prefix, affected versions, fix release. A selection, not the complete release notes. | `model_prefix`, `fw_from`, `fixed_in`, `bug_id`, `issue`, `source_url` | Replaced by the new app version |
| `aruba_firmware_baseline_custom` (KV Store) | Your fixed versions. A row for a train replaces the shipped row of the same train. | as the baseline | Kept |
| `aruba_known_issues_custom` (KV Store) | Your additional issues. | as the known issues | Kept |

An app upgrade replaces the shipped CSV files, so put your own rows only into the two `_custom` lookups. Edit
them with the [Lookup Editor](https://splunkbase.splunk.com/app/1724) app (the dashboard and the help page link
to the editor) or with `| outputlookup append=true aruba_known_issues_custom` in Search. `train` is the first
two parts of the version (`10.8`). `scope` is `ap`; switch and gateway versions are listed on the page but have
no baseline rows. A release note that lists a fix for one release train does not say that the same fix reached
every other train, so treat a hit as a reason to read the release note.

## Macros

| Macro | Use |
| --- | --- |
| `aruba_central_index` | Index of the Aruba Central data. |
| `aruba_syslog_index` | Index of the Aruba syslog. |
| `aruba_syslog` | Aruba syslog events: `aruba_syslog_index` plus the sourcetype filter. |
| `aruba_syslog_fields` | Adds `aruba_process`, `aruba_event_id`, `aruba_level`, `aruba_severity`, `aruba_device`, `aruba_device_ip`, `aruba_ap` and `aruba_message`. |
| `aruba_ver_key(1)` | Turns a version such as `10.8.1.2` into a sortable number. |
| `aruba_fw_key` | Adds `fw_norm`, `fw_train` and `fw_key` from `firmwareVersion`. |
| `aruba_fw_baseline` | Compares with the baseline lookups (your `_custom` rows first) and adds `fw_status`. |
| `aruba_fw_issues` | Keeps access points inside a documented issue range (shipped and `_custom` lookup). |
| `aruba_iso_epoch(1)` | Converts an ISO 8601 UTC timestamp to epoch seconds. |

## Notes on the indicators

- Reboots are derived from uptime (a drop of more than one minute between two polls while online). They depend
  on the poll interval of the Wireless input.
- Device availability is the share of polls in which a device was online. It is not an SLA figure.
- Switches and gateways come from the Inventory input (hourly by default), so their status can be up to an
  hour old.
- Alerts are written when they change. An open alert that did not change in the time range is not listed.
- The *Data health* page reads `index=_internal`. Users need access to that index for its log panels.

## Build

```
scripts/package.sh
```

creates `dist/aruba_network_insights-<version>.tar.gz` and its SHA-256 file. The help page
`default/data/ui/views/firmware_help.xml` is generated from `docs/firmware-check.md`; run
`python3 scripts/build_help.py` after you change that file. AppInspect:

```
pip install splunk-appinspect
splunk-appinspect inspect dist/aruba_network_insights-<version>.tar.gz --mode precert
```

## License

Apache License 2.0. See [LICENSE](LICENSE).
