from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    def __str__(self):
        return self.nombre
    

class Evento(models.Model):
    evento = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha = models.DateField()
    def __str__(self):
        return self.evento


class RegistroEvento(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    def __str__(self):
        return  f'Registro para {self.evento.evento} de {self.usuario.nombre}'
    

