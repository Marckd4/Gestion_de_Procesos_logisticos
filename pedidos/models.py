from django.db import models

from auditlog.registry import auditlog

class Solicitud(models.Model):
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    cod_dun = models.CharField(max_length=50)
    cod_ean = models.CharField(max_length=50)
    cod_sistema = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=255)
    area_solicitud = models.CharField(max_length=100)
    nombre_solicitante = models.CharField(max_length=120)
    cantidad_solicitada = models.PositiveIntegerField()
    status_prioridades = models.CharField(max_length=100)
    cant_enviada_bsf = models.PositiveIntegerField(default=0)
    chofer = models.CharField(max_length=120, blank=True, null=True)
    factura_guia = models.CharField(max_length=120, blank=True, null=True)
    
    def __str__(self):
        return self.cod_dun

auditlog.register(Solicitud)   
    

