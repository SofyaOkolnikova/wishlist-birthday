from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os

app = Flask(__name__)
app.secret_key = 'Sofia_top_secret'

# Файл для хранения данных о подарках
DATA_FILE = 'gifts.json'

def load_gifts():
    """Загружаем данные о подарках из JSON файла"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            gifts = json.load(f)
            # Гарантируем, что у каждого подарка есть все необходимые поля
            for gift in gifts:
                if 'reserved_by' not in gift:
                    gift['reserved_by'] = None
            return gifts
    else:
        # Начальные данные
        initial_gifts = [
                {
                "id": 1,
                "name": "Clarins Addition Concentre Eclat Visage",
                "reserved_by": null,
                "url": "https://goldapple.ru/19000000357-addition-concentre-eclat-visage",
                "image": "https://pcdn.goldapple.ru/p/p/19000000357/web/696d67416464335064708ddc4777900d8dafullhd.webp"
            },
            {
                "id": 2,
                "name": "Свободные штаны серо-зелёные (L)",
                "reserved_by": null,
                "url": "https://shuclothes.com/ru/run/run-tights/run-loose-pants-grey-green-25",
                "image": "https://static.shuclothes.com/sig/size:5669/q:100/aHR0cHM6Ly9zaHVjbG90aGVzLmNvbS9zdG9yYWdlLzUxNjI3L3NodV8zLjkuMjU5NjU1OS5qcGc"
            },
            {
                "id": 3,
                "name": "SmoRodina pumpkin enzyme cleanser",
                "reserved_by": null,
                "url": "https://goldapple.ru/19000347141-pumpkin-enzyme-cleanser",
                "image": "https://pcdn.goldapple.ru/p/p/19000347141/web/696d67416464335064708ddc5aa9cb2bf63fullhd.webp"
            },
            {
                "id": 4,
                "name": "Лонг с капюшоном серо-зелёный (L)",
                "reserved_by": null,
                "url": "https://shuclothes.com/ru/run/run-longsleeves/run-hooded-warm-longsleeve-grey-green-25",
                "image": "https://static.shuclothes.com/sig/size:5669/q:100/aHR0cHM6Ly9zaHVjbG90aGVzLmNvbS9zdG9yYWdlLzUxNTkxL3NodV8zLjkuMjU5NjE3NC5qcGc"
            },
            {
                "id": 5,
                "name": "Сертификат в Under by Me",
                "reserved_by": null,
                "url": "https://certificate.underbyme.ru/",
                "image": "https://optim.tildacdn.com/stor3039-3839-4165-a232-356134363961/-/format/webp/72616121.jpg.webp"
            },
            {
                "id": 6,
                "name": "Сертификат в Золотое яблоко",
                "reserved_by": null,
                "url": "https://goldapple.ru/cards",
                "image": "https://pcdn.goldapple.ru/p/g/fg/199/web/35386137666134362d316464352d343330372d613866382d3032646331306165346363328de122858dc4682.webp"
            },
            {
                "id": 7,
                "name": "Сертификат на массаж в Rehab.You",
                "reserved_by": null,
                "url": "https://rehabyou.ru/certificates/",
                "image": "https://rehabyou.ru/wp-content/themes/rehab/assets/images/loyalty-image.png"
            }
        ]
        save_gifts(initial_gifts)
        return initial_gifts

def save_gifts(gifts):
    """Сохраняем данные о подарках в JSON файл"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(gifts, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    """Главная страница с вишлистом"""
    gifts = load_gifts()
    return render_template('index.html', gifts=gifts)

@app.route('/book/<int:gift_id>', methods=['GET', 'POST'])
def book_gift(gift_id):
    """Страница бронирования подарка"""
    gifts = load_gifts()
    gift = next((g for g in gifts if g['id'] == gift_id), None)
    
    if not gift:
        flash('Подарок не найден', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        
        if name and not gift['reserved_by']:
            # Бронируем подарок
            gift['reserved_by'] = name
            save_gifts(gifts)
            
            flash(f'Подарок успешно забронирован за {name}!', 'success')
            return redirect(url_for('index'))
        elif gift['reserved_by']:
            flash('Этот подарок уже забронирован!', 'error')
        elif not name:
            flash('Пожалуйста, введите ваше имя', 'error')
    
    return render_template('booking.html', gift=gift)

@app.route('/cancel/<int:gift_id>')
def cancel_booking(gift_id):
    """Отмена бронирования подарка"""
    gifts = load_gifts()
    gift = next((g for g in gifts if g['id'] == gift_id), None)
    
    if not gift:
        flash('Подарок не найден', 'error')
        return redirect(url_for('index'))
    
    if not gift['reserved_by']:
        flash('Этот подарок еще не забронирован', 'error')
        return redirect(url_for('index'))
    
    # Отменяем бронирование
    previous_owner = gift['reserved_by']
    gift['reserved_by'] = None
    save_gifts(gifts)
    
    flash(f'Бронирование от {previous_owner} отменено! Подарок снова доступен.', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
