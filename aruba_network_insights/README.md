# Aruba Network Insights (`aruba_network_insights`)

Dashboard Studio dashboards for HPE Aruba Networking. They show the data collected by the
[HPE Aruba Central Add-on for Splunk (`TA_hpe_aruba_central`)](https://github.com/hgehrts/TA_hpe_aruba_central)
and, optionally, Aruba device syslog.

**This app contains no data collection.** It only visualises data that `TA_hpe_aruba_central` has
already collected and indexed. Without that add-on and its data the dashboards stay empty.

## Dashboards

Overview and the network map (sites and devices as a graph, green reachable, red unreachable); executive summary; offline devices, alerts, sites and syslog events; AP stability, capacity and load,
access points, one access point, throughput, devices and config sync; firmware and security; data health and
configuration. Tiles, rows and chart elements drill down between the views, set filters, or open the raw events
in Search. The dashboards use the full browser width. The full list with the question each page answers is in
the repository README. The views use Splunk's dark theme. Studio keeps the theme stored in the
view and does not switch it with the user preference. Search and the app chrome follow the user because
the app declares light and dark.

## Firmware check

**Risk > Firmware and security** rates the access point firmware against fixed versions from an HPE advisory and
against documented crash and reboot bugs from HPE release notes. **Risk > Firmware check help** explains it for
readers who know Aruba but not Splunk: what it does, how to read it, how to maintain its lists, limits and
sources. The shipped lists (`aruba_firmware_baseline`, `aruba_known_issues`) are replaced by every app
upgrade. Enter your own rows in `aruba_firmware_baseline_custom` and `aruba_known_issues_custom` (KV Store,
kept across upgrades), preferably with the Lookup Editor app from Splunkbase.

## Requirements

- Splunk Enterprise or Splunk Cloud with Dashboard Studio.
- `TA_hpe_aruba_central` (tested with 1.3.0), configured with at least one account and the inputs you want to
  see, running on a forwarder or on a heavy forwarder in the same environment. The app must be installed
  on the search head.

## Index settings

Searches on Aruba Central data use the search macro `aruba_central_index` (default `index=main`). Searches on
Aruba syslog use `aruba_syslog`, built on the index macro `aruba_syslog_index` (default `index=netops`). Open
**Configuration** in the app menu to find the indexes and to save the macros without a restart. The page also
shows a source check for the saved values: a traffic light, the last event and an hourly sparkline per source.

You can also set the macros by hand, for example in `local/macros.conf`:

```
[aruba_central_index]
definition = index=aruba

[aruba_syslog_index]
definition = index=netops
```

Aruba syslog is optional. It is typically received by Splunk Connect for Syslog (sourcetype `aruba:syslog`)
and parsed by `TA-aruba_networks`. Without it the syslog panels stay empty.

For more than one index use `definition = (index=aruba OR index=network)`.

## Sourcetypes used

`aruba:central:ap`, `aruba:central:swarm`, `aruba:central:ap_throughput`, `aruba:central:device`,
`aruba:central:device_inventory`, `aruba:central:site_health`, `aruba:central:alert`. Optional:
Aruba syslog (`aruba:syslog`, `aruba`, `aruba:<process>`).
