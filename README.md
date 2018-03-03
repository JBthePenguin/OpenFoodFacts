# OpenFoodFacts  *Python application*\*
**This application gets back the data proposed by the [OpenFoodFacts API](https://en.wiki.openfoodfacts.org/API) to build a database on your localhost and to use it later when you want to find a better product for your health than the one that you planned to eat (or to drink).
So, to stay healthy, *download the directory OpenFoodFacts* and ...**
## CREATE DATABASE *only before the first using*: 
To create the following database, [MySQL](https://dev.mysql.com/doc/refman/5.7/en/installing.html) or [MariaDB](https://mariadb.com/kb/en/library/getting-installing-and-upgrading-mariadb/) must be installed on your host.
![DB structure](/screenshots/db_structure.png)

### 1. *Connect to your MySQL Client with root account:*
```sh
$ sudo su
$ service mysql start
$ mysql
```
### 2. *Create database db_openfoodfacts:*
```sql
CREATE DATABASE db_openfoodfacts;
```
### 3. *Create a new user OpenFoodFactsApp with all privileges on db_openfoodfacts*
```sql
CREATE USER 'OpenFoodFactsApp'@'localhost' IDENTIFIED BY 'BonAppetit';
GRANT ALL ON db_openfoodfacts.* TO 'OpenFoodFactsApp'@'localhost';
exit;
```
### 4. *Create the tables and Insert data from [OpenFoodFacts API](https://en.wiki.openfoodfacts.org/API)*
At this point, you have two possibilities:
#### 4.1. *the faster one: using the dump file*
##### Download the dump file *[here ( 32.1 MB )](https://drive.google.com/open?id=1Va_58Wm6qBpvdTZ6_DD9U4pjeHYhOB2A)*.
##### Create the tables with data.
Inside the same directory of the dump file:
```sh
$ mysql -u OpenFoodFactsApp -p db_openfoodfacts < create_tables_dump_010318.sql
Enter password: BonAppetit
```
The installed database was created on *March 1st 2018* and contains 71237 products listed in 8983 categories and under categories.
If you want an updated database, you have to choice
#### 4.2. *the longer one : using the Python script*
##### Create the tables.
```sh
$ cd OpenFoodFacts
$ mysql -u OpenFoodFactsApp -p db_openfoodfacts < database/create_tables.sql
Enter password: BonAppetit
```
##### Create a virtual environment for Python with virtualenv (*!!!maybe you have to install virtualenv!!!*) and use it.
```sh
$ virtualenv -p python3 env
$ source env/bin/activate
```
##### Install all necessary modules ([requests](http://docs.python-requests.org/en/master/), [mysql.connector](https://dev.mysql.com/doc/connector-python/en/)).
```sh
(env)$ pip install -r requirements.txt
```
##### Insert data.
```sh
(env)$ python database/insert_data.py
```
![insert data screenshot](/screenshots/insert_data.png)
The [OpenFoodFacts API](https://en.wiki.openfoodfacts.org/API) proposes more than 10000 pages, each of them containing the characteristics of 20 products, that thus takes some time.
### NOW, the database is ready !!!
## USE OpenFoodFacts *Python application*
*If you use the dump file*, you have to create a virtual environment for Python with virtualenv (*!!!maybe you have to install virtualenv!!!*), use it and install requirements.
```sh
$ cd OpenFoodFacts
$ virtualenv -p python3 env
$ source env/bin/activate
(env)$ pip install -r requirements.txt 
```
### 1.Launch application.
```sh
(env)$ python .
```
### 2. Choice A : Search a substitute or search in yours favorites:
![welcome and choice A](/screenshots/welcome.png)
#### 2.1 *COMING SOON* ---> Search a substitute.
![I coming soon](/screenshots/coming_soon.png)
##### 2.1.1 Choose a category
##### 2.1.2 Choose a product and go to buy the substitute that founded by the application, for sure it's a good product for the healthy.
##### 2.1.3 After eating, if you are not sick, you can save the association product/substitute
#### 2.2 Search in yours favorites. 
\* The default language setting is french, if you want to change with an [other available language](https://en.wiki.openfoodfacts.org/API#Languages), it's necessary, at step 4.2, modify in **insert_data.py** : 

* *line 29*
```python
        name = product_off["product_name_fr"]
```
* *line 35*
```python
        nutrition_grade = product_off["nutrition_grade_fr"]
```
* *line 45*
```python
        description = product_off["ingredients_text_fr"]
```
* *line 58*
```python
URL = "http://fr.openfoodfacts.org/language/francais/"
```
