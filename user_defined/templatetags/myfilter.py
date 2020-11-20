from django import template

register = template.Library()


# 自定义过滤器实现模板变量的过滤
@register.filter
def myRepalce(value,args):
    # 将搜索的字段的,改为/
    old_value, new_value = args.split(':')
    return value.replace(old_value,new_value)

# # 返回对应的字符串的出版社
@register.filter
def get_real_publisher(value):
    try:
        value = eval(value)
        if len(value) == 1:
            return value[0]
        return value[-1]
    except:
        return value


# 返回对应字符串的作者
@register.filter
def get_real_author(value):
    try:
        value = eval(value)
        if len(value) == 1:
            return value[0]
        value = value[:-2]
    except:
        return value
    return ','.join(value)

# 在分页的按钮实现数字的减1
@register.filter
def get_sub(value):
    value -= 1
    return value