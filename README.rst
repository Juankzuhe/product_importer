Product Importer
================

Acme Inc - Product Importer

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style

Settings
--------

Moved to settings_.

.. _settings: http://cookiecutter-django.readthedocs.io/en/latest/settings.html

Basic Commands
--------------

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create an **superuser account**, use this command::

    $ docker-compose -f production.yml run --rm django python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

Type checks
^^^^^^^^^^^

Running type checks with mypy:

::

  $ mypy product_importer

Celery
^^^^^^

This app comes with Celery.

To run a celery worker:

.. code-block:: bash

    cd product_importer
    celery -A config.celery_app worker -l info

Please note: For Celery's import magic to work, it is important *where* the celery commands are run. If you are in the same folder with *manage.py*, you should be right.

Email Server
^^^^^^^^^^^^

In development, it is often nice to be able to see emails that are being sent from your application. For that reason local SMTP server `MailHog`_ with a web interface is available as docker container.

Container mailhog will start automatically when you will run all docker containers.
Please check `cookiecutter-django Docker documentation`_ for more details how to start all containers.

With MailHog running, to view messages that are sent by your application, open your browser and go to ``http://127.0.0.1:8025``

.. _mailhog: https://github.com/mailhog/MailHog

Deployment
----------

The following details how to deploy this application.

Docker
^^^^^^

See detailed `cookiecutter-django Docker documentation`_.

.. _`cookiecutter-django Docker documentation`: http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html

AWS
^^^^^^
.. Create a new instance ec2 _--image-id ubuntu 20.04

aws ec2 run-instances --image-id ami-00399ec92321828f5 --count 1 --instance-type t2.small --key-name product_importer --security-groups my-sg



.. Connect to instance

chmod 400 product_importer.pem

ssh -i /path/to/product_importer.pem ec2-user@ec2-WWW-XXX-YYY-ZZZ.REGION.compute.amazonaws.com

.. Install docker & docker-compose

sudo apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
sudo apt update
apt-cache policy docker-ce
sudo apt install docker-ce
sudo systemctl status docker
sudo usermod -aG docker ${USER}
sudo apt install docker-compose

.. Copy Files to EC2 Instance

cd /path/to/product_importer

rsync -av -e "ssh -i /path/to/product_importer.pem" . ec2-user@ec2-WWW-XXX-YYY-ZZZ.REGION.compute.amazonaws.com:~/app/

.. Deploy changes

ssh -i /path/to/product_importer.pem ec2-user@ec2-WWW-XXX-YYY-ZZZ.REGION.compute.amazonaws.com

cd /app

docker-compose -f production.yml build
docker-compose -f production.yml run --rm django python manage.py migrate
docker-compose -f production.yml up -d
