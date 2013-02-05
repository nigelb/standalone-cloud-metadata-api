# standalone-cloud-metadata-api

A standalone implementation of some cloud metadata APIs to test VM images against.
Note that it is not a complete implementation of the API, at this time.



# Apache

### Apache vhost config

    <VirtualHost 169.254.169.254:80>

        ServerName 169.254.169.254
        ScriptAliasMatch ^/+openstack(.*) "/var/www/169.254.169.254/cgi-bin/openstack_cgi_entrypoint.py"
        ScriptAliasMatch ^/+2009-04-04/+(meta|user)-data(.*) "/var/www/169.254.169.254/cgi-bin/ec2_cgi_entrypoint.py"

        SetEnv SCMA_CONFIG_DIR /etc/apache/scma/

        <Directory "/var/www/169.254.169.254/cgi-bin">
            AllowOverride None
            Options None
            Order allow,deny
            Allow from all
        </Directory>

    </VirtualHost>

## Apache Environment Variables

* `SCMA_ENABLE_CGITB` call cgitb.enable().
* `SCMA_CONFIG_DIR` set the location of the config directory.
* `SCMA_PYTHON_PATH_INCLUDE` if the standalone-cloud-metadata-api module is not in your python's system packages, set this variable to the location of the module.
* `SCMA_CWD_PYTHON_PATH_INCLUDE` if this variable is set to `True` then the current working directory will be set to `SCMA_PYTHON_PATH_INCLUDE`.

# Arping

One of the methods used to get the MAC address of the requesting machine is to use the arping command.
This command uses RAW sockets and usually needs to be run as root, however permissions to use RAW sockets can be granted with the setcap command:

    #root> setcap cap_net_raw+ep `which arping`