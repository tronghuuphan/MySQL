from configparser import ConfigParser

def read_db_config(filename='config.ini', section='mysql'):
    parser = ConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file.'.format(section, filename))
    return db

def read_aws_config(filename='config.ini', section='aws'):
    parser = ConfigParser()
    parser.read(filename)

    if parser.has_section(section):
        items = parser.items(section)
        access_key, secret_access_key, bucket = [items[i][1] for i in range(3)]
    else:
        raise Exception('{0} not found in the {1} file.'.format(section, filename))
    return access_key, secret_access_key, bucket
