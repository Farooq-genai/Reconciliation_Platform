
from file_service import read_uploaded_file

csv_content = b"name,age,city\nUmar,30,Hyderabad\nAli,28,Pune"

df = read_uploaded_file("users.csv", csv_content)

print("File reading successful")
print(df.to_dict(orient="records"))
