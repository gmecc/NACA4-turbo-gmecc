from naca4turbo import NACA4turbo
pr = NACA4turbo(p=4, t=10)
pr.profile(m=10)
pr.plot()

# расчет профиля по заданному углу поворота потока
pr.optim(dalpha=64)
pr.plot()


# координата верхней поверхности профиля
print([pr.f.xU, pr.f.yU])

# координата нижней поверхности профиля
print([pr.f.xL, pr.f.yL])

