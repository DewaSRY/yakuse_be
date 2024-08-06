# Docker Info

## to set up mysql on docker

1. run your local docker first.<br/>this stape make sure your docker demon running<br/>and ready to run mysql image
2. run shel command `docker-compose up --watch -d`<br/>to make this stape works you need run the command on the work
   directory<br/>which the docker compose file ("compose.yml")file on the root.<br/> this stape use to running the mysql
   image on background.
3. after all stape above you already can access the mysql database

```mermaid
flowchart LR
    markdown["`This **is** _Markdown_`"]
    newLines["`Line1
    Line 2
    Line 3`"]
    markdown --> newLines
```