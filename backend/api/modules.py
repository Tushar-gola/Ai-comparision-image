def error(message, errors = [], data = []):
    return {
        'data':data,
        'errors':errors,
        'message':message,
        'type': "error"
    }
    
def success(message, data = []):
    return {
        'data':data,
        'message':message,
        'type': "success"
    }
    
    
__url__='http://192.168.34.159:4044/'