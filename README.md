1. Create a directory for the code to be run out of.

2. Setup a virtual environment for flask to run in. Do this by installing flask using "py -3 -m venv .venv"

3. Activate the venv using ".venv\Scripts\activate"

4. Install flask in the venv using "$ pip install Flask"

5. This was made using python version 3.12.0 and flask version 3.0.0. If there are any problems with running the website, ensure you are running these versions with "python --version" and "flask --version"

6. In oredr to ensure the code is running as it should, you also need to install pytest using "pip install pytest" in the terminal
    6.1. To test the user database code works as intended, run "userTest.py"
    6.2. To test the product database code works as intended, run "productTest.py"

7. Run "flaskStuff.py" to start the website, and then go to the link it provides in the terminal - likely "127.0.0.1:5000" - to use it.

## Account Login Info ##
Admin user: admin@admin.com
Admin pass: password

Apple (seller) user: admin@apple.com
Apple (seller) pass: apple

User user: fordhammax@gmail.com
User pass: password