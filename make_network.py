#%% import statements
import pandas as pd
import networkx as nx 
import numpy as np 
from os.path import isfile, join
from os import listdir
from os.path import isfile, isdir
from functions import make_dict, make_network
import emoji
import json
import csv
import pickle


# 17 april have not run this yet, need to check if it works
#%% first need to create a full dictionary of all the hashtags

# define the dates and phases where we are looking
dates = ["march", "230124", "070324", "210324", "190324", "200324", "140324", "130324", "120324"]
folders = ["lvl1", "lvl2", "lvl3", "lvl4", "lvl5", "lvl6", 'moreseeds']

# initiate dictionary
all_hashtags = {}

#attribute dictionary from pkt file
with open('../data/analysis/metadata_dict_v8.pkl', 'rb') as attributes_file:
    attributes = pickle.load(attributes_file)
    
attributes

#%%
#%%
with open('../data/analysis/metadata_dict_corrected.pkl', 'wb') as f:
    pickle.dump(attributes, f)
    

#%% loop through files and add to dictionary
for folder in folders:
    # get the folder and check it exists
    path = "../data/processed/hashtaglists/{}".format(folder)
    if not isfile(path) and not isdir(path):
        print("folder does not exist")
        continue
    # get all files
    files = [f for f in listdir(path) if isfile(join(path, f))]
    print("number of files:", len(files))
    
    for file in files: 
        if file.endswith(".csv"):
            # get the file path for each file 
            file_path = join(path, file)

            #check the file exists
            if isfile(file_path):
                df = pd.read_csv(file_path) # this should create an unnamed first column instead of unnamed index!
                df.rename(columns = {'Unnamed: 0':'hashtag'}, inplace = True)
                # this removes emojis, idk if it's necessary tho
                df['hashtag'] = df['hashtag'].apply(lambda s: emoji.replace_emoji(s, ''))
                keyword = file_path.split("/")[-1].split(".")[0].split("_")[-1]
                if keyword[-1] == '2':
                    keyword = keyword[:-1]
                hashtag_dict = make_dict(df, keyword)
                # add to the overall dictionary
                all_hashtags[keyword] = hashtag_dict
                
#%%

#all_hashtags

# save the dictionary as a file
#with open('../data/analysis/all_hashtags_v4.pkl', 'wb') as f:
 #   pickle.dump(all_hashtags, f)
    

#%%

G = nx.Graph()

# A set to keep track of hashtags already marked as outer
outer_hashtags = set()

# Iterate through the nested dictionary to add nodes and edges
for outer_hashtag, inner_hashtags in all_hashtags.items():
    # Add outer hashtag as a node and set isOuter attribute to True
    G.add_node(outer_hashtag, isOuter=True)
    outer_hashtags.add(outer_hashtag)  # Mark the outer hashtag as already classified as outer
    
    #add attributes from the attributes dictionary
    G.nodes[outer_hashtag]['category'] = attributes[outer_hashtag]['category']
    G.nodes[outer_hashtag]['collected_videos'] = attributes[outer_hashtag]['collected_videos']
    G.nodes[outer_hashtag]['relevant_videos'] = attributes[outer_hashtag]['relevant_videos']
    G.nodes[outer_hashtag]['unique_creators'] = attributes[outer_hashtag]['unique_creators']
    G.nodes[outer_hashtag]['total_interactions'] = attributes[outer_hashtag]['total_interactions']
    G.nodes[outer_hashtag]['average_interactions'] = attributes[outer_hashtag]['average_interactions']
    G.nodes[outer_hashtag]['phase'] = attributes[outer_hashtag]['phase']
    G.nodes[outer_hashtag]['average_plays'] = attributes[outer_hashtag]['average_plays']
    G.nodes[outer_hashtag]['weighted_collected'] = attributes[outer_hashtag]['weighted_videocount']
    G.nodes[outer_hashtag]['weighted_relevant'] = attributes[outer_hashtag]['weighted_relevantvideos']
    
    for inner_hashtag, weight in inner_hashtags.items():
        # Add inner hashtag as a node
        G.add_node(inner_hashtag, isOuter=False)
        # Check if the inner hashtag is also an outer hashtag
        if inner_hashtag in outer_hashtags:
            # If it is, mark it as outer
            G.nodes[inner_hashtag]['isOuter'] = True
            
            G.nodes[inner_hashtag]['category'] = attributes[inner_hashtag]['category']
            G.nodes[inner_hashtag]['collected_videos'] = attributes[inner_hashtag]['collected_videos']
            G.nodes[inner_hashtag]['relevant_videos'] = attributes[inner_hashtag]['relevant_videos']
            G.nodes[inner_hashtag]['unique_creators'] = attributes[inner_hashtag]['unique_creators']
            G.nodes[inner_hashtag]['total_interactions'] = attributes[inner_hashtag]['total_interactions']
            G.nodes[inner_hashtag]['average_interactions'] = attributes[inner_hashtag]['average_interactions']
            G.nodes[inner_hashtag]['average_plays'] = attributes[inner_hashtag]['average_plays']
            G.nodes[inner_hashtag]['phase'] = attributes[inner_hashtag]['phase']
            G.nodes[inner_hashtag]['weighted_collected'] = attributes[inner_hashtag]['weighted_videocount']
            G.nodes[inner_hashtag]['weighted_relevant'] = attributes[inner_hashtag]['weighted_relevantvideos']
    
        # Check if the edge already exists
        if G.has_edge(outer_hashtag, inner_hashtag):
            # If edge exists, update the weight
            G[outer_hashtag][inner_hashtag]['weight'] += weight
        else:
            # If edge doesn't exist, add it with the weight
            G.add_edge(outer_hashtag, inner_hashtag, weight=weight)



#%%

# save the network 
nx.write_gexf(G, "../data/analysis/network/network_allv6.gexf")
# %%
