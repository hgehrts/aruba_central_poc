# Aruba Central POC Dashboards

<img src="aruba_central_poc/static/appIcon_2x.png" alt="App icon" width="72">

Splunk search-head app (`aruba_central_poc`) with Dashboard Studio dashboards for HPE Aruba Networking
New Central (GreenLake) data.

> **Requires the data from [`TA_hpe_aruba_central`](https://github.com/hgehrts/TA_hpe_aruba_central).**
> This app does not collect anything. Install and configure that add-on first, let its inputs run, then
> point this app to the index that holds the data (see below).

| | |
| --- | --- |
| App ID | `aruba_central_poc` |
| Version | 1.2.0 |
| Data source | `TA_hpe_aruba_central` (tested with 1.3.0) |
| Install on | Search head |
| License | Apache-2.0 |

## Menu and dashboards

The menu follows the people who use it.

| Menu | Dashboard | Question it answers |
| --- | --- | --- |
| | Overview | What is the state right now? |
| Management | Executive summary | Availability, open critical alerts, firmware compliance, reboots, config state, and the top risks, with drilldown |
| Operations | Offline devices | Which devices are offline, for how long, and did many go offline together? |
| Operations | Alerts | Open alerts, age, time to clear, noisy alert types, root cause and recommended action |
| Operations | Sites | Worst sites first, health trend, all sites |
| Troubleshooting | AP stability | Reboots derived from uptime, reboot reasons, reboot rate by model and firmware |
| Troubleshooting | Capacity and load | Clients, CPU, memory and PoE draw per access point and site, memory rising without a reboot |
| Troubleshooting | Access points, Access point | Fleet table and one access point |
| Troubleshooting | Throughput | Total throughput by interface, top 10 access points |
| Troubleshooting | Devices | Monitored devices by type, device inventory |
| Troubleshooting | Config sync | Devices whose configuration is not synchronized |
| Risk | Firmware and security | Access points below the fixed version of a security advisory, or in a documented release-note issue range |
| Platform | Data health | Is data arriving? Freshness, volume, input runs, add-on warnings and errors |
| Platform | Configuration | Find the index and set the index macro |

The dashboards use the dark theme. Studio keeps the theme in the view, so it does not follow the user
preference. Search and the app chrome do.

## Install

1. Install and configure `TA_hpe_aruba_central` and make sure data arrives.
2. Install the package `aruba_central_poc-<version>.tar.gz` from the
   [releases](https://github.com/hgehrts/aruba_central_poc/releases) on the search head
   (**Apps > Manage Apps > Install app from file**).
3. Open **Configuration** in the app menu and set the index macro.

## Index macro and Configuration page

Every search uses the macro `aruba_central_index`. The default is `index=main`.

The **Configuration** page in the app menu helps to set it. It lists the indexes that contain the
`aruba:central:*` sourcetypes of the last 24 hours, saves the macro without a restart and shows the events
per sourcetype for the saved value. The macro is stored in `local/macros.conf` of the app. Users who can
write to the app (`admin`, `sc_admin`) can use the page.

You can also set it by hand in `local/macros.conf` or under **Settings > Advanced search > Search macros**:

```
[aruba_central_index]
definition = index=aruba
```

For several indexes use `definition = (index=aruba OR index=network)`.

## Lookups you can edit

Two CSV lookups drive the **Firmware and security** page and the firmware figures on the executive summary.
Each row has a source link.

| Lookup | Content | Columns |
| --- | --- | --- |
| `aruba_firmware_baseline.csv` | Lowest fixed version per release train. Seeded from HPE advisory HPESBNW05162 (AOS-10 and AOS-8 access points). | `scope`, `train`, `min_fixed`, `advisory`, `source_url`, `note` |
| `aruba_known_issues.csv` | Model and version ranges with a documented release-note issue, and the release that fixed it. Seeded from the AOS-10.8.0.2 and AOS-10.8.1.2 release notes. | `model_prefix`, `fw_from`, `fixed_in`, `bug_id`, `issue`, `source_url` |

Both files are examples. HPE publishes new advisories and release notes all the time. Review the rows, then add,
change or remove them in your environment, for example with the Lookup Editor app. `train` is the first two
parts of the version (`10.8`). `scope` is `ap`. Switch and gateway versions are listed on the page but have no
baseline rows. A release note that lists a fix for one release train does not say that the same fix reached
every other train, so treat a hit as a reason to read the release note.

## Macros

| Macro | Use |
| --- | --- |
| `aruba_central_index` | Index of the Aruba Central data. |
| `aruba_ver_key(1)` | Turns a version such as `10.8.1.2` into a sortable number. |
| `aruba_fw_key` | Adds `fw_norm`, `fw_train` and `fw_key` from `firmwareVersion`. |
| `aruba_fw_baseline` | Compares with the baseline lookup and adds `fw_status`. |
| `aruba_fw_issues` | Keeps access points inside a documented issue range. |
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

creates `dist/aruba_central_poc-<version>.tar.gz` and its SHA-256 file. AppInspect:

```
pip install splunk-appinspect
splunk-appinspect inspect dist/aruba_central_poc-<version>.tar.gz --mode precert
```

## License

Apache License 2.0. See [LICENSE](LICENSE).
