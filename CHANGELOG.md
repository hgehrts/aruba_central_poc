# Changelog

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
