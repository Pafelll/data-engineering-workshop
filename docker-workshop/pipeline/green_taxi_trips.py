import os
import click
import pandas as pd
from sqlalchemy import create_engine, Engine
from tqdm.auto import tqdm
import logging
from typing import Iterable
import pyarrow.parquet as pq


logger = logging.getLogger()


zone_dtype = {
    "LocationID": "Int64",
    "Borough": "string",
    "Zone": "string",
    "service_zone": "string",
}


def load_into_db(df_iter: Iterable, target_table: str, engine: Engine) -> None:
    first = True

    for df_chunk in tqdm(df_iter):
        if first:
            df_chunk.head(0).to_sql(
                name=target_table,
                con=engine,
                if_exists='replace'
            )
            first = False

        df_chunk.to_sql(
            name=target_table,
            con=engine,
            if_exists='append'
        )
    logger.info(f"Loading data into {target_table} finished.")

def parquet_batches(file_path: str, chunksize:int = 100000):
    parquet_file = pq.ParquetFile(file_path)
    for batch in parquet_file.iter_batches(batch_size=chunksize):
        yield batch.to_pandas()


@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL user')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5432, type=int, help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--chunksize', default=100000, type=int, help='Chunk size for reading CSV')
@click.option('--data-dir', type=click.Path(exists=True, file_okay=False, dir_okay=True), default='.', help='Local folder with taxi data files')
def run(pg_user, pg_pass, pg_host, pg_port, pg_db, chunksize, data_dir):
    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')

    # load taxi zones
    zone_url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv'
    zone_df_iter = pd.read_csv(
        zone_url,
        dtype=zone_dtype,
        iterator=True,
        chunksize=chunksize,
    )
    load_into_db(zone_df_iter, "taxi_zone", engine)

    # load green taxi trips
    file_name = f'green_tripdata_2025-11.parquet'
    green_taxi_path = os.path.join(data_dir, file_name)
    green_taxi_df_iter = parquet_batches(green_taxi_path)
    load_into_db(green_taxi_df_iter, "green_taxi_trips", engine)


if __name__ == '__main__':
    run()