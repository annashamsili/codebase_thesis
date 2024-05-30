# from the folder names, get the folder and return a pandas dataframe

def get_files(folder):
    from os.path import listdir, isfile, isdir, join
    path = "../data/processed/hashtaglists/{}".format(folder)
    
    if not isfile(path) and not isdir(path):
        print("folder does not exist")
    else:
        files = [f for f in listdir(path) if isfile(join(path, f))]
        return files
        
def get_df(file):
    import pandas as pd
    from os.path import join, isfile, path
    if file.endswith(".csv"):
        # get the file path for each file 
        file_path = join(path, file)
        if isfile(file_path):
            df = pd.read_csv(file_path)
    return df


# here I will collect the rows of the video files - for quant analysis and for features in network
def get_metadata(df, hashtag_dict, keyword):
    import numpy as np
    import pandas as pd
    import regex
    
    #df['hashtags'] = df['hashtags'].str.replace(r'2$', '', regex=True)
    
    df = df.dropna(subset=['hashtags'])
    
    #only keep unique rows
    df = df.drop_duplicates(subset=['id'])
    
    # get the hashtag for which the list was collected
    # split all hashtags in the column, list of strings
    # create a new dataframe with only the rows that contain the relevant hashtag
    df_stripped = df.loc[df['hashtags'].str.split(',').apply(lambda x: keyword in x)]
    
    # add the number of collected videos and the number of relevant videos, which contain the hashtag, to the dictionary
    hashtag_dict[keyword] = {"collected_videos": len(df), "relevant_videos": len(df_stripped)}
    hashtag_dict[keyword]["unique_creators"] = df_stripped["author"].nunique()

    interactions = df_stripped["shares"].sum() + df_stripped["likes"].sum() + df_stripped["comments"].sum()
    hashtag_dict[keyword]["total_interactions"] = interactions
    if len(df_stripped) == 0 or pd.isnull(len(df_stripped)):
        hashtag_dict[keyword]["average_interactions"] = 0
    else:
        hashtag_dict[keyword]["average_interactions"] = round(interactions / len(df_stripped))
    #do the same as above for plays
    if len(df_stripped) == 0 or pd.isnull(len(df_stripped)):
        hashtag_dict[keyword]["average_plays"] = 0
    else:
        hashtag_dict[keyword]["average_plays"] = round(df_stripped["plays"].mean())
    
    return hashtag_dict[keyword]


def weighted_counts(keyword, categories_df, metadata_dict):
    import pandas as pd
    import numpy as np
    total_videos = categories_df.loc[categories_df["hashtags"] == keyword]["tiktok_count"].values
    if len(total_videos) == 0 or pd.isnull(total_videos[0]):
        total_videos = 1
        
    weighted_videocount = metadata_dict[keyword]['collected_videos']/total_videos
    weighted_relevantcount = metadata_dict[keyword]['relevant_videos']/total_videos
    
    if isinstance(weighted_videocount, np.ndarray):
        weighted_videocount = weighted_videocount[0]
    if isinstance(weighted_relevantcount, np.ndarray):
        weighted_relevantcount = weighted_relevantcount[0]
    #weighted_videocount = metadata_dict[keyword]['collected_videos']/total_videos
    #weighted_relevantcount = metadata_dict[keyword]['relevant_videos']/total_videos
    return weighted_videocount, weighted_relevantcount

def get_categories(keyword, categories_df):
    import pandas as pd
    category = categories_df.loc[categories_df["hashtags"] == keyword]["topic"].values
    if len(category) == 0 or pd.isnull(category[0]):
        category = "other"
    else:
        category = category[0]
    return category
    
# create a dictionary of hashtags, where each key contains all hashtags and how often they occur - network
def make_dict(df, keyword):
   # filter out the row with our keyword
   # look up how to deal with no column name
   hashtag_dict = {}
   for row in range(len(df)): 
       hashtag = df["hashtag"][row] #  figure out how to deal w the unnamed column!
       count = df["count"][row] 
       if hashtag == keyword:
           continue
       else:
           hashtag_dict[hashtag] = count
   return hashtag_dict

def make_network(hashtag_dict, G):
    import networkx as nx
    for keyword in hashtag_dict.keys():
        for hashtag in hashtag_dict[keyword].keys():
            G.add_node(hashtag)
            G.add_edge(keyword, hashtag, weight=hashtag_dict[hashtag]["count"]) # weight should probably be the count of the hashtag?
    return G