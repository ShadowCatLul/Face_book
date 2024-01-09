# Сервис микроблогов на подобие Твиттера

## Архитектура:
![Диаграмма без названия drawio](https://github.com/ShadowCatLul/Twitterbook/assets/64269779/8ca23c60-b5c2-428d-bcf5-5309a5279cff)

##Сущности
- Пользователь
  - id
  - username  
  - tweets (id твитов)
- Твит
  - id - id самого твита
  - user_id
  - content - содержимое
## Основные функции

Root (ping)

![image](https://github.com/ShadowCatLul/Twitterbook/assets/64269779/77ec670c-a075-42a5-94c5-7daf790d66b1)


Get-all-users
![image](https://github.com/ShadowCatLul/Twitterbook/assets/64269779/2e83a27c-07d2-447e-99b5-6cf8906491c9)



Get-all-tweets
![image](https://github.com/ShadowCatLul/Twitterbook/assets/64269779/cae9fc9a-279e-4e8f-a6b3-b82880a96cf4)


Debug
![image](https://github.com/ShadowCatLul/Twitterbook/assets/64269779/80e06247-b764-4681-9ddd-30c1a3af2a9c)


Get-by-name
![image](https://github.com/ShadowCatLul/Twitterbook/assets/64269779/8e01d299-5797-424c-89ed-daa52fdad40b)


Add user
![image](https://github.com/ShadowCatLul/Twitterbook/assets/64269779/1a99c751-5207-475b-8a56-56cd782f5a3e)



Также присутствуют функции добавления твита, обновления пользователя и твита и их удаления
