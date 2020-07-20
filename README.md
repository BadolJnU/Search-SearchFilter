# Search-SearchFilter

A django based webproject where a user can search by any keyword
-Automatically searches the database as you type the search word.
A django based ajax filter page, without reloading the template.


Tools used:
* Django 3.0.8
* Jquery and Ajax
* bootstrap


Installing
  1. Clone this repository
  2. Inside the root folder, run pipenv install to install dependencies
  3. Run pipenv shell to start working in the virtual environment
  4. Before running ./manage.py runserver, make sure you apply the database migrations (./manage.py migrate)
  
  There are four pages in this project, in home page there is a navbar, where user can signup, login and search a blog post from database by searching a keyword.
  in searchhistory page where filter the search history
  
