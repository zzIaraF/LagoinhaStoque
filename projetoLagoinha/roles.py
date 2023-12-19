from rolepermissions.roles import AbstractUserRole

class Gerente(AbstractUserRole):
    available_permissions = {
        'ver_cat': True, 'edit_cat': True, 'ex_cat':True, 'cadas_cat': True,
        'ver': True, 'edit': True, 'excl':True, 'cadas': True,
        'ver_user': True, 'edit_user': True, 'cadas_user': True,
        }

class Vendedor(AbstractUserRole):
    available_permissions = {
        'ver_cat': True, 'cadas_cat': True, 'edit_cat': True,
        'ver': True, 'edit': True, 'excl':True, 'cadas': True,
        'ver_user': True, 'edit_user': True,
    }

