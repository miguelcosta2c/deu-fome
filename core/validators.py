# usuarios/validators.py
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.core.files.uploadedfile import UploadedFile


def validar_dimensoes(campo_imagem: UploadedFile) -> None:
    # ==========================================
    # 2. VALIDAÇÃO DE DIMENSÕES (PIXELS)
    # ==========================================
    largura_max, altura_max = 2000, 2000
    largura_min, altura_min = 200, 200

    dimensoes = get_image_dimensions(campo_imagem)
    if not dimensoes:
        msg = "Não foi possível ler as dimensões da imagem."
        raise ValidationError(msg)

    largura, altura = dimensoes

    # Valida dimensões máximas
    if largura > largura_max or altura > altura_max:
        msg = (
            f"A imagem é muito grande ({largura}x{altura}px). "
            f"As dimensões máximas permitidas são {largura_max}x{altura_max} pixels."
        )
        raise ValidationError(msg)

    # Valida dimensões mínimas
    if largura < largura_min or altura < altura_min:
        msg = (
            f"A imagem é muito pequena ({largura}x{altura}px). "
            f"As dimensões mínimas permitidas são {largura_min}x{altura_min} pixels."
        )
        raise ValidationError(msg)


def validar_peso(campo_imagem: UploadedFile) -> None:
    # ==========================================
    # 1. VALIDAÇÃO DE PESO (TAMANHO DO ARQUIVO)
    # ==========================================
    peso_maximo_mb = 5
    peso_minimo_kb = 10

    tamanho_bytes = campo_imagem.size

    # Valida limite máximo (5MB)
    if tamanho_bytes > peso_maximo_mb * 1024 * 1024:
        msg = f"O arquivo é muito pesado. O tamanho máximo permitido é de \
            {peso_maximo_mb}MB."
        raise ValidationError(msg)

    # Valida limite mínimo (10KB)
    if tamanho_bytes < peso_minimo_kb * 1024:
        msg = f"O arquivo é muito leve. O tamanho mínimo permitido é de \
            {peso_minimo_kb}KB."
        raise ValidationError(msg)


def validar_tipo(campo_imagem: UploadedFile) -> None:
    # ==========================================
    # 3. VALIDAÇÃO DE TIPO (EXTENSÃO DO ARQUIVO)
    # ==========================================
    tipos_permitidos = ["image/jpeg", "image/png", "image/gif"]

    if campo_imagem.content_type not in tipos_permitidos:
        msg = (
            f"Tipo de arquivo inválido. "
            f"Os tipos permitidos são: {', '.join(tipos_permitidos)}."
        )
        raise ValidationError(msg)
