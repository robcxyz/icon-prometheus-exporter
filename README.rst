===========================================

## ICON - exporter agent for icon blockchain:
----------------

This is a python agent that extracts metric form ICON-nodes through provided rpcs. just clone and run the python agent on your server. The metrics are exported on port 6100 that need to be configured on prometheus server.

To install the icon-prometheus-exporter package.

.. code-block:: bash
sudo apt-get install python-pip python-dev build-essential
sudo pip install virtualenv
sudo pip install  virtaulenvwrapper

mkdir ~/.virtualenvs

    cd icon-prometheus-exporter
    python setup.py install

you can use the [prometheus server](https://github.com/ghalwash/terransible-aws-ec2-prometheus) to show the extracted data in grafana dashboards

## sample output:
----------------
## Infrastructure
![GitHub Logo](https://github.com/ghalwash/icon-prometheus-exporter/blob/master/Screenshot%20from%202020-06-17%2018-26-56.png)
