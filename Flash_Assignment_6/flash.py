from sage.all_cmdline import *

def coppersmith_howgrave_univariate(polynomial, modulus, beta, a, b, c):
    degree = polynomial.degree()
    value = degree * a + b

    if not 0<beta<=1:
        print("Beta lies out of (0, 1]")

    if not polynomial.is_monic():
        print("Polynomial isn't monic")
        
    Z_polynomial = polynomial.change_ring(ZZ)
    x = Z_polynomial.parent().gen()
    items = []
    for i in range(a):
        for j in range(degree):
            items.append((x * c)**j * modulus**(a - i) * Z_polynomial(x * c)**i)
    for i in range(b):
        items.append((x * c)**i * Z_polynomial(x * c)**a)

    M = Matrix(ZZ, value)

    for i in range(value):
        for j in range(i+1 ):
            M[i, j] = items[i][j]

    M = M.LLL()

    new_polynomial = 0 
    for i in range(value):
        new_polynomial += x**i * M[0 , i] / c**i

    potential_roots = new_polynomial.roots()

    roots = []
    for root in potential_roots:
        if root[0].is_integer():
            result = Z_polynomial(ZZ(root[0]))
            if gcd(modulus, result) >= modulus**beta:
                roots.append(ZZ(root[0]))

    return roots


e = 5

C = 20246814261631107295898476034132329896369527825079116685612857757892232359486103941729994361167407984386123338483313228791827891624563281533529947728958603718203679480035946561281117069953203476164441459491949703202741230369634268312423888323367573910490664163011674505910440811832580691350340009122754556804

N = 84364443735725034864402554533826279174703893439763343343863260342756678609216895093779263028809246505955647572176682669445270008816481771701417554768871285020442403001649254405058303439906229201909599348669565697534331652019516409514800265887388539283381053937433496994442146419682027649079704982600857517093
ZmodN = Zmod(N);


if __name__ == "__main__":
    s="flash: This door has RSA encryption with exponent 5 and the password is"
    maximum_length = 200
    final_string = ''.join(['{0:08b}'.format(ord(x)) for x in s])
    #print('final_string :',final_string)
    flag = False

    for length_x in range(0 , maximum_length+1 , 4 ):         

        P = PolynomialRing(ZmodN, names=('x',)); (x,) = P._first_ngens(1)
        polynomial = ((int(final_string, 2 )<<length_x) + x)**e - C
        degree = polynomial.degree()

        beta = 1                                 
        epsilon = beta / 7                       
        a = ceil(beta**2  / (degree * epsilon))     
        b = floor(degree * a * ((1 /beta) - 1 ))    
        c = ceil(N**((beta**2 /degree) - epsilon))  

        roots = coppersmith_howgrave_univariate(polynomial, N, beta, a, b, c)

        if roots:
            print("Solution found of size", length_x)
            print("Solution is :", '{0:b}'.format(roots[0]))
            password = str('{0:b}'.format(roots[0]))
            #print(password)
            decoded_password = ""
            for block in range(10):
                c = password[6+block*8:6+(block+1)*8]
                print('Binary :',c,'Decimal:',int(c,2),'Character:',chr(int(c, 2)))
                decoded_password+= chr(int(c, 2))
                #print(decoded_password)
            print("Final password to clear level 6: " + str(decoded_password))
            flag = True
    		#print(flag)
    if flag is False:
    	print ('Not found any solution')

