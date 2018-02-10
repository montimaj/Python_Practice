import numpy as np

def get_terms(values, max_deg):
    x = values[0]
    y = values[1]
    calc = [1]
    flag = {}
    d1 = 1
    while d1 <= max_deg:
        d2 = 0
        while d2 <= max_deg:
            if d1+d2 <= max_deg:
                if (d2, d1) not in flag.keys():
                    flag[(d1, d2)] = False
                    calc.append((x**d1)*(y**d2))
                    if d1 != d2:
                        calc.append((y**d1)*(x**d2))
            d2 += 1
        d1 += 1
    zero_val = [0]*len(calc)
    calcx = calc + zero_val
    calcy = zero_val + calc
    return calcx, calcy

def generate_matrices(given_points, observed_points, deg):
    M=[]
    Y=[]
    for point in observed_points:
        terms = get_terms(point, deg)
        M.append(terms[0])
        M.append(terms[1])
    for point in given_points:
        Y.append(point[0])
        Y.append(point[1])
    M = np.matrix(M)
    Y = np.matrix(Y).transpose()
    V = (M.T * M).I * M.T * Y
    E = np.abs(Y - M * V)
    return V, E

def total_error(E):
    rmse = 0
    for value in E:
        rmse += value**2
    return np.sqrt(rmse)

def get_vector(a,b, inclusive=False):
    if inclusive:
        b += 1
    return np.arange(a,b)

def generate_random_vector(size):
    vec = []
    for value in range(size):
        vec.append(np.random.random())
    return vec

def replace_max_vec_value(vec, replace):
    vec[vec.index(max(vec))]=replace
    return vec

def normalize_matrix(mat):
    max_val=np.max(mat)
    return mat/max_val

def generate_matrix(m,n):
    mat=[]
    for i in range(m):
        matrow=[]
        for j in range(n):
            matrow.append(np.random.randint(1,10))
        mat.append(matrow)
    return np.matrix(mat)

def cov_matrix(mat, row=True):
    return np.cov(mat,rowvar=row)


print('Range vector=', get_vector(10, 99))
vec = generate_random_vector(100)
print('\nRandom vector=', vec)
print('After max val replaced by zero: ', replace_max_vec_value(vec,0))
random_mat=generate_matrix(5,5)
print('\nRandom Matrix=\n', random_mat,'\nNormalized matrix:\n', normalize_matrix(random_mat))
mat=np.matrix([[4.0,2.0,0.6],[4.2, 2.1, 0.59],[3.9,2.0,0.58],[4.3,2.1,0.62],[4.1,2.2,0.63]])
print('\nCovariance matrix=\n', cov_matrix(mat, False))
deg=1
given_points = [(0, 20),(108.3, 0.9),(127.4, 109.2),(19.1, 128.3),(63.7, 64.6)]
observed_points = [(0, 0),(100, 0),(100, 100),(0, 100),(50, 50)]
V, E = generate_matrices(given_points, observed_points, deg)
print('\nCoeff Matrix=\n', V,'\n\nError Matrix=\n', E, '\n\nTotal error=', total_error(E))
