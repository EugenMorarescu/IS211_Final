# IS211_Final
This is my Final Project for class IS211. This is a web app which allows users to add, delete, and update posts to a blog.
I have included a table in my database to keep track of usernames and password accordingly. When a user logs in a session
is created and that user stays logged in until they click "Log out". I have made sure that duplicate entries are not
possible in the database to avoid different people using the same username. I made it so that when a user attempts to
log in, the username is checked against the known list of usernames and if it is new, it gets added along with the password. 
If the username already exists, the database will not be updated and the user will be returned to the login prompt.
I have also made it so that only the user and the admin account can add a new post under their username. If you attempt 
to create a post on behalf of another username, the app will not let you unless you are signed in as admin.I added some 
styling to the webpage to make it more presetenable as well.
