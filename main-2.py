import csv, pywebio, time, os, datetime, re, json
from fuzzywuzzy import fuzz, process
from Network import Network
from PIL import Image
from DataLoader import DataLoader
from get_filters import get_filters

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

def main():
    global any_js
    # pywebio.session.run_js(any_js)
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
    def b():
        X, y, y_indexes = loader.load_data('train.csv', ["description","object_img", 'id'], filters)
        X_train, X_test, y_train, y_test = net.tts(X, y_indexes, test_size=0.3, random_state=42, shuffle=False)

        net.train(X, y)
        fd = get_images(X_test, y_test)

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
                                print(fd[int(a[0][1])]['img'])
                                pywebio.output.put_grid([
                                    [pywebio.output.put_image(fd[int(a[0][1])]['img'])],
                                    [pywebio.output.put_text(fd[int(a[0][1])]['desc'][0])]
                                ])
        time.sleep(0.1)
        b()
    b()

    def make_solutions():
        test_X, test_y, test_y_indexes = loader.load_data('data.csv', ["description",'id'], filters)
        p = net.test(test_X)
        # print(p)
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

    def b2():
        global history

        # for filt in filters_1:
        #     if filt in filters_2:
        #         filters.append(filt)

        pywebio.session.run_js(f"""console.log({str(json.dumps(filters))})""")

        X, y, y_indexes = loader.load_data('train.csv', ["description","object_img", 'id'], filters)
        X_train, X_test, y_train, y_test = net.tts(X, y_indexes, test_size=0.3, random_state=42, shuffle=False)

        net.train(X, y)

        # print(dict(y_test))

        _img, img_src, desc, count, percent = get_images(X_test, y_test)

        # with open('history.txt', 'w+', encoding='utf-8') as h:
        #     h.write(f'{str(datetime.datetime.today())} - Accuracy: {net.last_accuracy}')

        # current_acc = float(re.findall(r'[\d\.]+', net.last_accuracy )[0])
        # try:
        #     last_acc = float(re.findall(r'[\d\.]+', list(map(lambda x: x['accuracy'], history))[-1])[0])
        # except Exception as e:
        #     last_acc = 0

        # state = 'улучшилось!'

        # if current_acc > last_acc:
        #     state = 'улучшилось!'
        #     history.append({
        #         'date': str(datetime.datetime.today()),
        #         'accuracy': net.last_accuracy
        #     })
        #     with open('history.json', 'w+', encoding='utf-8') as h:
        #         h.write(json.dumps(history, indent=4))
        # elif current_acc == last_acc:
        #     state = 'не изменилось!'
        # else:
        #     state = 'ухудшилось!'


        # with pywebio.output.use_scope('network_test', clear=True):
        #     pywebio.output.put_text(f'Метрика: {net.last_accuracy}, {state}')
        #     pywebio.output.put_text(f'Кол-во совпадений: {count}, {percent:.3f}%')
        #     pywebio.output.put_text(desc)
        #     pywebio.output.put_grid([
        #         [pywebio.output.put_text(f'Должно быть ({_img}.png)'), pywebio.output.put_text(f'Получается ({img_src}.png)')],
        #         [pywebio.output.put_image(src=Image.open(f'train_dataset_train/train/{_img}.png')), (pywebio.output.put_text(f'Not found image "{img_src}.png"!') if img is None else pywebio.output.put_image(src=img))]
        #     ])

    # pywebio.output.put_row([
    #     pywebio.output.put_button('Начать!', onclick=b2), pywebio.output.put_button('Сохранить', onclick=net.save), pywebio.output.put_button('Создать решение', onclick=make_solutions)
    # ], size='100px 120px')
    # b2()


if __name__ == '__main__':
    os.system('cls||clear')
    pywebio.start_server(main, port=8080, debug=True)
