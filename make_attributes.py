#%%
import pandas as pd
import numpy as np
from functions import get_metadata, make_dict, get_categories, weighted_counts
from os import listdir
from os.path import isfile, isdir, join
import emoji
import pickle

dates = ["march", "230124", "070324", "210324", "190324", "200324", "140324", "130324", "120324"]
folders = ["seedlist", "phase2","phase3", "phase4", "phase5", "phase6"]

metadata_dict = {}

categories_df = pd.read_csv("../data/analysis/hashtags_classified_v2.csv")

categories_df.head(10)

#%%

no_hashtags_used=[]
missing_categories = []
duplicate_value = []

#%% loop through files and add to dictionary
for folder in folders:
    # get the folder and check it exists
    for date in dates:
        path = "../data/raw/{}/{}".format(folder, date)
        if not isfile(path) and not isdir(path):
            #print("folder does not exist")
            continue
        # get all files
        files = [f for f in listdir(path) if isfile(join(path, f))]
        #print("number of files:", len(files))
        for file in files: 
            if file == ".DS_Store":
                continue
            #print(file)
            # get the file path for each file 
            file_path = join(path, file)
            #print(file_path)
            #check the file exists
            if isfile(file_path):
                df = pd.read_csv(file_path) 
                df.head(10)
                #df['hashtag'] = df['hashtag'].apply(lambda s: emoji.replace_emoji(s, ''))
                keyword = file.split(".")[0]
                if "_" in keyword:
                    keyword = keyword.split("_")[1]
                if "2" in keyword:
                    og_keyword = keyword
                    keyword = og_keyword[:-1]
                    print("This keyword is double", og_keyword)
                #print(keyword)
                # add to the overall dictionary
                #if the keyword already exists, update the values
                if keyword in metadata_dict.keys():
                    print("keyword", keyword, "already exists")
                    duplicate_value.append(keyword)
                else:
                    metadata_dict[keyword] = get_metadata(df, metadata_dict, keyword)
                    metadata_dict[keyword]['phase'] = folder
                    metadata_dict[keyword]["category"] = get_categories(keyword, categories_df)
                    metadata_dict[keyword]["weighted_videocount"], metadata_dict[keyword]["weighted_relevantvideos"] = weighted_counts(keyword, categories_df, metadata_dict)
                    metadata_dict[keyword]["weighted_videocount"] = metadata_dict[keyword]["weighted_videocount"]
                    if metadata_dict[keyword]["category"] == "other":
                        print(keyword, "is missing a category")
                        missing_categories.append(keyword)
                    if metadata_dict[keyword]["relevant_videos"] <2:
                        print("Few or no videos used the hashtag", keyword)
                        no_hashtags_used.append(keyword)


len(metadata_dict.keys())


#before you save this, check manually that u didn't misspell wiead from wieiad

#%%
duplicate_value

# %%

import pickle


# save dictionary as file

with open('/Users/anna/Desktop/MasterThesis/data/analysis/metadata_dict_v8.pkl', 'wb') as f:
    pickle.dump(metadata_dict, f)
# %%
# run this once you've checked everything above

print("amount of hashtags", len(metadata_dict.keys()))
print("amount of tags were only used once or never", len(no_hashtags_used))
print("the number of tags that need to be manually categorised:", len(missing_categories))
# %%
for category in no_hashtags_used:
    print(category)
# %%

for value in metadata_dict:
    print(value, ": ", metadata_dict[value]["weighted_videocount"])
