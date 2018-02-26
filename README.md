# Portofino-Labs

Take home assignment for Portofino Labs.

Just wanted to disclose starting ahead I pretty much got most of the code for this project straight out of the docs for 
[Docker Compose](https://docs.docker.com/compose/gettingstarted/) and a bit from a [Flask authetication snippet](http://flask.pocoo.org/snippets/8/). The REST API is all Python but the total amounts of original JS code is higher.

Also just a comment on something I think might have been a bit misleading is the diagram:

![Diagram](https://i.imgur.com/baTHtH9.png)

It shows nginx communicating directly with the REST API but the specs say

>Create a static, Nginx served page

If it's static it wouldn't be able to communicate directly; ie it's still the internal client which is requesting the REST API via ajax. In practice nginx is actively proxying requests for REST APIs so the diagram still does work in isolation. :)

I'm probably thinking about this too much.

Anway, the default access for the logs page is
>http://localhost/logs.html

I'm using port 80 for the GUI and 5000 for the API; feel free to change the mappings in docker-compose.yml
