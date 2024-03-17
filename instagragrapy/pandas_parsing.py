import pandas as pd


def parse_csv(path):
    df = pd.read_csv(path)
    posts = []
    for post in df["post_url"]:
        posts.append(post)
    print("the number of posts is: ",len(posts))
    return posts


def delete_csv(path, size):
    df = pd.read_csv(path)
    for i in range(size):
        df.drop(index=i, inplace=True)
    df.to_csv("updated_group3.csv")
    print("number of posts left: ", len(df))
