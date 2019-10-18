import imgaug as ia
import imgaug.augmenters as iaa
import inspect
import pprint
from termcolor import colored
import pygments


def transforms():
  return iaa.Sequential(
    [iaa.Crop(px=(0, 16)),
     iaa.GaussianBlur(sigma=(0, 3.0))])


class MyClass():
  def __init__(self):
    self.transforms = iaa.Sequential(
      [iaa.Crop(px=(0, 16)),
       iaa.GaussianBlur(sigma=(0, 3.0))])

  def __str__(self):
    return str(self.transforms)


# seq = transforms()
seq = MyClass()

# print(seq)
src = inspect.getsource(transforms)
# print(type(src))
# print(src)

# pprint.pprint(src, compact=True, indent=4)

# print(src.__dict__)

print(dir(pygments))
# print(pygments.highlight(src))

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter, TerminalFormatter
from pygments.formatters import get_formatter_for_filename
# from pygments.lexers import get_formatter_for_filename

aa = get_formatter_for_filename(__file__)
print(aa)

code = 'print "Hello World"'
print(highlight(src, PythonLexer(), TerminalFormatter()))