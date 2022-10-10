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
        }, 15000)
    })
"""

history: list[dict[str,str]] = []

with open('history.json', 'r+', encoding='utf-8') as h:
    history = json.loads(h.read())

data = {}

with open('train.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=',', quotechar='"')
    for row in reader:
        data[row[0]] = row[1]
net = Network()
loader = DataLoader()

filters_1 = get_filters('train.csv')
filters_2 = get_filters('data.csv')
# filters = list(set([*filters_1, *filters_2]))
filters = []
for filt in filters_1:
    if filt in filters_2:
        filters.append(filt)

filters = list(set(filters))


def get_images(X_test, y_test, i = 0):
    global data
    _img = list(y_test.head(1+i))[i]
    desc = data.get(str(y_test.index[i]))
    pred = net.test(X_test, y_test)
    img_src = round(pred[i])

    c = 0
    for g, img in enumerate(pred):
        if round(img) == list(y_test)[g]:
            c += 1

    print(f'Count: {c}, {((c/len(y_test))*100):.3f}%')

    if _img == img_src and i+2 <= len(y_test):
        print(f'{_img=} == {img_src=}')
        return get_images(X_test, y_test, i+1)
    return _img, img_src, desc, c, ((c/len(y_test))*100)

def make_solutions():
    global net, loader
    test_X, test_y, test_y_indexes = loader.load_data('data.csv', ["description",'id'], filters)
    p = net.test(test_X)
    data = {}
    with open('data.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        for i, row in enumerate(reader, start=-1):
            if i == -1:
                continue
            if i < len(p):
                data[row[0]] = p[i]
            else:
                break
    d = re.sub(r'[\-\:\.]', '_', re.sub(r'\s', 'T', str(datetime.datetime.today())))
    with open(f'solution_{d}.csv', 'w', encoding='utf-8') as f:
        f.write('id,object_img\n')
        for key, value in list(data.items()):
            f.write(f'{key},{round(value)}\n')
    pywebio.output.toast('Решение сохранено!', color='success')

os.system('cls||clear')
print('Loading data...')
X, y, y_indexes = loader.load_data('train.csv', ["description","object_img", 'id'], filters)
X_train, X_test, y_train, y_test = net.tts(X, y_indexes, test_size=0.3, random_state=42, shuffle=False)
print('Loading data end!')

print('Training...')
net.train(X, y)
print('Training end!')

def main():
    global any_js, make_solutions, filters
    pywebio.session.run_js(any_js)
    pywebio.session.run_js(f"""console.log({str(json.dumps(filters))})""")

    def b():
        global history, get_images, net

        _img, img_src, desc, count, percent = get_images(X_test, y_test)

        current_acc = float(re.findall(r'[\d\.]+', net.last_accuracy )[0])
        try:
            last_acc = float(re.findall(r'[\d\.]+', list(map(lambda x: x['accuracy'], history))[-1])[0])
        except Exception as e:
            last_acc = 0

        state = 'улучшилось!'

        if current_acc > last_acc:
            state = 'улучшилось!'
            history.append({
                'date': str(datetime.datetime.today()),
                'accuracy': net.last_accuracy
            })
            with open('history.json', 'w+', encoding='utf-8') as h:
                h.write(json.dumps(history, indent=4))
        elif current_acc == last_acc:
            state = 'не изменилось!'
        else:
            state = 'ухудшилось!'

        if os.path.exists(f'train_dataset_train/train/{img_src}.png'):
            img = Image.open(f'train_dataset_train/train/{img_src}.png')
        else:
            img = None
        with pywebio.output.use_scope('network_test', clear=True):
            pywebio.output.put_text(f'Метрика: {net.last_accuracy}, {state}')
            pywebio.output.put_text(f'Кол-во совпадений: {count}, {percent:.3f}%')
            pywebio.output.put_text(desc)
            pywebio.output.put_grid([
                [pywebio.output.put_text(f'Должно быть ({_img}.png)'), pywebio.output.put_text(f'Получается ({img_src}.png)')],
                [pywebio.output.put_image(src=Image.open(f'train_dataset_train/train/{_img}.png')), (pywebio.output.put_text(f'Not found image "{img_src}.png"!') if img is None else pywebio.output.put_image(src=img))]
            ])

    pywebio.output.put_row([
        pywebio.output.put_button('Начать!', onclick=b), pywebio.output.put_button('Сохранить', onclick=net.save), pywebio.output.put_button('Создать решение', onclick=make_solutions)
    ], size='100px 120px')
    b()


if __name__ == '__main__':
    pywebio.start_server(main, port=8080, debug=True)
