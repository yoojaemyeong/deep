import pymysql
import pandas as pd

# 1. MySQL 서버에 연결
connection = pymysql.connect(
    host='localhost',      # MySQL 서버 호스트명
    user='root',           # MySQL 사용자 이름
    password='diabetes', # MySQL 비밀번호
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
        for _, row in dataframe.iterrows():
            sql = """
            INSERT INTO diabetic_meals (meal_name, calories, carbohydrates, protein, fat)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                row['meal_name'],
                row['calories'],
                row['carbohydrates'],
                row['protein'],
                row['fat']
            ))
        connection.commit()

# 4. 데이터 조회 함수
def query_data_from_mysql(connection):
    with connection.cursor() as cursor:
        sql = "SELECT * FROM diabetic_meals"
        cursor.execute(sql)
        result = cursor.fetchall()  # 조회된 모든 데이터를 가져옴
        return result

# 5. 삽입 함수 호출 및 결과 조회
try:
    insert_data_to_mysql(df, connection)
    print("데이터 삽입 완료!")

    # 데이터베이스에서 데이터 조회
    query_result = query_data_from_mysql(connection)
    
    # 조회 결과 출력
    print("데이터베이스에서 조회한 결과:")
    for row in query_result:
        print(row)

except Exception as e:
    print(f"오류 발생: {e}")
finally:
    connection.close()
