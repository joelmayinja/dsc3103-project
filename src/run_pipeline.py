from src.common.logging_setup import get_logger
from src.ingest.source_a import ingest_source_a
from src.ingest.source_b import ingest_source_b
from src.transform.clean import clean_data
from src.transform.merge import merge_data


PATH = "data/processed/merged_prices_with_rain.parquet"
logger = get_logger()


def run_pipe():
    logger.info("=== Pipeline run started ===")

    logger.info("Stage 1: ingesting source A")
    source_a = ingest_source_a()
    logger.info("Source A ingested rows=%d", len(source_a))

    logger.info("Stage 2: ingesting source B")
    source_b = ingest_source_b()
    logger.info("Source B ingested rows=%d", len(source_b))

    logger.info("Stage 3: cleaning data")
    clean_prices, decisions = clean_data()
    logger.info(
        "Source A cleaned rows_in=%d rows_out=%d decisions=%d",
        len(source_a),
        len(clean_prices),
        len(decisions),
    )

    logger.info("Stage 4: merging prices and rainfall")
    merged = merge_data(clean_prices, source_b)
    logger.info("Merge complete rows=%d", len(merged))

    logger.info("Stage 5:Saving the merged file")
    merged.to_parquet(PATH,index=False)
    logger.info(f"Stagge 55: Saving complete:saved{len(merged)}rows")
    logger.info("=== Pipeline run completed===")

    return merged


if __name__ == "__main__":
    run_pipe()
