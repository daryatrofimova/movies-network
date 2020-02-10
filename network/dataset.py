import os

import pandas as pd


def prepare_dataset(path: str, filename: str, separator=',') -> pd.DataFrame:
    df = pd.read_csv(os.path.join(path, filename), sep=separator)[['cast', 'id']]
    df['cast'] = df.cast.apply(eval)
    # expand cast actors
    df = pd.DataFrame([{'movie_id': movie, **c} for movie, cast in zip(df.id, df.cast) for c in cast])

    # remove fields we don't need
    df = df[['movie_id', 'name']]
    df = df.merge(df, on=['movie_id'], how='outer')

    # return pairs of actors connected through the same movie
    return (df
            .loc[df.name_x != df.name_y]  # exclude duplicates from df.merge
            # there are a few duplicated names in the dataset, let's ignore them for now
            .groupby(['name_x', 'name_y'])
            .agg(cnt=pd.NamedAgg(column='movie_id', aggfunc='count'))
            .reset_index())

