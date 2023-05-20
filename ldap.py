import subprocess
import ldap3

adminPassword = "admin_password"
ldapHost = 'ldap.sparcs.org'

shell = '/bin/sh'
uid = lambda: int(subprocess.check_output(['id', '-u', 'nobody']).decode().strip())
opt = {'shell': shell, 'uid': uid}

def escape(str):
    return str.replace('\\', '\\\\').replace('"', '\\"').replace('$', '\\$')

host = ['-H', ldapHost]
admin = ['-D', 'cn=admin,dc=sparcs,dc=org']
def dnOnly(un):
    return ['uid=' + escape(un) + ',ou=People,dc=sparcs,dc=org']
def dn(un):
    return ['-D'] + dnOnly(un)
def password(pw):
    return ['-w', escape(pw)]
def newPassword(pw):
    return ['-s', escape(pw)]
def file(path):
    return ['-f', escape(path)]

adminPass = password(adminPassword)
searchSuffix = ['-x', '-LLL', '-b', 'ou=People,dc=sparcs,dc=org', '|', 'grep', 'uidNumber:']

def e(params):
    return subprocess.run(params, **opt, capture_output=True, text=True)

async def auth(un, pw):
    command = 'ldapwhoami'
    if un and pw:
        result = await e([command] + host + dn(un) + password(pw))
        if result.returncode != 0 or len(result.stdout) == 0 or len(result.stderr) != 0:
            raise Exception({'command': command, 'err': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr})
    else:
        raise Exception({'command': command, 'un': un, 'pw': pw})

async def passwd(un, opass, npass):
    command = 'ldappasswd'
    if un and opass and npass:
        result = await e([command] + host + dn(un) + password(opass) + newPassword(npass) + ['-S'])
        if result.returncode != 0 or len(result.stdout) != 0 or len(result.stderr) != 0:
            raise Exception({'command': command, 'err': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr})
    else:
        raise Exception({'command': command, 'un': un, 'opass': opass, 'npass': npass})

async def passwdByAdmin(un, npass):
    command = 'ldappasswd'
    if un and npass:
        result = await e([command] + host + admin + adminPass + newPassword(npass) + ['-S'] + dnOnly(un))
        if result.returncode != 0 or len(result.stdout) != 0 or len(result.stderr) != 0:
            raise Exception({'command': command, 'err': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr})
    else:
        raise Exception({'command': command, 'un': un, 'npass': npass})

async def uids():
    command = 'ldapsearch'
    result = await e([command] + host + admin + adminPass + searchSuffix)
    if result.returncode != 0 or len(result.stderr) != 0:
        raise Exception({'command': command, 'err': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr})
    else:
        return [int(s.strip()) for s in result.stdout.replace('uidNumber: ', '').split('\n')]

def add(path):
    command = 'ldapadd'
    if path:
        return e([command, host, admin, adminPass, file(path)]).then(lambda result: None).catch(lambda err: {'command': command, 'err': err})
    else:
        return {'command': command, 'path': None}

def delete(un):
    command = 'ldapdelete'
    if un:
        return e([command, host, admin, adminPass, dnOnly(un)]).then(lambda result: None).catch(lambda err: {'command': command, 'err': err})
    else:
        return {'command': command, 'un': None}

def ldif(un, uid):
  return '\n'.join([
    f"dn: uid={un},ou=People,dc=sparcs,dc=org",
    f"uid: {un}",
    f"cn: {un}",
    'objectClass: account',
    'objectClass: posixAccount',
    'objectClass: top',
    'objectClass: shadowAccount',
    'objectClass: postfixAccount',
    'shadowMax: 99999',
    'shadowWarning: 7',
    'loginShell: /bin/bash',
    f"uidNumber: {uid}",
    'gidNumber: 400',
    f"homeDirectory: /home/{un}",
    f"mail: {un}@sparcs.org"
  ])

def bind(un, pw):
    dn = f'uid={un},ou=People,dc=sparcs,dc=org'
    try:
        server = ldap3.Server(host=ldapHost, get_info=ldap3.ALL)
        conn = ldap3.Connection(server, dn, pw, auto_bind=True)
        return True
    except ldap3.core.exceptions.LDAPBindError as e:
        print(e)
        return False

if __name__ == "__main__":
    from getpass import getpass
    address = 'ldap.sparcs.org'
    un = input('Username: ')
    pw = getpass('Password: ')
    dn = f'uid={un},ou=People,dc=sparcs,dc=org'
    server = ldap3.Server(address, get_info=ldap3.ALL)
    conn = None
    try:
        conn = ldap3.Connection(server, dn, pw, auto_bind=True)
    except ldap3.core.exceptions.LDAPBindError as e:
        print(e)
        exit(1)
    
    conn.search('ou=People,dc=sparcs,dc=org', '(objectclass=posixAccount)', attributes=['uidNumber'])

    print(conn.entries[0]['uidNumber'])