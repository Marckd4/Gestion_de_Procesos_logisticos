from django.contrib import admin
from .models import Solicitud
from auditlog.registry import auditlog
from auditlog.models import LogEntry
from django.utils.html import format_html

# Registrar el modelo en auditlog
auditlog.register(Solicitud)

class SolicitudAdmin(admin.ModelAdmin):
    list_display = ('id', 'cod_dun', 'ultimo_usuario', 'fecha_modificacion', 'ver_historial')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        logs = LogEntry.objects.filter(
            content_type__model='solicitud',
            object_id__in=[str(obj.pk) for obj in qs]
        ).order_by('object_id', '-timestamp')
        logs_dict = {}
        history_dict = {}
        for log in logs:
            if log.object_id not in logs_dict:
                logs_dict[log.object_id] = log
            history_dict.setdefault(log.object_id, []).append(log)
        self.logs_dict = logs_dict
        self.history_dict = history_dict
        return qs

    def ultimo_usuario(self, obj):
        log = self.logs_dict.get(str(obj.pk))
        return log.actor if log else None
    ultimo_usuario.short_description = 'Último Usuario'

    def fecha_modificacion(self, obj):
        log = self.logs_dict.get(str(obj.pk))
        return log.timestamp if log else None
    fecha_modificacion.short_description = 'Fecha Modificación'

    def ver_historial(self, obj):
        logs = self.history_dict.get(str(obj.pk), [])
        if not logs:
            return "-"
        html = "<ul style='margin:0;padding-left:15px;'>"
        for log in logs:
            usuario = log.actor if log.actor else "Sistema / Desconocido"
            fecha = log.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            accion = log.get_action_display()
            html += f"<li><b>{accion}</b> por {usuario} el {fecha}</li>"
        html += "</ul>"
        return format_html(html)
    ver_historial.short_description = "Historial de Cambios"

admin.site.register(Solicitud, SolicitudAdmin)
