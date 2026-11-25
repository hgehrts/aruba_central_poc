# Changelog

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
