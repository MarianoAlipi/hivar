# declaring them as global variables so that we can change the type to fit (string, int, enum) later
INT = 'int'
FLOAT = 'float'
CHAR = 'char'
BOOL = 'bool'
ERR = 'err'
plus = '+'
minus = '-'
div = '/'
mult = '*'
andop = '&&'
orop = '||'
morethan = '>'
lessthan = '<'
moreequal = '>='
lessequal = '<='
equals = '=='


def get_cube():
    cube = {}
    cube[INT] = {}
    cube[INT][INT] = {}
    cube[INT][FLOAT] = {}
    cube[INT][CHAR] = {}
    cube[INT][BOOL] = {}

    cube[INT][INT][plus] = INT
    cube[INT][INT][minus] = INT
    cube[INT][INT][div] = INT
    cube[INT][INT][andop] = ERR
    cube[INT][INT][orop] = ERR
    cube[INT][INT][morethan] = BOOL
    cube[INT][INT][lessthan] = BOOL
    cube[INT][INT][moreequal] = BOOL
    cube[INT][INT][lessequal] = BOOL
    cube[INT][INT][equals] = BOOL

    cube[INT][FLOAT][plus] = FLOAT
    cube[INT][FLOAT][minus] = FLOAT
    cube[INT][FLOAT][div] = FLOAT
    cube[INT][FLOAT][andop] = ERR
    cube[INT][FLOAT][orop] = ERR
    cube[INT][FLOAT][morethan] = BOOL
    cube[INT][FLOAT][lessthan] = BOOL
    cube[INT][FLOAT][moreequal] = BOOL
    cube[INT][FLOAT][lessequal] = BOOL
    cube[INT][FLOAT][equals] = BOOL

    cube[INT][CHAR][plus] = ERR
    cube[INT][CHAR][minus] = ERR
    cube[INT][CHAR][div] = ERR
    cube[INT][CHAR][andop] = ERR
    cube[INT][CHAR][orop] = ERR
    cube[INT][CHAR][morethan] = ERR
    cube[INT][CHAR][lessthan] = ERR
    cube[INT][CHAR][moreequal] = ERR
    cube[INT][CHAR][lessequal] = ERR
    cube[INT][CHAR][equals] = ERR

    cube[INT][BOOL][plus] = ERR
    cube[INT][BOOL][minus] = ERR
    cube[INT][BOOL][div] = ERR
    cube[INT][BOOL][andop] = ERR
    cube[INT][BOOL][orop] = ERR
    cube[INT][BOOL][morethan] = ERR
    cube[INT][BOOL][lessthan] = ERR
    cube[INT][BOOL][moreequal] = ERR
    cube[INT][BOOL][lessequal] = ERR
    cube[INT][BOOL][equals] = ERR

    cube[FLOAT] = {}
    cube[FLOAT][INT] = {}
    cube[FLOAT][FLOAT] = {}
    cube[FLOAT][CHAR] = {}
    cube[FLOAT][BOOL] = {}

    # We know the values are the same as INT FLOAT but we rather repeat them for easier consults

    cube[FLOAT][INT][plus] = FLOAT
    cube[FLOAT][INT][minus] = FLOAT
    cube[FLOAT][INT][div] = FLOAT
    cube[FLOAT][INT][andop] = ERR
    cube[FLOAT][INT][orop] = ERR
    cube[FLOAT][INT][morethan] = BOOL
    cube[FLOAT][INT][lessthan] = BOOL
    cube[FLOAT][INT][moreequal] = BOOL
    cube[FLOAT][INT][lessequal] = BOOL
    cube[FLOAT][INT][equals] = BOOL

    cube[FLOAT][FLOAT][plus] = FLOAT
    cube[FLOAT][FLOAT][minus] = FLOAT
    cube[FLOAT][FLOAT][div] = FLOAT
    cube[FLOAT][FLOAT][andop] = ERR
    cube[FLOAT][FLOAT][orop] = ERR
    cube[FLOAT][FLOAT][morethan] = BOOL
    cube[FLOAT][FLOAT][lessthan] = BOOL
    cube[FLOAT][FLOAT][moreequal] = BOOL
    cube[FLOAT][FLOAT][lessequal] = BOOL
    cube[FLOAT][FLOAT][equals] = BOOL

    cube[FLOAT][CHAR][plus] = ERR
    cube[FLOAT][CHAR][minus] = ERR
    cube[FLOAT][CHAR][div] = ERR
    cube[FLOAT][CHAR][andop] = ERR
    cube[FLOAT][CHAR][orop] = ERR
    cube[FLOAT][CHAR][morethan] = ERR
    cube[FLOAT][CHAR][lessthan] = ERR
    cube[FLOAT][CHAR][moreequal] = ERR
    cube[FLOAT][CHAR][lessequal] = ERR
    cube[FLOAT][CHAR][equals] = ERR

    cube[FLOAT][BOOL][plus] = ERR
    cube[FLOAT][BOOL][minus] = ERR
    cube[FLOAT][BOOL][div] = ERR
    cube[FLOAT][BOOL][andop] = ERR
    cube[FLOAT][BOOL][orop] = ERR
    cube[FLOAT][BOOL][morethan] = ERR
    cube[FLOAT][BOOL][lessthan] = ERR
    cube[FLOAT][BOOL][moreequal] = ERR
    cube[FLOAT][BOOL][lessequal] = ERR
    cube[FLOAT][BOOL][equals] = ERR

    cube[CHAR] = {}
    cube[CHAR][INT] = {}
    cube[CHAR][FLOAT] = {}
    cube[CHAR][CHAR] = {}
    cube[CHAR][BOOL] = {}

    cube[CHAR][INT][plus] = ERR
    cube[CHAR][INT][minus] = ERR
    cube[CHAR][INT][div] = ERR
    cube[CHAR][INT][andop] = ERR
    cube[CHAR][INT][orop] = ERR
    cube[CHAR][INT][morethan] = ERR
    cube[CHAR][INT][lessthan] = ERR
    cube[CHAR][INT][moreequal] = ERR
    cube[CHAR][INT][lessequal] = ERR
    cube[CHAR][INT][equals] = ERR

    cube[CHAR][FLOAT][plus] = ERR
    cube[CHAR][FLOAT][minus] = ERR
    cube[CHAR][FLOAT][div] = ERR
    cube[CHAR][FLOAT][andop] = ERR
    cube[CHAR][FLOAT][orop] = ERR
    cube[CHAR][FLOAT][morethan] = ERR
    cube[CHAR][FLOAT][lessthan] = ERR
    cube[CHAR][FLOAT][moreequal] = ERR
    cube[CHAR][FLOAT][lessequal] = ERR
    cube[CHAR][FLOAT][equals] = ERR

    cube[CHAR][CHAR][plus] = ERR
    cube[CHAR][CHAR][minus] = ERR
    cube[CHAR][CHAR][div] = ERR
    cube[CHAR][CHAR][andop] = ERR
    cube[CHAR][CHAR][orop] = ERR
    cube[CHAR][CHAR][morethan] = ERR
    cube[CHAR][CHAR][lessthan] = ERR
    cube[CHAR][CHAR][moreequal] = ERR
    cube[CHAR][CHAR][lessequal] = ERR
    cube[CHAR][CHAR][equals] = BOOL

    cube[CHAR][BOOL][plus] = ERR
    cube[CHAR][BOOL][minus] = ERR
    cube[CHAR][BOOL][div] = ERR
    cube[CHAR][BOOL][andop] = ERR
    cube[CHAR][BOOL][orop] = ERR
    cube[CHAR][BOOL][morethan] = ERR
    cube[CHAR][BOOL][lessthan] = ERR
    cube[CHAR][BOOL][moreequal] = ERR
    cube[CHAR][BOOL][lessequal] = ERR
    cube[CHAR][BOOL][equals] = ERR

    cube[BOOL] = {}
    cube[BOOL][INT] = {}
    cube[BOOL][FLOAT] = {}
    cube[BOOL][CHAR] = {}
    cube[BOOL][BOOL] = {}

    cube[BOOL][INT][plus] = ERR
    cube[BOOL][INT][minus] = ERR
    cube[BOOL][INT][div] = ERR
    cube[BOOL][INT][andop] = ERR
    cube[BOOL][INT][orop] = ERR
    cube[BOOL][INT][morethan] = ERR
    cube[BOOL][INT][lessthan] = ERR
    cube[BOOL][INT][moreequal] = ERR
    cube[BOOL][INT][lessequal] = ERR
    cube[BOOL][INT][equals] = ERR

    cube[BOOL][FLOAT][plus] = ERR
    cube[BOOL][FLOAT][minus] = ERR
    cube[BOOL][FLOAT][div] = ERR
    cube[BOOL][FLOAT][andop] = ERR
    cube[BOOL][FLOAT][orop] = ERR
    cube[BOOL][FLOAT][morethan] = ERR
    cube[BOOL][FLOAT][lessthan] = ERR
    cube[BOOL][FLOAT][moreequal] = ERR
    cube[BOOL][FLOAT][lessequal] = ERR
    cube[BOOL][FLOAT][equals] = ERR

    cube[BOOL][CHAR][plus] = ERR
    cube[BOOL][CHAR][minus] = ERR
    cube[BOOL][CHAR][div] = ERR
    cube[BOOL][CHAR][andop] = ERR
    cube[BOOL][CHAR][orop] = ERR
    cube[BOOL][CHAR][morethan] = ERR
    cube[BOOL][CHAR][lessthan] = ERR
    cube[BOOL][CHAR][moreequal] = ERR
    cube[BOOL][CHAR][lessequal] = ERR
    cube[BOOL][CHAR][equals] = ERR

    cube[BOOL][BOOL][plus] = ERR
    cube[BOOL][BOOL][minus] = ERR
    cube[BOOL][BOOL][div] = ERR
    cube[BOOL][BOOL][andop] = BOOL
    cube[BOOL][BOOL][orop] = BOOL
    cube[BOOL][BOOL][morethan] = ERR
    cube[BOOL][BOOL][lessthan] = ERR
    cube[BOOL][BOOL][moreequal] = ERR
    cube[BOOL][BOOL][lessequal] = ERR
    cube[BOOL][BOOL][equals] = BOOL

    return cube
