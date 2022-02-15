from cms import run
from cms.model import Admin
from email_validator import validate_email,EmailNotValidError
from livereload import Server

app = run()


def add_admin():
    username = input("username : ")
    password = getpass("password : ")
    email = input("email : ")
    admin = Admin(username, password, email)
    admin.add_admin()
    print("admin added")

def migrate():
    import os
    if not os.path.isdir("migrations"):
        os.system("flask db init")
        
    os.system("flask db migrate")
    os.system("flask db upgrade")

if __name__ == "__main__":
    import sys
    from getpass import getpass
    if sys.argv[1] == "add_admin":
        try:
            add_admin()
        except KeyboardInterrupt:
            print("\nadmin creation canceled")
    elif sys.argv[1] == "migration":
        migrate()
    if sys.argv[1] == "dev":    
        server = Server(app.wsgi_app)
        server.serve(port=8000)