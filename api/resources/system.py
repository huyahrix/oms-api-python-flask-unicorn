import logging
import pyodbc 
import bcrypt
import json
from api.configs.db import cursor, cnxn

#
#   auth
#
def getUserInfo(userName):
    str_query ="""SELECT * from users 
                INNER JOIN  employees ON user_id = emp_id 
                LEFT JOIN mailgroup ON director_emp_id = emp_id 
                WHERE user_login_name LIKE '{userName}' and status = 0 """.format(userName=userName)
    try:
        cursor.execute(str_query)
        resuft = cursor.fetchone()
        return resuft
    except pyodbc.Error as ex:
        logging.error(ex.args[1])
        return None


def verifyPassword(password, dbHash):
	if bcrypt.checkpw(password.encode("utf8"), dbHash.encode("utf8")):
	    return True
	else:
	    return False


#
#   menu
#
def getUserMenu(userId):
    str_query ="""select [g].[module_group_id], [g].[module_group_name] as [module_group], 
                [f].[module_id], [m].[module_name], [m].[module_icon], [m].[module_display_order], [f].[menu_id] as [form_id], [f].[menu_name] as [form_name], 
                [f].[menu_icon] as [form_icon], [f].[menu_display_order], [f].[url], 
                CASE WHEN b.menu_id IS NULL THEN 0 ELSE 1 END AS bookmark, 
                CASE WHEN B.menu_id IS NULL THEN 'fa fa-star-o text-green' ELSE 'fa fa-star text-grey' END AS bookmark_icon, 
                [g].[display_order], [f].[is_old_menu], [f].[old_permission], [f].[disabled], [f].[checkPermissions], [f].[form_active] 
                from [MainMenu] as [f] 
                left join [module] as [m] on [m].[module_id] = [f].[module_id] 
                left join [module_group] as [g] on [g].[module_group_id] = [m].[module_group_id] 
                left join [bookmarkmenu] as [b] on [b].[menu_id] = [f].[menu_id] and [b].[user_id] = '{user_id}' 
                where [f].[disabled] = '0' and [f].[is_menu] = '1' 
                order by g.display_order, m.module_display_order, f.menu_display_order""".format(user_id = userId)
    try:
        cursor.execute(str_query)
        result = cursor.fetchall()
        data = [dict(zip([key[0] for key in cursor.description], row)) for row in result]
        return data
    except pyodbc.Error as ex:
        logging.error(ex.args[1])
        return None


def getCustomizeMenu(userId):
    str_query = """select * from [customize_bookmark_menu] where [user_id] = '{}'""".format(userId)
    try:
        cursor.execute(str_query)
        result = cursor.fetchall()
        data = [dict(zip([key[0] for key in cursor.description], row)) for row in result]
        return data
    except pyodbc.Error as ex:
        logging.error(ex.args[1])
        return None


def GetBookmarkMenu(userId):
    str_query = """select [b].[menu_id], 
                CASE WHEN b.bookmark_type = 'custom' THEN c.menu_title ELSE m.menu_name END as menu_name, 
                CASE WHEN b.bookmark_type = 'custom' THEN 'fa fa-th' ELSE m.menu_icon END as menu_icon, 
                CASE WHEN b.bookmark_type = 'custom' THEN c.menu_url ELSE m.form_active END as form_active, 
                CASE WHEN b.bookmark_type = 'custom' THEN c.target ELSE '' END as target, 
                CASE WHEN m.is_old_menu = 1 THEN m.url ELSE (CASE WHEN c.menu_type = 1 THEN c.menu_url ELSE '' END) END as url, 
                CASE WHEN b.bookmark_type IS NULL THEN 0 ELSE 1 END as order_type, [b].[display_order] 
                from [BookmarkMenu] as [b] left join [MainMenu] as [m] on [m].[menu_id] = [b].[menu_id] 
                left join [customize_bookmark_menu] as [c] on [b].[menu_id] = CONVERT(varchar, c.custom_id) 
                where [b].[user_id] = '{}' order by [b].[display_order] asc, [order_type] desc""".format(userId)
    try:
        cursor.execute(str_query)
        result = cursor.fetchall()
        data = [dict(zip([key[0] for key in cursor.description], row)) for row in result]
        return data
    except pyodbc.Error as ex:
        logging.error(ex.args[1])
        return None


#
#   session
#
def CreateSessions(sessions):
    str_query ="""insert into [sessions] ([SessionID], [UserID], [DateTimeLogin], [IPAddress], [ServerID]) 
                values ('{SessionID}', '{UserID}', '{DateTimeLogin}', '{IPAddress}', '{ServerID}')""".format(
                    SessionID=sessions['SessionID'],
                    UserID = sessions['UserID'],
                    DateTimeLogin = sessions['DateTimeLogin'],
                    IPAddress = sessions['IPAddress'],
                    ServerID = sessions['ServerID'])
    try:
        cursor.execute(str_query)
        cnxn.commit()
        return True
    except pyodbc.Error as ex:
        logging.error(ex.args[1])
        return False


def GetSesionID():
    str_query = """	select top 1 [s].*, [e].[emp_sex], [u].[user_login_name] from [sessions] as [s] 
                    left join [users] as [u] on [u].[user_id] = [s].[UserID] 
                    left join [employees] as [e] on [e].[emp_id] = [s].[UserID] 
                    order by [s].[SessionID] desc"""
    try:
        cursor.execute(str_query)
        resuft = cursor.fetchone()
        return resuft
    except pyodbc.Error as ex:
        logging.error(ex.args[1])
        return None

