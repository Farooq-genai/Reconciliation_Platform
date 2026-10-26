from sqlalchemy import text
from database import engine


try:
    with engine.connect() as connection:
        result = connection.execute(text("Select Version()"))
        print("PostgreSQL Connection Successful")
        print(result.scalar())

except Exception as err:
    print("PostgreSQL Connection Failed!")
    print(err)

    