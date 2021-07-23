#!/usr/bin/env python

import json
import genanki
from os import listdir


class CustomNote(genanki.Note):
    @property
    def guid(self):
        return genanki.guid_for(self.fields[0])


model = genanki.Model(
    1343037055,
    "Simple Model",
    fields=[
        {"name": "QuestionNumber"},
        {"name": "Question"},
        {"name": "OptionalImage"},
        {"name": "OptionA"},
        {"name": "OptionB"},
        {"name": "OptionC"},
        {"name": "OptionD"},
        {"name": "Answer"},
    ],
    templates=[
        {
            "name": "Card 1",
            "qfmt": "{{Question}}<br><br>{{OptionalImage}}<br><b>A:</b> {{OptionA}}<br><b>B:</b> {{OptionB}}<br><b>C:</b> {{OptionC}}<br><b>D:</b> {{OptionD}}<br>",
            "afmt": '{{Question}}<br><br>{{OptionalImage}}<br><b>A:</b> {{OptionA}}<br><b>B:</b> {{OptionB}}<br><b>C:</b> {{OptionC}}<br><b>D:</b> {{OptionD}}<br><br><hr id="answer"><br><br>{{Answer}}',
        },
    ],
)


def create_note_for_question(question):
    if question["QuestionCorrectAnswer"] == "":
        return None

    optional_image = ""

    if question["QuestionDrawing"] == "True":
        optional_image = f"""<img src="{question['QuestionNr']}.png">"""

    correct_answer_long = question[
        "QuestionAnswer" + question["QuestionCorrectAnswer"] + "NL"
    ]

    return CustomNote(
        model=model,
        fields=[
            question["QuestionNr"],
            question["QuestionTextNL"],
            optional_image,
            question["QuestionAnswerANL"],
            question["QuestionAnswerBNL"],
            question["QuestionAnswerCNL"],
            question["QuestionAnswerDNL"],
            "<b>" + question["QuestionCorrectAnswer"] + "</b>: " + correct_answer_long,
        ],
    )


with open("./data/categories.json", "r") as categories_file, open(
    "./data/questions.json", "r"
) as questions_file:
    categories = json.loads(categories_file.read())
    questions = json.loads(questions_file.read())

decks = {
    category["CategorieFromChapter"]: genanki.Deck(
        2068240807 + int(category["CategorieFromChapter"]),
        "HAREC::" + category["CategorieNameNL"],
    )
    for category in categories
}

for question in questions:
    note = create_note_for_question(question)

    if note != None:
        decks[question["QuestionChapter"]].add_note(note)

package = genanki.Package(decks.values())
package.media_files = [f"img/{img}" for img in listdir("img")]

package.write_to_file("deck.apkg")
