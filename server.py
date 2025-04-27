import asyncio
import os

# Константы
HOST = '127.0.0.1'  # Локальный адрес
PORT = 8080         # Порт сервера
WEB_ROOT = './'     # Директория для хостинга файлов

# Кэш для загруженных файлов
file_cache = {}

# Загрузка файла в память
def load_file(file_path):
    if file_path in file_cache:
        return file_cache[file_path]
    try:
        with open(file_path, 'rb') as file:
            content = file.read()
            file_cache[file_path] = content
            return content
    except FileNotFoundError:
        return None

# Формирование HTTP-ответа
def create_response(status_code, content, content_type="text/html"):
    headers = f"HTTP/1.1 {status_code}\r\n"
    headers += f"Content-Type: {content_type}\r\n"
    headers += f"Content-Length: {len(content)}\r\n\r\n"
    return headers.encode('utf-8') + content

# Обработка клиента
async def handle_client(reader, writer):
    try:
        # Чтение данных от клиента
        request_data = await reader.read(1024)
        request_text = request_data.decode('utf-8')
        print(f"Received request:\n{request_text}")

        # Парсим HTTP-запрос
        request_lines = request_text.split("\r\n")
        request_line = request_lines[0]
        method, path, _ = request_line.split(" ")

        # Определяем путь к файлу
        if path == '/':
            path = '/index.html'
        file_path = WEB_ROOT + path

        # Получаем содержимое файла
        file_content = load_file(file_path)

        if file_content:
            response = create_response("200 OK", file_content)
        else:
            error_content = b"<html><body><h1>404 Not Found</h1></body></html>"
            response = create_response("404 Not Found", error_content)

        # Отправляем ответ клиенту
        writer.write(response)
        await writer.drain()
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        # Закрываем соединение
        writer.close()
        await writer.wait_closed()

# Основная функция сервера
async def main():
    server = await asyncio.start_server(handle_client, HOST, PORT)
    print(f"Server is listening on http://{HOST}:{PORT}")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())