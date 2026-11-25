# Aruba Central POC Dashboards (`aruba_central_poc`)

Dashboard Studio dashboards for the data collected by the
[HPE Aruba Central Add-on for Splunk (`TA_hpe_aruba_central`)](https://github.com/hgehrts/TA_hpe_aruba_central).

**This app contains no data collection.** It only visualises data that `TA_hpe_aruba_central` has
already collected and indexed. Without that add-on and its data the dashboards stay empty.

## Dashboards

Overview and executive summary; offline devices, alerts and sites; AP stability, capacity and load, access points,
one access point, throughput, devices and config sync; firmware and security; data health and configuration.
Rows and single values drill down between the views. The full list with the question each page answers is in
the repository README. The views use Splunk's dark theme. Studio keeps the theme stored in the
view and does not switch it with the user preference. Search and the app chrome follow the user because
the app declares light and dark.

## Requirements

- Splunk Enterprise or Splunk Cloud with Dashboard Studio.
- `TA_hpe_aruba_central` (tested with 1.3.0), configured with at least one account and the inputs you want to
  see, running on a forwarder or on a heavy forwarder in the same environment. The app must be installed
  on the search head.

## Index setting

All searches use the search macro `aruba_central_index`. The default is `index=main`. Open
**Configuration** in the app menu to find the index with the Aruba Central data and to save the macro
without a restart. The page also shows the events per sourcetype for the saved value.

You can also set the macro by hand, for example in `local/macros.conf`:

```
[aruba_central_index]
definition = index=aruba
```

For more than one index use `definition = (index=aruba OR index=network)`.

## Sourcetypes used

`aruba:central:ap`, `aruba:central:swarm`, `aruba:central:ap_throughput`, `aruba:central:device`,
`aruba:central:device_inventory`, `aruba:central:site_health`, `aruba:central:alert`.
