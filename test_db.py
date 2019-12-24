from pre_owned_books.models import User
print(User.query.all())

for i in User.query.all():
    print(i.username)
    print(i.password_hash)
