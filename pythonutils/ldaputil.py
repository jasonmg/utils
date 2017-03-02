# -*- coding: UTF-8 -*-

import ldap

_ldap_path = "ldap://ip:port"
_ldap_user = "ldap_user"
_ldap_pwd = "ldap_pwd"
_base_dn = "dc=xxx,dc=xxx"


def _validate_ldap_user(user_id):
    try:
        ###  if connection through SSL ldaps://xxxx:636
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
        ldap.set_option(ldap.OPT_REFERRALS, 0)
        ###   end 
        l = ldap.initialize(_ldap_path)
        l.protocol_version = ldap.VERSION3
        l.simple_bind_s(_ldap_user, _ldap_pwd)

        search_scope = ldap.SCOPE_SUBTREE
        search_filter_name = "sAMAccountName"
        search_filter = '(' + search_filter_name + "=" + user_id + ')'
        retrieve_attributes = None

        ldap_result_id = l.search(_base_dn, search_scope, search_filter, retrieve_attributes)
        result_type, result_data = l.result(ldap_result_id, 0)
        print("result: %s" % result_data)
        if not len(result_data) == 0:
            r_a, r_b = result_data[0]
            return 1, (r_b["distinguishedName"][0], r_b["mail"][0].decode("utf-8"),
                       r_b["displayName"][0].decode("utf-8"),
                       get_department_name(r_a))
        else:
            return 0, ()
    except ldap.LDAPError as e:
        print(e)
        return 0, ()
    finally:
        l.unbind()
        del l


def get_department_name(_data):
    """
    _data format: CN=xxx,OU=xxx,OU=xxx,OU=xxxDC=xxx,DC=local
    return xxx-xxx-xxx
    """
    strs = _data.split(",")
    if len(strs) > 1:
        department_strs = [s.replace("OU=", '') for s in strs if "OU=" in s and "OU=xxx-xxx" != s]
        department_strs.reverse()
        return ''.join(department_strs)
    else:
        return ''


def get_details(user, try_num=5):
    i = 0
    found_result = ()
    while i < try_num:
        is_found, found_result = _validate_ldap_user(user)
        if is_found:
            break
        i += 1
    return found_result


def ldap_validate(user_name, pwd):
    try:
        if not pwd:
            return False, "PassWord empty"
        detail = get_details(user_name, 10)
        if not detail:
            return False, "Not Exist User"
        dn, mail, name, department = detail
        my_ldap = ldap.initialize(_ldap_path)
        my_ldap.simple_bind_s(dn.decode("utf-8"), pwd)
        print("Login Ok")
        return True, (name, mail, department)
    except ldap.LDAPError as e:
        print("Login Fail: %s" % e)
        return False, e
