'''
  GUI based search engine to index and search local files
  Author:     Siddhant Medar
  Email:      siddhantsmedar@gmail.com
  Modified:   19th May,2022
'''

import os
import pickle
import PySimpleGUI as pygui
from typing import Dict

pygui.ChangeLookAndFeel('Black')


class GUI:
    def __init__(self):
        self.layout: list = [
            [pygui.Text('Search Term', size=(11, 1)),
             pygui.Input(size=(40, 1), focus=True, key="_TERM_"),
             pygui.Radio('Contains', size=(10, 1), group_id='choice', key="_CONTAINS_", default=True),
             pygui.Radio('StartsWith', size=(10, 1), group_id='choice', key="_STARTSWITH_"),
             pygui.Radio('EndsWith', size=(10, 1), group_id='choice', key="_ENDSWITH_")],
            [pygui.Text('Path', size=(11, 1)),
             pygui.Input('C:/', size=(40, 1), key="_PATH_"),
             pygui.FolderBrowse('Browse', size=(10, 1)),
             pygui.Button('Re-Index', size=(10, 1), key="_IDX_"),
             pygui.Button('Search', size=(10, 1), bind_return_key=True, key="_SEARCH_")],
            [pygui.Output(size=(100, 30))]]

        self.window: object = pygui.Window('File Search Engine', self.layout, element_justification='left')


class FileSearchEngine:
    def __init__(self):
        self.file_idx = []
        self.results = []
        self.matches = 0
        self.records = 0

    def create_new_idx(self, values: Dict[str, str]) -> None:
        root_path = values['_PATH_']
        self.file_idx: list = [(root, files) for root, dirs, files in os.walk(root_path) if files]

        with open('file_idx.pkl', 'wb') as f:
            pickle.dump(self.file_idx, f)

    def load_existing_idx(self) -> None:
        try:
            with open('file_idx.pkl', 'rb') as f:
                self.file_idx = pickle.load(f)
        except:
            self.file_idx = []

    def search(self, values: Dict[str, str]) -> None:
        self.results.clear()
        self.matches = 0
        self.records = 0
        term = values['_TERM_']

        # search for matches and count results
        for path, files in self.file_idx:
            for file in files:
                self.records += 1
                if (values['_CONTAINS_'] and term.lower() in file.lower() or
                        values['_STARTSWITH_'] and file.lower().startswith(term.lower()) or
                        values['_ENDSWITH_'] and file.lower().endswith(term.lower())):

                    result = path.replace('\\', '/') + '/' + file
                    self.results.append(result)
                    self.matches += 1
                else:
                    continue

        with open('results.txt', 'w') as f:
            for row in self.results:
                f.write(row + '\n')


def main():
    g = GUI()
    s = FileSearchEngine()
    s.load_existing_idx()  # load if exists, otherwise return empty list

    while True:
        event, values = g.window.read()

        if event is None:
            break
        if event == '_IDX_':
            s.create_new_idx(values)
            print()
            print(">> New index created!")
            print()
        if event == '_SEARCH_':
            s.search(values)

            print()
            for result in s.results:
                print(result)

            print()
            print(">> Searched {:,d} records and found {:,d} matches".format(s.records, s.matches))
            print(">> Results saved in working directory as results.txt.")


if __name__ == '__main__':
    print('Starting program...')
    main()
