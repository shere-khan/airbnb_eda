import pandas as pd
import seaborn as sns
from pathlib import Path
from matplotlib import pyplot as plt
import os

def main():
    path = "data"
    df = load_data(path)

    # find_numeric_columns(df)

    # Remove specific columns.
    # df = keep_cols(df, "doc/columns/listings_interesting_columns.txt")

    # Plot correlation map.
    corr_plot(df)

    # Date vs number of listings. Did number of listings decrease after shutdown?
    # date_x_num_listings(df)

def find_numeric_columns(df):
    dts = pd.DataFrame(df.dtypes)
    dts.reset_index(inplace=True)
    dts.columns = ["cols", "dt"]
    df_ = dts[(dts.dt == "int64") | (dts.dt == "float64")]
    list(map(print, df_.cols.unique()))

def corr_plot(df):
    # Correlation plot.
    df = keep_cols(df, "doc/columns/corrplot.txt")
    plt.figure(figsize=(20, 20))
    heat_map = sns.heatmap(df)
    plt.show()

def date_x_num_listings(df):
    # Filter out junk dates.
    date_path = "doc/dates/valid_dates.txt"
    dates = get_list_from_text(date_path)
    df = df[df["last_scraped"].isin(dates)]

    # Group by date and plot num of listings by date.
    df_ = df.groupby("last_scraped").agg({"id": "count"})
    df_ = df_.reset_index()
    plt.figure(figsize=(20, 10))
    sns.lineplot(data=df_, x="last_scraped", y="id")
    plt.show()

def get_list_from_text(path):
    with Path(path).open("r") as f:
        valid = f.readlines()
        valid = set(map(lambda x: x.replace("\n", ""), valid))
    return valid

def keep_cols(df, path):
    cols = get_list_from_text(path)
    df = df[cols]
    return df

def remove_cols(df, path):
    cols = get_list_from_text(path)
    rem = cols.intersection(df.columns)
    df_ = df.drop(rem, axis=1)
    return df_

def load_data(dir):
    path = os.walk(dir)
    dfs = []
    for root, directories, files in path:
        for file in files:
            if root.split("/")[-1] != "summary":
                if file.split(".")[0] == "listings":
                    f = Path(root) / file
                    dfs.append(pd.read_csv(f))
    df = pd.concat(dfs)
    return df

def examine_col_diff():
    with Path("doc/columns/listings_short_columns.txt").open("r") as f:
        short = f.readlines()
        short = set(map(lambda x: x.replace("\n", ""), short))

    with Path("doc/columns/listings_interesting_columns.txt").open("r") as f:
        interesting = f.readlines()
        interesting = set(map(lambda x: x.replace("\n", ""), interesting))

    print(short.difference(interesting))

if __name__ == '__main__':
    main()