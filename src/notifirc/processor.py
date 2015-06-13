from pprint import pprint
from notifirc.utils import decode_msg

CONTEXT_AFTER = 5

def check_matches(msg, filters):
    matched_filters = []
    for f in filters:
        if f['func'](msg):
            matched_filters.append(f['id'])
    return matched_filters

def get_context(msg_store, channel, msg_id, m_after=5, m_before=2):
    msg_ids = list(range(msg_id - m_before, msg_id + m_after))
    return msg_store.get_messages(channel, msg_ids)

def process_messages(msg_store, sub, filters):
    last_msg = 0
    for m in sub.listen():
        msg_data = m['data']
        msg = decode_msg(msg_data)
        last_msg = msg['id']

        msg_store.save_message(msg['channel'], msg['id'], msg_data)

        # check msg from the past, so we have some
        # context for our matches
        msg_to_check = msg_store.get_message(msg['channel'], last_msg - 5)

        if msg_to_check:
            import ipdb; ipdb.set_trace()
            matches = check_matches(msg['msg'], filters)
            if len(matches) > 0:
                pprint(get_context(msg_store, msg_to_check['channel'], msg_to_check['id']))