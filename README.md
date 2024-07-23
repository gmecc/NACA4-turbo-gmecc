# NACA4-turbo-gmecc
NACA for turbine stages


# расчет теоретического профиля
```python
pr = NACA4turbo(p=4, t=12)
```

# расчет профиля по заданному углу поворота потока
```python
pr.optim(dalpha=74)
```
# координата верхней поверхности профиля
```python
print([pr.f.xU, pr.f.yU])
```

# координата верхней поверхности профиля
```python
print([pr.f.xL, pr.f.yL])
pr.plot()
```

Угол установки
Угол входа
Угол выхода

# расчет профиля турбинной решетки