# reversi Project by parsa
# Version History

## [1.1.0] - 2024-10-02
### Added
- Show correct cells after losing in hard mode.
- Add different difficulties and different time limits.
- Added  CSS for responsive styling.

### Changed
- Use ORM for game object.
- add custom logics to game like timer .

### Fixed
- Corrected an issue with overing game.
- Fixed a bug where user profiles were not being saved properly.

---

## [1.0.0] - 2024-10-01
### Initial Release
- Basic project setup with Django.
- Play game on one device .


A project with Django and Bootstarp technologies.

<br>
<h2>How to Run? </h2>
<br>

<h2>
  Create a new virtual environment and activate it.
</h2>

<h3>on Windows:</h3>
<div class="highlight highlight-source-shell">

  ```
  $ pip install virtualenv
  ```
  <br>
  
  ```
  $ virtualenv your_virtualenv_name
  ```
</div>


<h3>on Linux:</h3>
<div class="highlight highlight-source-shell">

  ```
  $ sudo apt-get install python-pip
  ```
  <br>
  
  ```
  $ pip install virtualenv
  ```
  <br>
  
  ```
  $ virtualenv your_virtualenv_name
  ```
</div>

<br>

<h2>
  Set all required environment variables:
</h2>

<h3>Example on Windows:</h3>
<div class="highlight highlight-source-shell">

  ```
  $ set SECRET_KEY=abbass
  ```
</div>

<h3>Example on Linux:</h3>
<div class="highlight highlight-source-shell">

  ```
  $ export SECRET_KEY=abbass
  ```
</div>
<br>

<h2>
  Install the dependencies:
</h2>
<div class="highlight highlight-source-shell">

  ```
  $ pip install -r requirements.txt
  ```
</div>
<br>

<h2>
  Create and migrate the database:
</h2>
<div class="highlight highlight-source-shell">

  ```
  $ python manage.py migrate
  ```
</div>
<br>

<h2>
  Create a new superuser:
</h2>
<div class="highlight highlight-source-shell">

  ```
  $ python manage.py createsuperuser
  ```
</div>
<br>

<h2>
  Collect static files:
</h2>
<div class="highlight highlight-source-shell">

  ```
  $ python manage.py collectstatic
  ```
</div>
<br>

<h2>
  Run the server on default port 8000:
</h2>
<div class="highlight highlight-source-shell">

  ```
  $ python manage.py runserver
  ```
</div>
<br>

<h2>
  Run quickly on windows (after activate virtualenv):
</h2>
<div class="highlight highlight-source-shell">

  ```
  $ win-run.cmd
  ```
</div>
<br>

<h2>
  Run quickly on Linux or macOS:
</h2>
<div class="highlight highlight-source-shell">

  ```
  $ source run.py
  ```
</div>
<br>

<h2>
  Enjoy it :)
</h2>
