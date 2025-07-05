import pandas as pd
import json

# Let's load all the posts into a pandas df so that querying it (based on length, theme, target audience) and returning only the relevant posts becomes easier


class FewShotPosts:
    def __init__(self, file_path="data/processed_posts.json"):
        # This is smn like a constructor
        # Initialize the pandas df and a var called unique_themes to None
        self.df = None
        self.unique_themes = None
        self.unique_target_audience=None
        # Call load_posts() win constructor itself, so just creating an obj of this cls will call this fxn
        self.load_posts(file_path)

    def load_posts(self, file_path):
        with open(file_path, encoding="utf-8") as file:
            # Load the json ile
            posts = json.load(file)
            # Create the df from the json file
            self.df = pd.json_normalize(posts)
            # print(self.df)
            # Add a col called Length to the df which takes the line_count col and applies txformation to it using categorize_length() and returns the size of length of the post
            self.df['length'] = self.df['line_count'].apply(self.categorize_length)
            # collect unique themes
            all_themes = self.df['theme'].apply(lambda x: x).sum()
            self.unique_themes = list(set(all_themes))
            # self.unique_themes=['Emotional Intelligence', 'Self-Improvement', 'Mental Health', 'Motivation', 'Neuroscience', 'Relationships', 'Productivity']

            # collect unique target audiences
            all_target_audiences = self.df['target_audience'].tolist()
            self.unique_target_audience = list(set(all_target_audiences))
            # self.unique_target_audience=['Self-Improvement Seekers', 'Creatives and Entrepreneurs', 'General Audience', 'Couples', 'Professionals', 'Students and Young Professionals', 'Adults']

    def get_filtered_posts(self, length, theme, target_audience):
        df_filtered = self.df[
            (self.df['theme'].apply(lambda themes: theme in themes)) &  # themes contains 'Motivation'
            (self.df['target_audience'] == target_audience) &  # target_audience is 'General Adults'
            (self.df['length'] == length)  # Line count is less than 5
        ]
        return df_filtered.to_dict(orient='records') # orient='records' will return a list of dictionaries

    def categorize_length(self, line_count):
        if line_count < 5:
            return "Short"
        elif 5 <= line_count <= 10:
            return "Medium"
        else:
            return "Long"

    def get_themes(self):
        return self.unique_themes

    def get_target_audience(self):
        return self.unique_target_audience


if __name__ == "__main__":
    fs = FewShotPosts()
    posts = fs.get_filtered_posts("Medium","Motivation","Self-Improvement Seekers")
    print(posts)
