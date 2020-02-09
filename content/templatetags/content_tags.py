from django import template
from django.utils.html import strip_tags


# class SplitText(template.Node):
#     def __init__(self, text, context_var):
#         self.text = template.Variable(text)
#         self.context_var = context_var
#
#     def render(self, context):
#         s = self.text.resolve(context).replace("\n", "")
#         try:
#             soup = BeautifulSoup(s)
#         except:
#             context[self.context_var] = [s, '']
#             return ''
#         bsoup = [str(i) for i in soup]  # big blocks
#         # print bsoup
#         blocks = []
#         plain_chunk = ''
#         chunk = ''
#         for p in bsoup:
#             plain_chunk += strip_tags(p)
#             chunk += p
#             if len(plain_chunk.split()) >= WORDS_PER_COLUMN or p == bsoup[len(bsoup) - 1]:
#                 blocks.append(chunk)
#                 chunk = ''
#                 plain_chunk = ''
#         context[self.context_var] = blocks
#         return ''
#
#
# register = template.Library()
#
#
# def checkBitsCount(bits, count):
#     if len(bits) != count:
#         raise template.TemplateSyntaxError('%s tag requires %d arguments' % (bits[0], (count - 1)))
#         return False
#     if bits[count - 2] != 'as':
#         raise template.TemplateSyntaxError("before-last argument to %s tag must be 'as'" % bits[0])
#         return False
#     return True
#
#
# WORDS_PER_COLUMN = 40  # testing
#
#
# def do_split_text(parser, token):
#     bits = token.contents.split()
#     if checkBitsCount(bits, 4):
#         return SplitText(bits[1], bits[3])
#
#
# register.tag('split_text', do_split_text)
