#!/usr/bin/env python

import json
import genanki

my_model = genanki.Model(
    1343037055,
    "Simple Model",
    fields=[
        {"name": "Question"},
        {"name": "OptionA"},
        {"name": "OptionB"},
        {"name": "OptionC"},
        {"name": "OptionD"},
        {"name": "Answer"},
    ],
    templates=[
        {
            "name": "Card 1",
            "qfmt": "{{Question}}<br><br><b>A:</b> {{OptionA}}<br><b>B:</b> {{OptionB}}<br><b>C:</b> {{OptionC}}<br><b>D:</b> {{OptionD}}<br>",
            "afmt": '<hr id="answer">{{Answer}}',
        },
    ],
)

def create_note_for_question(question):
    if question['QuestionCorrectAnswer'] == '':
        return None

    correct_answer_long = question['QuestionAnswer' + question['QuestionCorrectAnswer'] + 'NL']

    return genanki.Note(
        model=my_model,
        fields=[
            question['QuestionTextNL'],
            question['QuestionAnswerANL'],
            question['QuestionAnswerBNL'],
            question['QuestionAnswerCNL'],
            question['QuestionAnswerDNL'],
            '<b>' + question['QuestionCorrectAnswer'] + '</b>: ' + correct_answer_long
        ]
    )


with open("./data/categories.json", "r") as categories_file, open(
    "./data/questions.json", "r"
) as questions_file:
    categories = json.loads(categories_file.read())
    questions = json.loads(questions_file.read())

decks = {
    category['CategorieFromChapter']: genanki.Deck(2068240807 + int(category['CategorieFromChapter']), "HAREC: " + category['CategorieNameNL'])
    for category in categories
}

for question in questions:
    note = create_note_for_question(question)

    if note != None:
        decks[question['QuestionChapter']].add_note(note)

genanki.Package(decks.values()).write_to_file('deck.apkg')
