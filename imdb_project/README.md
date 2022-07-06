<h1 align="center">Movie pipeline project</h1>
<hr style="border:2px solid black">
<h2 align="center">General information</h2>
<p>This project can be treated as app, that is used for collecting films data.</p>
<p>It uses TMDB database as first major source of data (for more detailed information look here: <a href="https://developers.themoviedb.org">themoviedb</a></p>
<p>On the other hand, TMDB data is not completely full as it does not include needed information
, like number of voter for films or average rating. This information is necessary in case we 
want to display some charts in Metabase service, based on this data.</p>
<p>Therefore, this app uses IMDB database for extracting such an indispensable information,
(files are taken from <a href="https://datasets.imdbws.com/">here</a>.</p>
<hr style="border:2px solid black">
<h2 align="center">Main components</h2>
<ul>
<li><h4>Airflow dev kit (including webserver, scheduler and db) - orchestrates data pipeline</h4></li>
<li><h4>Pyspark - used for manipulating vast volumes of provided data</h4></li>
<li><h4>PostgreSQL - used for storing resulting data as well as making charts in Metabase</h4></li>
<li><h4>S3(minio) - AWS cloud storage used as a mediator-storage for raw data on it`s way to constant storing in postgres DB</h4></li>
<li><h4>Metabase - service for visualizing and analyzing data stored in Postgres DB</h4></li>
</ul>
<hr style="border:2px solid black">
<h2 align="center">Usage</h2>
<p>According to the main idea of containerized application,
in order to run this app you need to install docker and docker-compose.</p>
<h5>TO LAUNCH LOCALLY</h5>
<p>Just cd in working directory(imdb_project) and use:</p><p><b>sudo docker-compose up -d --build</b></p>
<p>This command will initiate raising all necessary containers and setting up environment for them</p>
<p><b>Note</b>, that docker-compose.yml file won't up without not only Dockerfile, but also entrypoint.sh and .env files</p>
<p>After this you can go to <a href="http://localhost:3001">http://localhost:3001</a>
and make necessary charts, diagrams etc.</p> 
<p><b>Keep in mind</b>, that you can also use python scripts provided separately without airflow,
for this you should replace every usage "s3" and "database" to "localhost", however I wouldn't recommend 
doing it because of ease in manipulating your workflow via Airflow.</p>
<p><b>PS.</b> you can change default environment variables if you want to:)</p>
<hr style="border:2px solid black">
<h2 align="center">Airflow examples of correct running</h2>

![image](https://user-images.githubusercontent.com/99387760/174488986-4307a9a7-2c0b-4df8-a04e-f4e5861bd82e.png)
<p>Note,that dags are scheduled for 1:00 AM to save all data from the previous day</p>
<hr style="border:2px solid black">
<h2 align="center">Examples of Metabase usage</h2>

![image](https://user-images.githubusercontent.com/99387760/174486189-2c708869-f863-44b6-a856-78cce3b11dd5.png)

![image](https://user-images.githubusercontent.com/99387760/174486510-fc2deaf0-4c05-42e0-b705-6987d4c8bb4d.png)

![image](https://user-images.githubusercontent.com/99387760/174486525-ccef751d-b328-4555-9e53-3b19dd5d43d7.png)

![image](https://user-images.githubusercontent.com/99387760/174486532-b72c80b8-22cd-4c46-b9dc-fd2434bf0731.png)

![image](https://user-images.githubusercontent.com/99387760/174486552-d3bbf49c-4217-4b9a-b8c0-7d89b5d0ab11.png)
