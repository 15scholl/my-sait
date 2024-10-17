from flask import Flask, request, jsonify
from googlesearch import search
import requests
from bs4 import BeautifulSoup
import html

app = Flask(__name__)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data['question']
    
    # Поиск через Google (берем 3 первых результата)
    search_results = search(question, num_results=3)
    
    answers = []
    
    for url in search_results:
        try:
            # Отправляем запрос к каждой найденной странице
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Пробуем найти заголовки и абзацы на странице
            paragraphs = soup.find_all('p')
            
            # Собираем текст первых абзацев
            content = ' '.join([para.get_text() for para in paragraphs[:3]])
            
            # Добавляем текстовое содержимое как ответ
            if content:
                answers.append(content)
            else:
                answers.append(f"Не удалось извлечь текст из {url}")
        
        except Exception as e:
            answers.append(f"Ошибка при обработке URL {url}: {str(e)}")
    
    # Возвращаем объединенный текст ответов
    return jsonify({'answer': ' '.join(answers)})

if __name__ == '__main__':
    app.run(debug=True)
