import csv, pywebio, time, os, datetime, re, json
from fuzzywuzzy import fuzz, process
from Network import Network
from PIL import Image
from DataLoader import DataLoader
from get_filters import get_filters
import warnings
warnings.filterwarnings("ignore")

any_js = """
        WebIO._state.CurrentSession.ws.addEventListener('close', () => {
            console.log('Test!')
            setTimeout(() => {
                window.location.reload()
            }, 100)
        })
"""

history: list[dict[str,str]] = []

with open('history.json', 'r+', encoding='utf-8') as h:
    history = json.loads(h.read())
data = {}

# with open('data.csv', 'r', encoding='utf-8') as f:
#     reader = csv.reader(f, delimiter=',', quotechar='"')
#     for row in reader:
#         data[row[0]] = row[1]
with open('train.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=',', quotechar='"')
    for row in reader:
        data[row[0]] = [row[1], row[2]]
net = Network()
loader = DataLoader()

os.system('cls||clear')
filters_1 = get_filters('train.csv')
filters_2 = get_filters('data.csv')
filters = list(set([*filters_1, *filters_2]))
def get_images(X_test, y_test, i = 0):
    pred = net.test(X_test, y_test)
    formatted_data = {}
    c = 0
    for g, img in enumerate(pred):
        if round(img) == list(y_test)[g]:
            c += 1

    for i in range(len(y_test)-1):
        _img = list(y_test.head(1+i))[i]
        desc = data.get(str(y_test.index[i]))
        img_src = round(pred[i])
        if os.path.exists(f'train_dataset_train/train/{img_src}.png'):
            img = Image.open(f'train_dataset_train/train/{img_src}.png')
        else:
            img = None
        formatted_data[_img] = {
            'desc': desc,
            'img': img
        }
    return formatted_data
X, y, y_indexes = loader.load_data('train.csv', ["description","object_img", 'id'], filters)
X_train, X_test, y_train, y_test = net.tts(X, y_indexes, test_size=0.3, random_state=42, shuffle=False)

net.train(X, y)
fd = get_images(X_test, y_test)
def main():
    global any_js, data, fd
    # pywebio.session.run_js(any_js)

    def b():

        q: str = pywebio.input.input(placeholder="Введите запрос...", required=True)

        with pywebio.output.use_scope('answer_scope', clear=True):
            for a in process.extract(q, list(data.values()), limit=10000):
                if a[1] > 50:
                    acc = 0
                    target_acc = len(q.split(' '))
                    for word in q.split(' '):
                        if word.lower() in a[0][0].lower():
                            acc += 1
                    if acc == target_acc:
                        if not fd.get(int(a[0][1])) is None:
                            if not fd[int(a[0][1])]['img'] is None:
                                pywebio.output.put_grid([
                                    [pywebio.output.put_image(fd[int(a[0][1])]['img'])],
                                    [pywebio.output.put_text(fd[int(a[0][1])]['desc'][0])]
                                ])
        time.sleep(0.1)
        b()
    b()

if __name__ == '__main__':
    pywebio.start_server(main, port=8080, debug=True)
