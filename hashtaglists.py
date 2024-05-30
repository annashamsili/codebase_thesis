#%%
#import statements
import pandas as pd 
import numpy as np

searchterms = []

# find new hashtags

# get filenames
filenames = ["almondmoms.csv", "anarecovry.csv", "caloriedeficitforweightloss.csv",
             "calories.csv", "cassieainsworthedit.csv", "cleangirl.csv", "coquetteaesthetic.csv", 
             "datingtipsforwomen.csv", "diet.csv", "dinnerideas.csv", "easyrecipes.csv", "easyweightloss.csv",
             "fatlosshelp.csv", "girltips.csv", "girlygirl.csv", "glowuptips.csv", 
             "gymfood.csv", "gymtok.csv", "momlife.csv", "momsoftiktok.csv", "momtok.csv",
             "morningroutine.csv", "nightroutine.csv", "ootd.csv", "pilatesprincess.csv", 
             "pinkaesthetic.csv", "selfcareroutine.csv", "thatgirl.csv", "vanillagirl.csv", 
             "weightlossfood.csv", "weightlosstipsforwomen.csv", "weightlosstransformation.csv"]

#%%

hashtaglists = [pd.read_csv("../data/processed/hashtaglists/lvl4/cooccur_{}".format(filename)).sort_values(ascending=False, by='count') for filename in filenames]
#%% show me most popular ones per list
i = 0

for file in hashtaglists:
    keyword = filenames[i].split(".")[0]
    print(keyword)
    print(file.head(25))
    i += 1
    
#%%combine all the dataframes
combined_df = pd.concat(hashtaglists, join='outer', ignore_index=True, axis=0)
combined_df = combined_df.sort_values(ascending=False, by='count')
combined_df = combined_df.drop_duplicates()
combined_df.head(50)

# %%
