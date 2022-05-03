zero = [[],[]]
one = [[zero],[]]
negone = [[],[zero]]
star = [[zero],[zero]]
    
def print_game(G):
    """Given G = [ GL,GR ],
    prints a string that represents the game"""
    GL =""
    GR =""
    if zero in G[0]:
        GL+="0 "
    if one in G[0]:
        GL+="1 "
    if negone in G[0]:
        GL+="-1 "
    if star in G[0]:
        GL+="* "
    if zero in G[1]:
        GR+="0 "
    if one in G[1]:
        GR+="1 "
    if negone in G[1]:
        GR+="-1 "
    if star in G[1]:
        GR+="* "
    print("{"+GL+"|"+GR+"}")


def neg(G):
    """Returns the conjugate (negative) of G, -G = [-GR,-GL]"""
    HL=[]
    HR=[]
    if G==zero:
        return zero
    for Gl in G[0]:
        HR.append(neg(Gl))
    for Gr in G[1]:
        HL.append(neg(Gr))
    return [HL,HR]

def rank(G):
    """Returns the rank (birthday) of G"""
    if G==zero:
        return 0
    leftranks = [rank(Gl) for Gl in G[0]]
    rightranks = [rank(Gr) for Gr in G[1]]
    return 1+max(leftranks+rightranks)

def murder(n):
    """Returns the perfect murder of rank n"""
    if n==0:
        return zero
    if n==1:
        return negone
    else:
        return [[],[zero,murder(n-1)]]

def negmurder(n):
    """Returns the conjugate of the perfect murder of rank n"""
    if n==0:
        return zero
    if n==1:
        return one
    else:
        return [[zero,negmurder(n-1)],[]]

def oL(G):
    """Returns the winner (L or R) of G when Left plays first"""
    GL=G[0]
    if GL==[]:
        return 'L'
    for Gl in GL:
        if oR(Gl)=='L':
            return 'L'
    return 'R'

def oR(G):
    """Returns the winner (L or R) of G when Right plays first"""
    GR=G[1]
    RightFirst='L'
    if GR ==[]:
        return "R"
    for Gr in GR:
        if oL(Gr)=='R':
            return "R"
    return "L"

def o(G):
    """Returns the outcome of G"""
    LeftFirst=oL(G)
    RightFirst=oR(G)
    if LeftFirst=='L' and RightFirst=='R':
        return 'N'
    if LeftFirst=='L' and RightFirst=='L':
        return 'L'
    if LeftFirst=='R' and RightFirst=='R':
        return 'R'
    if LeftFirst=='R' and RightFirst=='L':
        return 'P'


def add(G,H):
    """Given games G=[GL,GR] and H=[HL,HR],
    returns the game that is the sum of G and H"""
    leftoptions=[]
    rightoptions=[]
    for Gl in G[0]:
        leftoptions.append(add(Gl,H))
    for Hl in H[0]:
        leftoptions.append(add(G,Hl))
    for Gr in G[1]:
        rightoptions.append(add(Gr,H))
    for Hr in H[1]:
        rightoptions.append(add(G,Hr))
    return[leftoptions, rightoptions]

def soL(G):
    """Returns the strong Left outcome of G"""
    n = rank(G)
    if n==0:
        return 'L'
    if oL(add(G,murder(n-1)))=='R' or oL(G)=='R':
        return 'R'
    return 'L'

def soR(G):
    """Returns the strong Right outcome of G"""
    n = rank(G)
    if n==0:
        return 'R'
    if oR(add(G,negmurder(n-1)))=='L' or oR(G)=='L':
        return 'L'
    return 'R'

def so(G):
    """Returns the strong outcome of G"""
    LeftStrong=soL(G)
    RightStrong=soR(G)
    if LeftStrong=='L' and RightStrong=='R':
        return 'N'
    if LeftStrong=='L' and RightStrong=='L':
        return 'L'
    if LeftStrong=='R' and RightStrong=='R':
        return 'R'
    if LeftStrong=='R' and RightStrong=='L':
        return 'P'

def proviso(G,H): 
    """Checks the Proviso for G>=H"""
    strongG=so(G)
    strongH=so(H)
    if strongG == "L":
        return True
    if strongH == "R":
        return True
    if strongG == strongH:
        return True
    return False

def maintenance_a(G,H):
    """Checks part (a) of the Maintenance Property for G>=H"""
    for Hl in H[0]:
        there_exists=False
        for Gl in G[0]:
            if is_greater(Gl,Hl):
                there_exists=True
                break
        for Hlr in Hl[1]:
            if is_greater(G,Hlr):
                there_exists=True
                break
        if not there_exists:
            return False
    return True

def maintenance_b(G,H):
    """Checks part (b) of the Maintenance Property for G>=H"""
    for Gr in G[1]:
        condition=False
        for Hr in H[1]:
            if is_greater(Gr,Hr):
                condition=True
                break
        for Grl in Gr[0]:
            if is_greater(Grl,H):
                condition = True
                break
        if not condition:
            return False
    return True

def is_greater(G,H):
    """Checks if G>=H mod E"""
    if proviso(G,H) and maintenance_a(G,H) and maintenance_b(G,H):
        return True
    else:
        return False
        
def is_invertible(G):
    """Returns True if G+(-G) is 0 (mod E), False otherwise"""
    H = neg(G)
    sum = add(G,H)
    return is_greater(sum,zero) and is_greater(zero,sum)

def is_Pfree(G):
    """Returns True if no followers of G, including G, have outcome P"""
    if o(G)=="P":
        return False
    for GL in G[0]:
        if not is_Pfree(GL):
            return False
    for GR in G[1]:
        if not is_Pfree(GR):
            return False
    return True