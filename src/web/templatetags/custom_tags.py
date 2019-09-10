from django.template import Library, Node, TemplateSyntaxError
from django.template.base import FilterExpression

register = Library()

@register.filter(name='startswith')
def do_startswith(value, arg):
    return str(value).startswith(str(arg))

@register.filter(name='endswith')
def do_endswith(value, arg):
    return str(value).endswith(str(arg))

@register.filter(name='jsonify')
def do_jsonify(value):
     return str(value)

@register.tag(name='foreach')
def do_foreach(parser, token):
     try:
          # Split the tag content into words, respecting quoted strings.
          tag_name, i, to, n = token.split_contents()
          if not 'foreach' == tag_name or not 'to' == to:
               raise TemplateSyntaxError("Invalid syntax, use foreach i to n") 
          if not i or not n:
               raise TemplateSyntaxError("Invalid syntax, i and n must be integers or template variables")

          # parse integers or template variables
          i = int(i) if i.isdigit() else parser.compile_filter(i)
          n = int(n) if n.isdigit() else parser.compile_filter(n)

          # parse contents
          contents = parser.parse(('endforeach', ))
          parser.delete_first_token()

          # render content     
          return ForeachNode(i, n, contents)
     except (ValueError, Exception):
        raise TemplateSyntaxError("Invalid syntax, use foreach i to n")       

@register.tag(name='javascript')
def do_javascript(parser, token):
     try:
          # validate tag syntax
          tag_name, var = token.split_contents() 
          if not 'javascript' == tag_name or not var:
               raise TemplateSyntaxError("Invalid syntax, use javascript variable") 

          var_exp = parser.compile_filter(var)
          
          # render content 
          return JavascriptNode(var, var_exp)
     except (ValueError, Exception):
          raise TemplateSyntaxError("Invalid syntax, use javascript variable")  


class ForeachNode(Node):
     def __init__(self, i=0, n=0, contents=None):
          self.i, self.n, self.contents = i, n, contents

     def render(self, context):
          # resolve template variables
          i, n = self.i, self.n
          if isinstance(i, FilterExpression):
               i = i.resolve(context, ignore_failures=False)
          if isinstance(n, FilterExpression):
               n = n.resolve(context, ignore_failures=False)

          # loop variables i, n
          context['n'] = n
          nodelist = []            
          while i < n:
               context['i'] = i
               i += 1
               for node in self.contents:
                    nodelist.append(node.render_annotated(context))                    

          return ''.join(nodelist)


class JavascriptNode(Node):
     def __init__(self, var_name, var_exp):
          self.var_name, self.var_exp = var_name, var_exp

     def render(self, context):
          # resolve template variables
          object = self.var_exp.resolve(context, ignore_failures=False)

          # check for list or object
          if not object:
               return "let %s = null;" % self.var_name

          elif hasattr(object, '__iter__'):
               array = []
               for el in object:
                    if isinstance(el, str):
                         array.append("\'%s\'" % el)
                    else:
                         array.append(str(el))

               return "let %s = [%s];" % (self.var_name, ",\n".join(array))

          else:
               return "let %s = %s;" % (self.var_name, str(object))

