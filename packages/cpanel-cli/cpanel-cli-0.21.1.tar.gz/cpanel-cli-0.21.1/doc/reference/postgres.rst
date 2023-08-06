..
   Do not edit this .rst file directly — it’s generated programmatically.
   See doc/reference.sh.

==================================================
Module: ``postgres``
==================================================

`Leer en español </es/latest/reference/postgres.html>`_

- **create postgres user USERNAME PASSWORD**
- **list postgres users**
- **rename postgres user OLDUSERNAME NEWUSERNAME NEWPASSWORD**
- **set postgres password USERNAME NEWPASSWORD**
- **delete postgres user USERNAME**
- **create postgres database DBNAME**
- **list postgres databases**
- **rename postgres database OLDDBNAME NEWDBNAME**
- **delete postgres database DBNAME**

**COMMANDS**


**create postgres user USERNAME PASSWORD**

Create a new PostgreSQL user with USERNAME and PASSWORD.

*Example*

.. code:: sh

    $ cpanel create postgres user "scott" 'tiger'

**list postgres users**

List all PostgreSQL users associated to the cPanel account.

*Example*

.. code:: sh

    $ cpanel list postgres users

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/Postgresql::list_users/

**rename postgres user OLDUSERNAME NEWUSERNAME NEWPASSWORD**

Rename PostgreSQL user from OLDUSERNAME to NEWUSERNAME with NEWPASSWORD.

*Example*

.. code:: sh

    $ cpanel rename postgres user "scott" "larry" 'tiger'

**set postgres password USERNAME NEWPASSWORD**

Change the password for PostgreSQL user USERNAME to NEWPASSWORD.

*Example*

.. code:: sh

    $ cpanel set postgres password "scott" 'panther'

**delete postgres user USERNAME**

Delete PostgreSQL user USERNAME.

*Example*

.. code:: sh

    $ cpanel delete postgres user "scott"

**create postgres database DBNAME**

Create a new PostgreSQL database with name DBNAME.

*Example*

.. code:: sh

    $ cpanel create postgres database 'northwind'

**list postgres databases**

List existing PostgreSQL databases.

*Example*

.. code:: sh

    $ cpanel list postgres databases

See a sample of the JSON result data at:
https://api.docs.cpanel.net/openapi/cpanel/operation/Postgresql-list_databases/

**rename postgres database OLDDBNAME NEWDBNAME**

Rename PostgreSQL database from OLDDBNAME to NEWDBNAME.

*Example*

.. code:: sh

    $ cpanel rename postgres database 'northwind' 'southgale'

**delete postgres database DBNAME**

Delete PostgreSQL database named DBNAME.

*Example*

.. code:: sh

    $ cpanel delete postgres database 'northwind'

