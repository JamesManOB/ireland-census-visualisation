# Data, provenance and reproducibility

## Sources recorded in the original report

- **Central Statistics Office, Census 2022, table F5020**: population aged one year and over, usually resident and present in the State, who were living outside the State one year ago. The report names this source for immigration counts.
- **CSO Census of Population 2022 Profile 5, Citizenship**: contextual interpretation of citizenship and immigration. The report's source URL is <https://www.cso.ie/en/releasesandpublications/ep/p-cpp5/censusofpopulation2022profile5diversitymigrationethnicityirishtravellersreligion/citizenship>.
- The full references and rationale are preserved in [design-report.pdf](design-report.pdf).

The repository packages the supplied final project. It does not independently re-download or revalidate the underlying CSO tables.

## Included tables

The CSVs in `data/` are newly exported from the embedded values in `specs/dashboard.vl.json`. They are not the original raw CSO downloads or recovered original processed CSVs. Values, category strings and stored proportions are preserved.

| File | Rows | Grain | Fields |
| --- | ---: | --- | --- |
| `recent_immigrants_by_citizenship.csv` | 10 | Citizenship | `citizenship`, `count`, `rank` |
| `recent_immigrants_age_by_citizenship.csv` | 100 | Citizenship × age band | `citizenship`, `age_group`, `count`, `pct_within_citizenship` |
| `recent_immigrants_housing_tenure.csv` | 60 | Citizenship × tenure | `citizenship`, `occupancy_type`, `count`, `pct_within_citizenship` |
| `recent_immigrants_rent_by_citizenship.csv` | 10 | Citizenship × recorded landlord type | `citizenship`, `landlord_type`, `avg_weekly_rent` |

`pct_within_citizenship` is stored as a fraction between 0 and 1 and displayed as a percentage. The exported age and tenure fractions each sum to approximately 1 within each citizenship group. Counts refer to their own table populations; they must not automatically be treated as a common denominator across panels.

Rent is expressed in euros per week. The embedded rent rows all use `Rented from private landlord` as the landlord type. The reference line is separately hard-coded as `national_avg: 273` and is not calculated from these ten rows.

## Important interpretation limits

- **Population coverage:** exact source table identifiers and denominators for housing tenure and rent are not recorded in the supplied files. Their comparability with F5020 cannot be established from the dashboard alone.
- **Reference line:** the original design calls €273 a national average, but its exact source, tenure coverage and comparability with the plotted rent values need verification.
- **Citizenship:** this is not birthplace, ethnicity or a direct measure of immigration status. The Irish citizenship category should not automatically be described as Irish-born returnees.
- **Selected categories:** only the ten displayed citizenship categories are included. Broad groups such as Other Asia are aggregates.
- **Descriptive measures:** differences do not establish causal effects. Mean rent does not show the distribution, housing quality, household size or geographical mix.
- **Presentation:** the original fixed panel sizes suit desktop viewing; narrow screens may require horizontal scrolling. Axes may rescale when filtering.
- **Category strings:** `Other EU27 ` includes a trailing space in the original data and dropdown. It is deliberately preserved so exact-match filtering continues to work.

## Original and maintained versions

The original HTML and final JSON contain equivalent specifications. `index.html` embeds that final specification, with HTML language, encoding, viewport and title metadata, basic spacing and a correctly closed visualisation container added. Chart data and interaction logic are preserved.

The earlier CSV prototype uses click selection rather than the final dropdown and references four CSV filenames relative to its own location. It is retained as a historical source, not the default entry point. To experiment with it, copy the four exports from `data/` beside it or update its URLs. Those exports come from the final version; they are not proof of the prototype's original inputs.

The provided source folder also contains a walkthrough video. It is not bundled here; the repository includes the HTML, both specifications and the design report.

## Rebuild scope

Run `python scripts/build.py` from any working directory using its full path if necessary. The script reads the final specification, exports the embedded tables and rebuilds the runnable HTML. It does not fetch data, repeat the original cleaning process or update the fixed rent benchmark.
