import csv, pywebio, time
from fuzzywuzzy import fuzz, process

def main():
    data = {}

    with open('data.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')

        for row in reader:
            data[row[1]] = {
                'id': row[0],
                'text': row[1]
            }
    def b():
        q = pywebio.input.input(placeholder="Введите запрос...")

        with pywebio.output.use_scope('answer_scope', clear=True):
            for a in process.extract(q, list(data.keys())):
                # if a[1] > 50:
                pywebio.output.put_text(a[0])
        time.sleep(0.1)
        b()
    b()

if __name__ == '__main__':
    pywebio.start_server(main, port=8080, debug=True)
