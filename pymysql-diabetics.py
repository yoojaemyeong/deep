import pymysql
import pandas as pd

# 1. MySQL 서버에 연결
connection = pymysql.connect(
    host='localhost',      # MySQL 서버 호스트명 (로컬호스트의 경우 'localhost')
    user='root',           # MySQL 사용자 이름
    password='diabetes', # MySQL 루트 비밀번호
    database='diabetics', # 사용할 데이터베이스 이름
    charset='utf8',
    cursorclass=pymysql.cursors.DictCursor
)

# 2. CSV 파일을 pandas로 읽기
csv_file_path = 'diabetic_meals.csv'  # CSV 파일 경로
df = pd.read_csv(csv_file_path)

# 3. 데이터베이스에 데이터를 삽입하는 함수
def insert_data_to_mysql(dataframe, connection):
    with connection.cursor() as cursor:
        # 데이터프레임의 각 행(row)을 MySQL에 삽입
        for _, row in dataframe.iterrows():
            sql = """
            INSERT INTO diabetic_meals (d_meal1, d_meal2, calories, carbohydrates, protein, fat)
            VALUES (%s, %s, %d, %f, %f,%f)
            """
            cursor.execute(sql, (
                row[‘d_meal1’],
	        row[‘d_meal2'],
                row['calories'],
                row['carbohydrates'],
                row['protein'],
                row['fat']

            ))
        # 변경사항을 커밋
        connection.commit()

# 4. 삽입 함수 호출
try:
    insert_data_to_mysql(df, connection)
    print("데이터 삽입 완료!")
except Exception as e:
    print(f"오류 발생: {e}")
finally:
    connection.close()
