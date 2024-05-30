#%%
#import statements
import pandas as pd 
import numpy as np

#%% functions
def find_cooccur(df, searchterm):
    word_dict = {}
    for row in df:
        if row is not np.nan:
            hashtags = row.split(",")
            if searchterm in hashtags:
                for hashtag in hashtags:
                    if hashtag in word_dict:
                        word_dict[hashtag] += 1
                    else:
                        word_dict[hashtag] = 1
    return word_dict

def clean_dict(word_dict, to_ignore):
    for word in to_ignore:
        if word in word_dict:
            del word_dict[word]
    return word_dict

def dict_to_df(word_dict):
    word_df = pd.DataFrame.from_dict(word_dict, orient='index', columns=['count'])
    word_df = word_df.sort_values(ascending=False, by='count')
    return word_df


#%% stop words & filenames

to_ignore = ['fyp', 'viral', 'foryou', 'foryoupage', 'fypage', 
             'foryourpage', 'foryoupage', 'fypage', 'fypg', 'fypchallenge', 
             'fypシ', "fy", "capcut", "viralvideo", "viralvideos", "trending",
             "foryoupageofficiall", "foryoupageofficial", "4u", "ypシ゚viral", 
             "account", "tiktok", "tt", "me", "xhtiktok", "tiktokindia", "tiktokusa", 
             "fypシ゚viral", "explorepage", "foryoupage❤", "f4f", "stitch", "tiktokedit", "xyzbca", "trend", "trending"]

# get filenames
#filenames = ["model.csv"]
#%% loop through files

for filename in filenames:
    filepath = "../data/raw/phase6/210324/{}".format(filename)
    searchterm = filename.split(".")[0]
    df = pd.read_csv(filepath)
    df = df['hashtags']
    # create a dictionary of co-occurrences
    word_dict = find_cooccur(df, searchterm)
    # removing the stopwords
    word_dict = clean_dict(word_dict, to_ignore)
    word_df = dict_to_df(word_dict)
    word_df['searchterm'] = searchterm
    print(word_df.head(15))
    word_df.to_csv('../data/processed/hashtaglists/lvl6/cooccur_{}.csv'.format(searchterm))

# %%

filepath = "../data/raw/seedlist/march/thynspo.csv"
searchterm = "thynspo"
df = pd.read_csv(filepath)
df = df['hashtags']
df.head(10)

#%%
word_dict = find_cooccur(df, searchterm)
print(word_dict)
#%%
word_dict = clean_dict(word_dict, to_ignore)
word_df = dict_to_df(word_dict)
word_df['searchterm'] = searchterm
print(word_df.head(15))
word_df.to_csv('../data/processed/hashtaglists/moreseeds/cooccur_{}.csv'.format(searchterm))
# %%
