import pandas as pd
import datetime

from pretreatment.building import pre_building
from pretreatment.direction import pre_direction
from pretreatment.encoding import pre_encoding
from pretreatment.floor import pre_floor
from pretreatment.model import pre_model
from pretreatment.overview import pre_overview


def pre_datatype(df):
    # df['district'] = df['district'].astype('category')
    df['rooms'] = df['rooms'].astype('int64')
    df['living_rooms'] = df['living_rooms'].astype('int64')
    df['direction'] = df['direction'].astype('bool')
    # df['decoration'] = df['decoration'].astype('category')
    # df['floor'] = df['floor'].astype('category')
    df['total_floor'] = df['total_floor'].astype('int64')
    df['built_year'] = df['built_year'].astype('datetime64[ns]')
    df['subway'] = df['subway'].astype('bool')
    df['taxfree'] = df['taxfree'].astype('bool')
    df['reference'] = df['reference'].astype('bool')
    df['date'] = df['date'].astype('datetime64[ns]')

    return df

def pretreatment(savefname):
    df = pre_overview()
    df = pre_direction(df)
    df = pre_floor(df)
    df = pre_building(df)
    df = pre_model(df)
    df = pre_encoding(df)
    df = pre_datatype(df)
    df['built_year'] = df['built_year'].dt.year
    df['month'] = df['date'].dt.month
    # delete variables
    df = df.drop(['keywords', 'region', 'position', 'reference', 'date'], axis=1)

    print(df.info())

    df.to_csv(savefname, encoding='utf-8', index=False)
    print("Pretreat Success!\n")

    return df