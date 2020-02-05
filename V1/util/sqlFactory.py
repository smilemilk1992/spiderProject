import json

def getInsertSql(table,data):
    strCol = ''
    strVal = ''
    for k in data.keys():
        if k=="table":
            continue
        strCol += ',`' + k + '`'
        if isinstance(data[k], list):
            dataValue = '|'.join(data[k])
        elif isinstance(data[k], dict):
            dataValue = json.dumps(data[k], ensure_ascii=False)
        elif not isinstance(data[k], str):
            dataValue = str(data[k])
        else:
            dataValue = data[k]

        strVal += ",'" + dataValue.replace("\'","\\'") + "'"

    sql = "INSERT INTO `%s` (%s) VALUES (%s)" % (table, strCol[1:], strVal[1:])
    return sql