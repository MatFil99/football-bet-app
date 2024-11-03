# it creates container bet-c-pg and bet_pg volume that is used as storage
docker run -d \
        --name bet-c-pg \
        -e POSTGRES_PASSWORD=admin \
        -e POSTGRES_USER=pgadmin \
        -v bet_pg:/var/lib/postgresql/data \
        -e POSTGRES_DB=betdb \
-p 5432:5432 \
postgres
