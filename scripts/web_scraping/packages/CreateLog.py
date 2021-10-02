from datetime import datetime as dt

def printLog(msg, path_log_file):
    '''
    Parameters
    ----------
    msg : string
        Message to be printed and saved in the log file.
    path_log_file : string
        Path to the log file, a new file will be created if it does not exist
        in the path.

    Returns
    -------
    string message.

    '''
    
    logf = path_log_file.replace('.txt','_{d}.txt'.format(d=dt.now().strftime('%Y%m%d')))
    msg = f"{dt.now().strftime('%Y%m%d_%H%M%S').split('.')[0]}: {msg.replace('\n', ' ')[:255]}"
    with open(logf, 'a+') as logf:
        print(msg.replace('\n', ' '), file = logf)
    
    print(msg)