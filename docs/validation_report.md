# Validation report

| Rule | Failing rows before cleaning | Action taken |
| --- | ---: | --- |
| Positive price | 46 | Rejected non-positive prices |
| Duplicate record_id | 31 | Dropped duplicate IDs, keeping first |
| Duplicate rows | 10 | Dropped exact duplicate rows |
| Valid date | 26 | Removed invalid/future dates |
| Missing market | 181 | Imputed 'Unknown' |
| Known commodity | 0 | Normalized commodity text |

## Cleaning decisions

- Reject: 10 exact duplicate rows (duplicate row rule).
- Reject: 21 rows with duplicate record_id values.
- Reject: 43 rows with non-positive prices.
- Reject: 18 rows with invalid or future dates.
- Impute: 163 missing market values set to 'Unknown'.
- Raw file preserved: True (sha256=80663705a6e97f1f1fb10c6fab1c15a98fea154689d5560f8a07e9b30591f011).
