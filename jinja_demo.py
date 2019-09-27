from jinja2 import Environment, FileSystemLoader

cls = [{'name': 'exe'},

       ]
fields = [
    {'name': ['field' + str(i) for i in range(50)]}
]
field_type = {'type': 'models.CharField(max_length=200)'}
file_loader = FileSystemLoader('Templates')
env = Environment(loader=file_loader)
template = env.get_template('jinja_test.txt')
output = template.render(cls=cls, fields=fields, ftype=field_type)
print(output)
print(type(output))
str_byte = output.encode()

f = open('Templates/output.py', 'wb')
f.write(str_byte)
