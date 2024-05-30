#%%
import pandas as pd
import numpy as np
import seaborn as sns
import pickle
import matplotlib.pyplot as plt


with open('../data/analysis/metadata_dict_v8.pkl', 'rb') as attributes_file:
    attributes = pickle.load(attributes_file)
    

attributes['dietculture']['category'] = 'random'
    
    
# Transform the attributes dictionary to a dataframe
df_attributes = pd.DataFrame(attributes).T

# %%
df_attributes.head()




#%%
# calculate a new column called untagged_videos, which is collected_videos - relevant_videos
df_attributes['untagged_videos'] = df_attributes['collected_videos'] - df_attributes['relevant_videos']
# %%
    
df_attributes.to_csv('/Users/anna/Desktop/MasterThesis/data/analysis/hashtag_metadata_v8_withkeywords.csv', index=True)
# %%
# Assuming df is your DataFrame containing the data
# Grouping by 'phase' and summing up the relevant_videos and collected_videos
phase_data = df_attributes.groupby('phase')[['collected_videos', 'relevant_videos']].sum().reset_index()

# Plotting the stacked bar plot
plt.figure(figsize=(10, 6))

# Add horizontal, light grey grid lines
plt.grid(axis='y', color='lightgrey', zorder=-10)  # Set zorder to 0 to place the grid in the background

sns.barplot(x='phase', y='collected_videos', data=phase_data, color='lightblue', label='Fuzzy search results', zorder=2)
sns.barplot(x='phase', y='relevant_videos', data=phase_data, color='darkblue', label='Relevant videos', zorder=10)
plt.title('Videos collected for each phase')
plt.xlabel('Phase')
plt.ylabel('Number of Videos')

# Add values to the columns
for index, row in phase_data.iterrows():
    collected_videos = row['collected_videos']
    relevant_videos = row['relevant_videos']
    untagged_videos = collected_videos - relevant_videos
    #plt.text(index, relevant_videos, str(relevant_videos), ha='center', va='bottom')
    #plt.text(index, collected_videos, str(untagged_videos), ha='center', va='top')
    percentage = relevant_videos / collected_videos * 100
    plt.text(index, relevant_videos, f"{percentage:.1f}%", ha='center', va='bottom')

plt.legend()

plt.show()






# %% videos per category
phase_data = df_attributes.groupby('category')[['collected_videos', 'relevant_videos']].sum().reset_index()

# Plotting the stacked bar plot
plt.figure(figsize=(10, 6))

# Add horizontal, light grey grid lines
plt.grid(axis='y', color='lightgrey', zorder=-10)  # Set zorder to 0 to place the grid in the background

sns.barplot(x='category', y='collected_videos', data=phase_data, color='lightblue', label='Fuzzy search results', zorder=2)
sns.barplot(x='category', y='relevant_videos', data=phase_data, color='darkblue', label='Videos using the hashtag', zorder=10)
plt.title('Videos by manual categorisation')
plt.xlabel('Category')
plt.ylabel('Number of Videos')

# Rotate x-axis labels
plt.xticks(rotation=75)

# Add values to the columns
for index, row in phase_data.iterrows():
    collected_videos = row['collected_videos']
    relevant_videos = row['relevant_videos']
    untagged_videos = collected_videos - relevant_videos
    #plt.text(index, relevant_videos, str(relevant_videos), ha='center', va='bottom')
    #plt.text(index, collected_videos, str(untagged_videos), ha='center', va='top')
    percentage = relevant_videos / collected_videos * 100
    plt.text(index, relevant_videos, f"{percentage:.0f}%", ha='center', va='bottom')
    

plt.legend()

plt.show()


# %%
print("Total count of videos: ", df_attributes['collected_videos'].sum())
print("Total count of relevant videos: ", df_attributes['relevant_videos'].sum())
print("Total count of untagged videos: ", df_attributes['untagged_videos'].sum())
print("Percentage of relevant videos: ", df_attributes['relevant_videos'].sum() / df_attributes['collected_videos'].sum() * 100, "%")

print("Total count of videos in the dataset: ", len(df_attributes))
print("Average interactions per video: ", df_attributes['total_interactions'].mean())

print("Rows with ""random"" category: ", df_attributes[df_attributes['category'] == 'random'])

# %%
other_videos = df_attributes[df_attributes['category'] == 'other']

# %%
