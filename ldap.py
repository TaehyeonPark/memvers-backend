from ldap3 import Server, Connection, ALL, NTLM

def get_ldap_connection(nickname : str = None):
    if nickname == None:
        return None