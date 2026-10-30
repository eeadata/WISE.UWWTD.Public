# Decisions

Settled by the project owner on 2026-10-30.

- **D-01.** Provisional 2024 reported data and compliance results may be published in this repository once the owner approves the push.
- **D-02.** `FLAContact.csv` from the 2024 Article 17 Reportnet file is left out because it holds personal data. The repacked zip therefore differs from the original file (SHA-256 `0a0c21278a8cb9e7e21d6c613b37f6c9908ec1096124784fb6f96bfbf37b1b93`); the three tables it keeps are byte-identical to the original.
- **D-03.** 2024 reported data comes from the Reportnet 3 export of 29 October 2026 (`EU Dataset - Art15` and `Art17 - Descriptive data.zip`).
- **D-04.** Compliance results for 2022 and 2024 are `final_Agglomeration` and `final_Plant` from the water lake release `uwwtd_released-and-db_2026-10-30`, filtered to DatasetId 20 (2022) and 39 (2024). The Reportnet export holds no compliance results.
- **D-05.** All data is published as zips of CSV files, for simple loading. In the compliance CSVs an empty cell is a missing value and `""` is an empty text value.
- **D-06.** The earlier five-year compliance files, `Compliance/legal` and the older zips in `other/` are removed. Git history keeps them.
- **D-07.** `Compliance/` is renamed `data/`, and the zip named `UWWTD_Reported_ref2024_Final.zip` is filed as reference year 2022, which is what it holds.
