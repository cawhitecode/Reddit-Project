Chris White</br>
Reddit-Project</br>
</br>
This project is to practice Python, PostgreSQL, and Data Analytics.
</br></br>
Use Reddit API to gather information then use it gage engagement</br>
You'll need:</br>
PuTTy - https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html</br>
PGadmin4 </br>
Reddit API account/PRAW</br>
psycopg2</br>
BlockingScheduler(if you want data to pull at set times)</br>
</br>
I'm using a PostgreSQL database, but if you want to use another SQL just change out psycopg2 for the corresponding library import. </br>
</br>
How to install/use - Windows </br>
1. Setup a server - I used DigitalOcean.com - the server does have to support the database language you choose(SQL)</br>
2. Install PuTTy - type in your host name/address = I.P. address of server, port 22</br>
3. When logged in on Ubuntu type "adduser *yourname*" without quotes then "usermod -aG sudo *yourname*" **yourname is whatever you want it to be**</br>
4. command list:</br>
*python3*</br>
sudo apt-get update</br>
sudo apt-get install mc</br>
sudo apt-get -y install python3-pip</br>
sudo apt-get -y install python3-dev</br>
sudo -H pip3 install --upgrade pip</br>
sudo apt-get install postgresql postgresql-contrib  **note this changes if you want to a different use a different SQL language**</br>
sudo -i -u postgres</br>
CREATE USER **yourname** WITH PASSWORD **'yourpassword'**</br>
sudo -i -u root</br>
5. Open PGadmin4 using **yourname** as User name and **yourpassword** as password</br>
keep in mind that your server may not be listening to your program.</br>
6. Don't forget to install PRAW, Psycopg2, and BlockingScheduler</br>
7. Open and save both files. Reddit.py is the initial setup for making the table and pulling the data. Reddit_pull.py pulls the data continously</br>
