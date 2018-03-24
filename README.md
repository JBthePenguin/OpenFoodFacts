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
##### Download the dump file with full data *[here ( 32MB )](https://drive.google.com/open?id=1m7l86H7eHp3zx_p3BML7K86BKai-cpew)*.
##### Create the tables with data.
Inside the same directory of the dump file:
```sh
$ mysql -u OpenFoodFactsApp -p db_openfoodfacts < dump_full_db_off_110318.sql
Enter password: BonAppetit
```
The installed database was created on *March 11st 2018* and contains 71237 products listed in 8983 categories ( one category can have many levels hierarchy).

![count row](/screenshots/count_row.png)

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
\* you can also insert_data.py to insert all in one time, but it can very very,... long.
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
#### 2.1 Search a substitute. *tape 1*
##### 2.1.1 Choose one of the main category in the list
![list main categoiries](/screenshots/main_categories_1.png)

Select the category that you want to search with the number... 
![list down categoiries](/screenshots/down_cat_prod.png)
### ....
![list product](/screenshots/product_1.png)

**Choice B**: here you can choose to go in a down or up category, come back to the main menu, see all products without down categories or directly see all the products inside this category. I think it's better to go first in some down categories before selecting a product, but you can do what you want at this step !!!
![list product](/screenshots/product_2.png)
##### 2.1.2 Choose a product
![choose product](/screenshots/choose_prod.png)

Select the product that you want to find a substitute. The application display all informations on it and found substitutes with a better Nutri-Score -> A

![product infos](/screenshots/product_info.png)
## Now you can select the substitute that you prefer and all informations on it are displaying.

![substitute infos](/screenshots/substitute_info.png)

Go to buy it, for sure it's a good product for the healthy.
##### 2.1.3 Choice C: after eating, if you are not sick, you can save the association product/substitute in your Favorites.
Select 1 to save the association product/substitut in your favorites.
![favorite input msg](/screenshots/favorite.png)
#### 2.2 Search in yours favorites. *tape 2* 
![list favorite](/screenshots/list_favorite.png)
This is a list of yours favorites. You can choose to check one (when, where you want) or delete one.\
Tape 1 and choose which one you want to see the description.
![list favorite](/screenshots/favorite_info.png)

### Bye !!!!!
![bye](/screenshots/bye.png)

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
:metal: If you want the inverse mode, if you want to eat something bad for you, just change "a" by "e" in off_class/product.py
* *line 105*
```python
                        if product_ng[0].lower() == "a":
``