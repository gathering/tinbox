![tinbox logo](https://github.com/gathering/tinbox/blob/main/static/tinbox.png?raw=true)

# tinbox

tinbox is a small Django-based application that creates slideshows in the web browser. It was created for The Gathering, but can be used by anyone.

# Setup

The best way to go about this is to use Docker. Pull this repo, then run:

```
docker-compose up -d --build
docker-compose exec app python3 manage.py migrate
```

After this, you might want to create a user for logging in:

```
docker-compose exec app python3 manage.py createsuperuser
```

This user can be used to login in the admin panel, here: `/admin`

