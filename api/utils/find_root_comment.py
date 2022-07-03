
# 递归查找root评论
def find_root_comment(coment):
    if coment.parent_comment:
        return find_root_comment(coment.parent_comment)
    return coment
