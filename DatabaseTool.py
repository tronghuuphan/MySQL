from mysql.connector import MySQLConnection, Error
from aws_config import read_db_config, read_aws_config
from upload_image import upload_to_aws

def get_all_id():
    query = """
    SELECT id FROM LogApp_person
    """
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)

        cursor = conn.cursor()
        cursor.execute(query)

        rows = cursor.fetchall()
        return [rows[i][0] for i in range(len(rows))]
    except Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
        

def get_camera_id():
    query = """
    SELECT id FROM LogApp_camera
    """
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)

        cursor = conn.cursor()
        cursor.execute(query)

        rows = cursor.fetchall()
        return [rows[i][0] for i in range(len(rows))]
    except Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

def insert_person(name, image_file):
    query = """
    INSERT INTO LogApp_person(name)
    VALUES (%s)"""
    args = (name,)
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)

        cursor = conn.cursor()
        cursor.execute(query, args)

        conn.commit()
        upload_to_aws(image_file, image_file)
    except Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

def insert_tracking(idPeople_id, idContact_id, idCam_id, date, time):
    """
    NOTE: Date format: "yyyy-mm-dd"
          Time format: "hh:mm:ss"
    """

    query = """
    INSERT INTO LogApp_tracking(idPeople_id, idContact_id, idCam_id, date, time)
    VALUES (%s, %s, %s, %s, %s)"""
    args = (idPeople_id, idContact_id, idCam_id, date, time)
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)

        cursor = conn.cursor()
        cursor.execute(query, args)

        conn.commit()
    except Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
