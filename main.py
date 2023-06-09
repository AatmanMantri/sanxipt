import requests


# Function to extract text from a webpage
def extract_text(url):
    response = requests.get(url)
    html_text = response.text

    # Remove HTML tags
    extracted_text = ""
    in_tag = False
    for char in html_text:
        if char == '<':
            in_tag = True
        elif char == '>':
            in_tag = False
        elif not in_tag:
            extracted_text += char

    return extracted_text.strip()


# Simple evaluation algorithm to measure performance
def evaluate_extraction(original_text, extracted_text):
    original_words = original_text.split()
    extracted_words = extracted_text.split()

    # Calculate the word overlap
    common_words = set(original_words) & set(extracted_words)
    overlap_percentage = len(common_words) / len(original_words) * 100

    # Calculate the extraction ratio based on the number of extracted words and total words in the original text
    extraction_ratio = len(extracted_words) / len(original_words) * 100

    return overlap_percentage, extraction_ratio


# Function to send text to ChatGPT and get a summary
def get_summary(text):
    api_key = "YOUR_OPENAI_API_KEY"
    endpoint = "https://api.openai.com/v1/engines/davinci/completions"

    prompt = f"summarize the below text in 7 points:\n{text}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "prompt": prompt,
        "max_tokens": 50
    }

    response = requests.post(endpoint, headers=headers, json=data)
    response_json = response.json()
    print("response_json:", response_json)
    summary = response_json["choices"][0]["text"].strip()

    return summary


# URL of the webpage to extract text from
url = "https://techcrunch.com/2023/06/07/openai-gpt5-sam-altman/?utm_source=tldrai"

# Extract text from the webpage
original_text = extract_text(url)

# Modifications to the extracted text (can be extended with more modifications if needed)
modifications = {
    "original": original_text,
}

# Evaluate the performance for each modification and get the summaries
evaluation_results = []
for modification, extracted_text in modifications.items():
    overlap_percentage, extraction_ratio = evaluate_extraction(original_text, extracted_text)
    summary = get_summary(extracted_text)

    evaluation_results.append((modification, overlap_percentage, extraction_ratio, summary))


# Print the original text
print("Original Text:")
print("---------------------------")
print(original_text)
print("---------------------------\n")

# Print the evaluation results and summaries in a tabular format
print("Performance Evaluation:")
print("---------------------------------------------------------------------------------------------")
print("|   Modification   |  Overlap (%)  |  Extraction (%)  |                      Summary                       |")
print("|------------------|---------------|------------------|----------------------------------------------------|")
for modification, overlap_percentage, extraction_ratio, summary in evaluation_results:
    print(f"|   {modification:<16}|    {overlap_percentage:.2f}     |      {extraction_ratio:.2f}      |  {summary:<50}  |")
print("---------------------------------------------------------------------------------------------")
