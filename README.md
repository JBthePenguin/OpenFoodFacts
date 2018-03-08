# OpenFoodFacts  *Python application*\*
**This application gets back the data proposed by the [OpenFoodFacts API](https://en.wiki.openfoodfacts.org/API) to build a database on your localhost and to use it later when you want to find a better product for your health than the one that you planned to eat (or drink).
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
\**new db is coming, [a dump with data for Category](https://drive.google.com/open?id=1e9osRfSo7x2igyE0Ttd_69qV3lOB_zyD)*
##### Download the dump file *[here ( 32.1 MB )](https://drive.google.com/open?id=1xdT9koEhS_lv95WpbP1ts1WLP43ueuwB)*.
##### Create the tables with data.
Inside the same directory of the dump file:
```sh
$ mysql -u OpenFoodFactsApp -p db_openfoodfacts < dump_full_db_off_080318.sql
Enter password: BonAppetit
```
The installed database was created on *March 8st 2018* and contains 71847 products listed in 3422 categories and under categories, 22 levels hierarchy.
If you want an updated database, you have to choice
#### 4.2. *the longer one : using the Python script*
\* a new script to insert data only in Category -> [insert_category_data.py](/database/insert_category_data.py)
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
##### Insert data in Table Category.
```sh
(env)$ python database/insert_category_data.py
```
##### Insert data in Tables Product and CategoryProduct.
```sh
(env)$ python database/insert_product_data.py
```
![insert data](/screenshots/insert_data.png)
The [OpenFoodFacts API](https://en.wiki.openfoodfacts.org/API) proposes more than 10000 pages, each of them containing the characteristics of 20 products, that thus takes some time.
### NOW, the database is ready !!!
## USE OpenFoodFacts *Python application*
*If you used the dump file*, you have to create a virtual environment for Python with virtualenv (*!!!maybe you have to install virtualenv!!!*), use it and install requirements.
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
#### 2.1 Search a substitute.
##### 2.1.1 Choose one of the main category in the list
![list main categoiries](/screenshots/main_categories_1.png)
#### ...
![list main categoiries](/screenshots/main_categories_2.png)

Select the category that you want to search with the number.
![list down categoiries](/screenshots/down_cat_prod.png)
#### ...
![list product](/screenshots/product_1.png)
Choice B: here you can choose to go in a down category, or come back to the main menu, OR ...
##### 2.1.2 Choose a product
![list product](/screenshots/product_2.png)

Select the product that you want to find a substitute. The application display all informations on it...
![product infos](/screenshots/product_info.png)
### COMING SOON
![coming soon](/screenshots/coming_soon.png)
... and found one subsitute before displaying all information.
![substitute infos](/screenshots/subsitute_info.png)
Go to buy it, for sure it's a good product for the healthy.
##### 2.1.3 Choice C: after eating, if you are not sick, you can save the association product/substitute.
![favorite input](/screenshots/favorite_input.png)
Select 1 to save the association product/substitut in your favorites.
![favorite msg](/screenshots/favorite_msg.png)
#### 2.2 Search in yours favorites. 
![list favorite](/screenshots/list_favorite.png)
Select a Favorite in the list.
![display favorite](/screenshots/display_favorite.png)
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
