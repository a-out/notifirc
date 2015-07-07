from random import shuffle


def zero_min(n):
    return 0 if n < 0 else n


def read_nicks(nick_file):
    nicks = [l.rstrip() for l in nick_file.readlines()]
    shuffle(nicks)
    return nicks


def read_configs(config_file, nicks_file, creds_file):
    nicks = read_nicks(nicks_file)
    channels = [
        l.rstrip().split(' ') for l in
        config_file.readlines()]
    creds = creds_file.read().rstrip().split(' ')

    return [
        {
            'host': host,
            'port': port,
            'channel': channel,
            'nick': nicks.pop(),
            'creds': creds
        }
        for (host, port, channel) in channels
    ]
