# Laboratório 9.6 — FastAPI, Docker e Deploy

Engenharia de Software · API FastAPI em container Docker, publicada no Azure App Service (plano Free F1)
com CI/CD pelo GitHub Actions.

**Aplicação online:** <https://lab096-gmarinho-hacfekbzf9e5drg6.brazilsouth-01.azurewebsites.net>
(documentação interativa em [`/docs`](https://lab096-gmarinho-hacfekbzf9e5drg6.brazilsouth-01.azurewebsites.net/docs))

## Passos

1. API RESTful em FastAPI: [`main.py`](main.py), CRUD de itens em `/items`.
2. Imagem Docker: [`Dockerfile`](Dockerfile) (`python:3.14-slim`, Uvicorn na porta 80) e
   [`.dockerignore`](.dockerignore).
3. e 4. Rodar localmente e testar com o Postman:

   ```bash
   docker build -t lab09-fastapi .
   docker run --rm -p 8000:80 lab09-fastapi
   ```

   Acesse <http://127.0.0.1:8000/items>. A coleção do [9.5](https://github.com/gabrielmarinhorosa/Lab_09.5_EngSoft)
   testa exatamente essa porta.
5. Ambiente no App Service: Web App Linux para container, plano F1, região Brazil South. O container `main`
   roda a imagem pública `gmarinhoo/lab09-fastapi:latest` do Docker Hub, porta 80.
6. A página `/` responde com o nome da API e o commit que gerou a imagem.
7. CI/CD: [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml). A cada push na `main`, o workflow:
   1. constrói a imagem;
   2. publica no Docker Hub com as tags `latest` e o sha do commit;
   3. chama o webhook de deploy contínuo do App Service, que baixa a imagem nova e reinicia o container.

   Secrets usados: `DOCKERHUB_TOKEN` (token do Docker Hub) e `AZURE_WEBAPP_WEBHOOK_URL` (webhook do Centro de
   Implantação). O modo sidecar do App Service não oferece GitHub Actions no Centro de Implantação, por isso o
   workflow foi escrito à mão e usa o webhook.
8. Deploy automático: o commit `f3a00e4` fez a página `/` passar a mostrar
   `"version": "f3a00e4f62670fe5de31c4cc8ce3daad9b9ec9cb"`, sem nenhum passo manual depois do push.
9. [Coleção do Postman](https://go.postman.co/collection/52575572-b12e3ee0-4429-489e-b0ae-d4417f617b1d)
   (cópia em [`postman/`](postman/lab_09_6_fastapi_azure.postman_collection.json)). Rodada duas vezes contra a
   aplicação online: 14 requisições, 23 asserções, nenhuma falha.

| Método | Rota | Sucesso | Erros |
|---|---|---|---|
| GET | `/items` | 200 | |
| GET | `/items/{id}` | 200 | 404 |
| POST | `/items` | 201 | 422 |
| PUT | `/items/{id}` | 200 | 404, 422 |
| DELETE | `/items/{id}` | 200 | 404 |

Os itens ficam em memória: a lista volta aos dois itens iniciais quando o container reinicia.
