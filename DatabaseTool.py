from mysql.connector import MySQLConnection, Error
from aws_config import read_db_config, read_aws_config
from upload_image import upload_to_aws

def get_all_id():
    '''
    Get all ID from from the database (Person Table)
    '''
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
    '''
    Get all camera ID from database (Camera Table)
    '''
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
    '''
    Insert a person (name) into database (Person Table)
    param name: Name of person. If unknow, name = ""
    param image_file: NAME of image file (NOT PATH. If PATH, please preprocess)
    '''
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
    Example: insert_tracking(idPeople_id=1, idContact_id=2, idCam_id=4, date='2020-01-01', time='10:23:23')
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


# New feature: Upload personal Log
def insert_person_log(idPeople_id, idCam_id, mask, date, time, image):
    """
    Upload into person log
    Note:
        param mask: Boolean type (0 or 1)

    Example: insert_person_log(idPeople_id=2, idCam_id=1, mask=1,'2020-01-01','12:23:22','image_of_id.jpg')
    """

    query = """
    INSERT INTO LogApp_personlog(idPeople_id, idCam_id, mask, date, time, image)
    VALUES (%s,%s,%s,%s,%s,%s)
    """
    args = (idPeople_id, idCam_id, mask, date, time, 'person-log.s3.ap-southeast-1.amazonaws.com/' + image)
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)

        cursor = conn.cursor()
        cursor.execute(query, args)

        conn.commit()
        upload_to_aws(image, image, bucket='person-log')

    except Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

