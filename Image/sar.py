import numpy as np

shh = 0.352 + .413j
shv = -0.517 + 0.732j
svh = shv
svv = 0.813 + 0.172j

kl = [[shh],[np.sqrt(2)*shv],[svv]]
kl = np.matrix(kl)
kl_dagger = np.conjugate(kl).T
cl = kl * kl_dagger
print("KL = ", kl)
print("\nKL_DAGGER = ", kl_dagger)
print("\nCL = ", cl)

kp = [[shh+svv], [shh-svv],[2*shv]]
kp = np.matrix(kp)*1/np.sqrt(2)
kp_dagger = np.conjugate(kp).T
cp = kp * kp_dagger
print("\nKP = ", kp)
print("\nKP_DAGGER = ", kp_dagger)
print("\nCP = ", cp)