from google.cloud import translate_v2 as translate
from fpdf import FPDF
import json


# define a function to load phrases from the list of phrases I wrote from json
def load_phrases(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# define a function to translate the phrases using Google Translate API
# takes a list of phrases (str) and target language (str) as parameters and returns the translated phrases in a dictionary,
# key is the original phrase in English, value is the translated version in target language

def translate_phrases(phrases, target_language):
    # Initialize the Google Cloud Translation API client
    client = translate.Client()
    # initialize an empty dictionary for return
    translated_phrases = {}
    # iterate over the phrases dictionary, key is the category and value is the phrase_list
    for category, phrase_list in phrases.items():
        # initialize an empty list for translated phrases in the current category
        translated_phrases[category] = []

        # iterates over the list of phrases in the current category
        for phrase in phrase_list:
                # use the API to translate texts
                translation = client.translate(phrase, target_language=target_language)
                translated_phrases[category].append(translation['translatedText'])

    return translated_phrases

# define a function that generates a PDF
def generate_pdf(translated_phrases, output_file):
    # initialize a pdf object, adding pages and setting font and font size to it
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', size=12)

    # for loop to iterate over translated_phrases dictionary
    for category, phrases in translated_phrases.items():
        # for each category, make the text bold and bigger
        pdf.set_font("Arial", style="B", size=14)
        # for each phrase under the categories, make the font sizes normal
        pdf.set_font("Arial", size=12)

        # for loop to iterate over the list of translated phrases in the current category
        for phrase in phrases:
            # adds each phrase to the PDF and moves to a new line
            pdf.cell(0, 10, txt=phrase, ln=True)

    # save the PDF
    pdf.output(output_file)







