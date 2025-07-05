from llm_helper import llm
from few_shot import FewShotPosts

few_shot = FewShotPosts()


def get_length_str(length):
    if length == "Short":
        return "1 to 5 lines"
    if length == "Medium":
        return "6 to 10 lines"
    if length == "Long":
        return "more than 10 lines"


def generate_post(length, theme, target_audience):
    # get the correct prompt for the passed length, theme and target_audience
    prompt = get_prompt(length, theme, target_audience)
    # invoke llm
    response = llm.invoke(prompt)
    # return response
    return response.content


def get_prompt(length, theme, target_audience):
    length_str = get_length_str(length) # 1 to 5, 6 to 10 or 11 to 15 lines

    prompt = f'''
    Generate a LinkedIn post using the below information. No preamble.

    1) Theme: {theme}
    2) Length: {length_str}
    3) Target audience: {target_audience}
    '''

    # check if some posts with this theme, length and target_audience already exist and store them
    examples = few_shot.get_filtered_posts(length, theme, target_audience)

    if len(examples) > 0: # if such posts exist, add these examples as few shot learning to the prompt
        prompt += "4) Use the writing style as per the following examples."

    for i, post in enumerate(examples):
        post_text = post['text']
        prompt += f'\n\n Example {i+1}: \n\n {post_text}'

        if i == 1: # Use max two samples
            break

    return prompt


if __name__ == "__main__":
    print(generate_post("Medium", "Motivation", "Self-Improvement Seekers"))