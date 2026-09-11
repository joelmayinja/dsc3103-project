

#%%
import requests
import pandas as pd
# %%
from src.common.config import (
    SOURCE_B_RAW_PATH,
    MARKET_COORDS,
    RAINFALL_START_DATE,
    RAINFALL_END_DATE,
    RAINFALL_URL
)  

def get_market_rainfall(market_name,latitude,longitude,start_date =RAINFALL_START_DATE,end_date =RAINFALL_END_DATE):

    params = {
        "latitude":latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date":end_date,
        "timezone":"auto",
        "daily":"precipitation_sum"
     
    }

    response=requests.get (RAINFALL_URL,params =params,timeout =10)
    if response.status_code !=200:
        raise RuntimeError(
            f"Failed to fetch rainfall data for {market_name}: Status code: {response.status_code}"
        )

    daily =response.json()["daily"]
    return pd.DataFrame({
        "date":daily["time"],
        "rainfall_mm":daily["precipitation_sum"],
        "market":market_name
    
})


    