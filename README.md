# FastAPI-Voting [Interactive Demo](https://www.asico1116.com/docs)
## Use devcontainer (Recommended)
1. Clone this repo.

2. Set the environment variables and secrets for PostgreSQL, and save as `.env` in the folder.

   ```shell
   DATABASE_USERNAME=postgres
   DATABASE_PASSWORD=postgres
   DATABASE_HOSTNAME=db
   DATABASE_PORT=5432
   DATABASE_NAME=postgres
   SECRET_KEY=STRING_TO_ENCRYPT_JWT
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=60
   ```

3. Use the devcontainer to open the API server.

   - Install [Docker](https://www.docker.com/), VSCode extensions [Remote Development](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack) and [Docker](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker).
   - Open the repo folder in VSCode.
   - Open the command palette (ctrl + shift + p) and choose `Dev Containers: Rebuild and Reopen in Container`.
   - Use `F5` to run the API server and it runs on `http://localhost:8000/docs`.

4. Run 

   ```cmd
   docker exec -it <postgresql_container_id> bash
   ```

   to inspect the postgresql

---

## Install locally

1. Clone this repo.

2. Set the environment variables and secrets for PostgreSQL, and save as `.env` in the folder. (see above)

3. Install [Python](https://www.python.org/), [Docker](https://www.docker.com/) and [PostgreSQL](https://www.postgresql.org/).

4. Install dependencies.
    ```cmd
    pip install -r requirements.txt
    ```

5. Run

    ```cmd
    uvicorn app.main:app --reload
    ```

    to open the API server and it runs on `http://localhost:8000/docs`.

