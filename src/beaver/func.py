# coding=UTF-8
__author__="Alex Korovyansky"
__date__ ="$15.04.2010 12:15:36$"

def subclasses(cls, _seen=None):    
    if not isinstance(cls, type):
        raise TypeError('itersubclasses must be called with '
                        'new-style classes, not %.100r' % cls)
    if _seen is None: _seen = set()
    try:
        subs = cls.__subclasses__()
    except TypeError: # fails only when cls is type
        subs = cls.__subclasses__(cls)
    for sub in subs:
        if sub not in _seen:
            _seen.add(sub)
            yield sub
            for sub in subclasses(sub, _seen):
                yield sub

def isint(data):
    '''проверка является ли аргумент int-числом'''
    try:
        int(data)
    except Exception:
        return 0
    return 1

def make_unicode(string):
    if type(string) != unicode:
        string = string.decode('utf-8')
    return string

def unmake_unicode(string):
    if type(string) == unicode:
        string = string.encode('utf-8')
    return string

def randbytes(length):
    import random
    return [random.randint(1,127) for b in range(0, length)]

def rand_7bit_ascii_string(length):
     return "".join([chr(random.randint(1,127)) for b in range(0, length)])

def stringtobytes(string):
    return [ord(c)%256 for c in string]

def bytestostring(bb):
    return "".join([chr(b) for b in bb])

def inttobytes(value):
  result = [] # инициализируем переменную, в которую запишем результат
  # собираем байты (в обратном порядке)
  while value > 0:
    tail = value % 0x100 # запомним остаток от деления на 256
    result.append(tail)  # либо в конец последовательности
    value >>= 8 # смещаемся на 8 бит вправо

  return result

def bytestoint(bb):
  result = 0L
  value = 1L
  for b in bb:
      result += b * value
      value <<= 8
  return result

def hextobytes(hex_string):
    result = []
    for i in range(0, len(hex_string) // 2):
        hb = hex_string[2*i:2*i+2]
        result.append(int(hb, 16))
    return result

def bytestohex(bb):
    return "".join(["%02x" % b for b in bb])


if __name__ == "__main__":
    s = "a.a"
    cut_extension(s)
    print s
    print bytestohex(hextobytes("01ff10"))
