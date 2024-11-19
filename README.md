В файле `utils.py` реализован клиент, который является оберткой над github api клиентом и позволяет собирать информацию об issue и прилинкованных к ним pull requests.  
В файле `test_notebook.ipynb` приведен простой пример использования клиента.  
В файле `example.json` приведен пример результата поиска связанных issue и pull requests.  
Формат результата:
```
{
    "repo_1_full_name": [
        {
            "issue": issue number,
            "pull requests": [
                pull_1 number,
                pull_2 number,
                ...
            ]
        }
    ]
}
```
Для использования необходимо установить в файле `.env` переменную `GITHUB_ACCESS_TOKEN` - это access token для github, нужен, чтобы иметь нормальную квоту на отправку запросов по github api (без авторизации квота быстро кончается)