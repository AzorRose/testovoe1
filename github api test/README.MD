Инструкция по запуску: 
1. Скачать и установить Python версии не ниже 3.10
2. Создать файл .env и добавить следующие переменные:
  GITHUB_USER=
  GITHUB_TOKEN=
  REPO_NAME=
В переменную GITHUB_USER необходимо вписать ваше имя пользователя в github, в REPO_NAME - название репозитория, который будет создаваться для тестирования,
в GITHUB_TOKEN - ваш токен для работы с гитхаб. Чтобы его получить необходимо зайти в Settings -> Developer Settings ->  Personal access tokens -> Tokens (classic) 
и нажать на кнопку Generate New Token (classic). Необходимо задать описание токена и установить галочки в
полях repo и delete_repo и нажать Generate token.
3. Запустить скрипт start_test.sh

Для выполнения требуется подключение к интернету
