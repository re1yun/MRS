# -*- coding: utf-8 -*-
import fire
from tqdm import tqdm

from recom_util import load_json
from recom_util import write_json
from recom_util import remove_seen
from recom_util import most_popular


class MostPopular:
    def _generate_answers(self, train, questions):
        _, song_mp = most_popular(train, "songs", 200)
        _, tag_mp = most_popular(train, "tags", 100)

        answers = []

        for q in tqdm(questions):
            answers.append({
                "uid": q["uid"],
                "songs": remove_seen(q["songs"], song_mp)[:10],
                #"tags": remove_seen(q["tags"], tag_mp)[:10],
            })

        return answers

    def run(self, train_fname, question_fname):
        print("Loading train file...")
        train = load_json(train_fname)

        print("Loading question file...")
        questions = load_json(question_fname)

        print("Writing answers...")
        answers = self._generate_answers(train, questions)
        write_json(answers, "results/results.json")

        return answers


if __name__ == "__main__":
    fire.Fire(MostPopular)

