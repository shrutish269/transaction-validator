def split_dataframe(df, chunk_size=1000):

    chunks = []

    for i in range(0, len(df), chunk_size):
        chunks.append(df.iloc[i:i + chunk_size])

    return chunks