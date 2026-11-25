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
| Version | 1.1.0 |
| Data source | `TA_hpe_aruba_central` (tested with 1.3.0) |
| Install on | Search head |
| License | Apache-2.0 |

## Dashboards

| Dashboard | Content |
| --- | --- |
| Overview | APs online and not online, wireless sessions, max CPU and memory, wireless throughput, latest alerts, sites |
| Access points | Access points by status, with drilldown to one access point |
| Access point | One access point: latest state, CPU, memory and sessions, throughput by interface |
| Throughput | Total throughput by interface, top 10 access points |
| Devices | Monitored devices by type, device inventory |
| Sites | Site health |
| Alerts | Alerts by severity, alert list |
| Configuration | Index discovery and the `aruba_central_index` macro |

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
