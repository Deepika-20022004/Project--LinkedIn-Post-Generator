import json
from llm_helper import llm
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException


def extract_metadata(post):
    # Takes some trial and error to arrive at the right prompt
    template = '''
    You are given a LinkedIn post. You need to extract number of lines, theme and target_audience.
    1. Return a valid JSON. No preamble. 
    2. JSON object should have exactly three keys: line_count, theme and target_audience. 
    3. theme is an array of text themes. Extract maximum two themes.
    
    Here is the actual post on which you need to perform this task:  
    {post}
    '''   
    # Format the prompt to use it further
    pt = PromptTemplate.from_template(template)
    # Create a pipeline to send the formatted prompt (pt) directly to the llm (llm)
    chain = pt | llm
    # Invoke the pipeline (chain) to generate the response
    response = chain.invoke(input={"post": post})
    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content) # response.content has the actual ans
    except OutputParserException:
        raise OutputParserException("Context too big. Unable to parse jobs.")
    return res


def get_unified_themes(posts_with_metadata):
    unique_themes = set()
    # Loop through each post and extract the themes
    for post in posts_with_metadata:
        # Insert the list of themes for each post into the set (as long as each list is unique)
        unique_themes.update(post['theme'])  # {['a','b'],['c','d'],['e','f']}

    # join all the tags lists  in the set into a comma sep list
    unique_themes_list = ','.join(unique_themes) # ['a','b','c','d','e','f']
    # few shot learning
    template = '''I will give you a list of themes. You need to unify themes with the following requirements:
    1. Themes are unified and merged to create a shorter list. 
       Example 1: "Personal Growth", "Personal Development", "Self-Improvement", "Professional Growth", "Growth" can be all merged into a single theme "Self-Improvement". 
       Example 2: "Motivation", "Motivational", "Inspiration" can be mapped to "Motivation".
       Example 3: "Emotional Intelligence", "Empathy", "Mindfulness", "Self-Love", "Self Care", "Gratitude", "Acceptance"  can be mapped to "Emotional Intelligence".
       Example 4: "Mental Health", "Overcoming Stress", "Nostalgia" can be mapped to "Mental Health".
       Example 5: "Relationships", "Love" can be mapped to "Relationships".
       Example 6: "Productivity" can be mapped to "Productivity".
       Example 7: "Neuroscience" can be mapped to "Neuroscience".
    2. Each theme should follow title case convention. For example: "Personal Growth"
    3. Output should be a JSON object, no preamble
    3. Output should have mapping of original theme and the unified theme. 
       For example: {{"Personal Growth": "Self-Improvement",  "Personal Development": "Self-Improvement", "Motivation": "Motivation"}}
    
    Here is the list of themes: 
    {themes}
    '''

    # Now same way as in extract_metadata(), format prompt, pipe it, invoke, gen response
    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={"themes": str(unique_themes_list)})
    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except OutputParserException:
        raise OutputParserException("Context too big. Unable to parse jobs.")
    return res

def get_unified_target_audience(posts_with_metadata):
    unique_target_audience = set()
    # Loop through each post and extract the target_audience
    for post in posts_with_metadata:
        # Insert the target_audience for each post into the set
        unique_target_audience.add(post['target_audience'])  # {'a','b,'c','d,'e','f'}

    # convert the unique_target_audience set into a list
    unique_target_audience = list(unique_target_audience) # ['a','b','c','d','e','f']
    # print(unique_target_audience_list)

    # # few shot learning
    template = '''I will give you a list of target_audiences. You need to unify them with the following requirements:
    1. Target_audiences are unified and merged to create a shorter list. 
       Example 1: "Students and Young Professionals", "Young adults and professionals", "Young Professionals", "Young adults/students", "Young Adults" can be all merged into a single target_audience "Students and Young Professionals". 
       Example 2: "Individuals seeking self-improvement", "Adults looking for self-improvement", "Adults seeking self-improvement", "Professionals and individuals seeking self-improvement", "Individuals with anxiety or self-doubt, and anyone looking for motivational content", "Young adults and individuals interested in self-improvement", "Adults seeking personal growth", "Individuals seeking motivation and inspiration", "Adults looking for self-improvement advice" can be mapped to "Self-Improvement Seekers".
       Example 3: "General audience", "General public", "General Adults", can be mapped to "General Audience".
       Example 4: "Adults", "Adults in workforce", "Adults in their 20s, 30s, and 40s experiencing loneliness and self-doubt", "adults experiencing loneliness and self-doubt" can be mapped to "Adults".
       Example 5: "Couples", "Boyfriends and Girlfriends" can be mapped to "Couples".
       Example 6: "Professionals" can be mapped to "Professionals".
       Example 7: "Creatives and Entrepreneurs", "YouTube creators and followers", "Content Creators and Followers" can be mapped to "Creatives and Entrepreneurs".
    2. Each theme should follow title case convention. For example: "Creatives and Entrepreneurs"
    3. Output should be a JSON object, no preamble
    3. Output should have mapping of original target_audience and the unified target_audience. 
       For example: {{"Individuals seeking self-improvement": "Self-Improvement Seekers",  "General public": "General Audience"}}
    
    Here is the list of target_audiences: 
    {target_audience}
    '''
    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={"target_audience": str(unique_target_audience)})
    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except OutputParserException:
        raise OutputParserException("Context too big. Unable to parse jobs.")
    return res

def process_posts(raw_file_path, processed_file_path=None):
    # Open the raw json file to be processed (raw_posts.json)
    with open(raw_file_path, encoding='utf-8') as file:
        # Load the raw json file
        posts = json.load(file)
        # print(posts) # just to check if the file has loaded 
        # For each post in posts, shd extract the metadata with a user defined fxn (extract_metadata())
        enriched_posts = []
        for post in posts: 
            # print(post)
            # each post will be like this: {'text': 'abc', 'engagement': 123}
            # Extract metadata for each post
            metadata = extract_metadata(post['text']) 
            # print(metadata)
            # metadata will then be like this: {'line_count': 1, 'language': 'abc', 'tags': ['pqr,'def']}
            # Link each post and its metadata with pipe operator
            post_with_metadata = post | metadata
            # Store these posts with metadata in a list
            enriched_posts.append(post_with_metadata) 
            # check if enriched_posts is right
            # for en_post in enriched_posts:
            #     print(en_post)

    unified_themes=get_unified_themes(enriched_posts)
    # print(unified_themes)
    unified_target_audience=get_unified_target_audience(enriched_posts)
    # print(unified_target_audience)

    for post in enriched_posts:
        # update theme
        current_themes = post['theme']
        new_themes = {unified_themes[theme] for theme in current_themes}
        post['theme'] = list(new_themes)

        # update target_audience
        current_target_audience= post['target_audience']
        new_target_audience = unified_target_audience[current_target_audience]
        post['target_audience'] = new_target_audience

    with open(processed_file_path, encoding='utf-8', mode="w") as outfile:
        json.dump(enriched_posts, outfile, indent=4)


if __name__ == "__main__":
    # On running this file, below function shd be called for preprocessing the raw posts
    # process_posts(<raw_file>,<processed_file>)
    process_posts("data/raw_posts.json", "data/processed_posts.json")