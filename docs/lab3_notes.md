# Lab 3 Notes

This pipeline uses ETL: both raw sources are ingested, validated and cleaned, then joined before the merged dataset is stored as Parquet. Transforming before storage keeps invalid prices, dates and rainfall values out of the processed artifact and makes the final data easier to consume.

The pipeline is idempotent through overwrite-on-load. Each run replaces `data/processed/prices_with_rainfall.parquet`, so rerunning the same inputs cannot duplicate output rows.

Missing markets are imputed as `Unknown`; invalid prices, invalid dates, duplicate rows and duplicate IDs are rejected from the cleaned price data. A missing raw source file fails fast with an informative `FileNotFoundError`.
