from naca4turbo import NACA4turbo

# расчет теоретического профиля
pr = NACA4turbo(p=4, t=12)

# расчет профиля по заданному углу альфа
pr.optim(dalpha=74)
# координата верхней поверхности профиля
print([pr.f.xU, pr.f.yU])

# координата верхней поверхности профиля
print([pr.f.xL, pr.f.yL])
pr.plot()

