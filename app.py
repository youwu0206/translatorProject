from flask import Flask, render_template, request, send_file
from travel_translation_tool import load_phrases, translate_phrases, generate_pdf

# Initialize Flask app
app = Flask(__name__)


@app.route('/')
def index():
    # Load phrases for category selection
    phrases = load_phrases('phrases.json')
    # get category names from the keys of dictionary
    categories = list(phrases.keys())
    # Passes the list of categories to the template under the variable name categories
    return render_template('index.html', categories=categories)


@app.route('/generate', methods=['POST'])
def generate():
    # Get user input, extract language and categories from input
    target_language = request.form['language']
    selected_categories = request.form.getlist('categories')

    # Load predefined phrases from json
    phrases = load_phrases('phrases.json')
    # filter the dictionary to make sure it only includes certain categories
    selected_phrases = {cat: phrases[cat] for cat in selected_categories}

    # Translate the filtered phrases to target language
    translated_phrases = translate_phrases(selected_phrases, target_language)

    # Generate PDF, naming the output file to be generated_cheat_sheet.pdf
    output_file = 'generated_cheat_sheet.pdf'
    generate_pdf(translated_phrases, output_file)

    # pass the output file to results.html, return the rendered template
    return render_template('results.html', filename=output_file)


@app.route('/download/<filename>')
def download(filename):
    return send_file(filename, as_attachment=True)


# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)


