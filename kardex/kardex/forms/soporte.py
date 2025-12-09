# kardex/forms.py

# kardex/forms.py

# kardex/forms.py

from django import forms

from kardex.models import Soporte


class SoporteForm(forms.ModelForm):
    MAX_FILE_SIZE_MB = 50  # tamaño máximo permitido

    EXTENSIONS_PERMITIDAS = [
        "pdf",

        "doc", "docx",
        "xls", "xlsx",

        "png", "jpg", "jpeg", "gif", "webp",
    ]

    class Meta:
        model = Soporte
        fields = [
            'titulo',
            'descripcion',
            'categoria',
            'prioridad',
            'adjunto'
        ]

        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Asunto del problema'
            }),

            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe detalladamente tu problema'
            }),

            'categoria': forms.Select(attrs={
                'class': 'form-control'
            }),

            'prioridad': forms.Select(attrs={
                'class': 'form-control'
            }),

            # ✅ INPUT FILE
            'adjunto': forms.FileInput(attrs={
                'class': 'custom-file-input',
                'id': 'customFile',
                'accept': (
                    '.pdf,'
                    '.doc,.docx,'
                    '.xls,.xlsx,'
                    '.png,.jpg,.jpeg,.gif,.webp,'
                    'image/*'
                )
            }),
        }

    # ✅ VALIDACIÓN REAL EN BACKEND
    def clean_adjunto(self):

        archivo = self.cleaned_data.get('adjunto')

        # Campo opcional → si no viene, pasa
        if not archivo:
            return archivo

        # ------- VALIDAR EXTENSIÓN -------
        nombre = archivo.name
        extension = nombre.split(".")[-1].lower()

        if extension not in self.EXTENSIONS_PERMITIDAS:
            raise forms.ValidationError(
                "Formato de archivo no permitido. "
                "Solo se aceptan PDF, Word, Excel o imágenes."
            )

        # ------- VALIDAR TAMAÑO -------
        max_size_bytes = self.MAX_FILE_SIZE_MB * 1024 * 1024

        if archivo.size > max_size_bytes:
            raise forms.ValidationError(
                f"El archivo es demasiado grande. "
                f"Máximo permitido: {self.MAX_FILE_SIZE_MB} MB."
            )

        return archivo
