from django.db import models

class rail_lines(models.Model):
    line_id = models.IntegerField()
    route_code = models.CharField(max_length=100)
    route_color = models.CharField(max_length=6)
    route_text_color = models.CharField(max_length=6)
    route_url = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    pdf_file_url = models.CharField(max_length=255)
    iconography_url = models.CharField(max_length=255)
    terminal_1 = models.CharField(max_length=100)
    terminal_2 = models.CharField(max_length=100)
    description_0 = models.CharField(max_length=100)
    description_1 = models.CharField(max_length=100)
    travel_direction_0 = models.CharField(max_length=100)
    travel_direction_1 = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = "Rail Lines"

    def __str__(self):
        return self.route_code
