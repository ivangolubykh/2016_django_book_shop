'''
Мои собственные шаблонные фильтры тут.
'''
from django import template


register = template.Library()


@register.filter(name='get_add')
def get_add(dic, arg=False):
    ''' Функция должна получить словарь из request.GET
    и вернуть строку get-запроса вида ?q=Автор+01
    А при наличии дополнительного параметра arg, еще и добавить к строке
    параметр page=arg для работы пагинации. Итог может получиться такого вида:
    ?q=Автор+01&page=2
    '''
    if len(dic) == 0 and not arg:
        return ''
    if 'page' in dic:
        dic['page'] = [str(arg)]
    rez = list(map(lambda var_name: '{}={}'.
               format(var_name, '+'.join(dic[var_name][0].split())), dic))
    if 'page' not in dic:
        rez.append('page={}'.format(arg))
    return '?'+'&'.join(rez)
