from io import BytesIO

import pytest
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

from core.validators import validar_dimensoes, validar_peso, validar_tipo


def criar_imagem(largura: int, altura: int, formato: str = "JPEG") -> BytesIO:
    imagem = Image.new("RGB", (largura, altura), color="red")
    buffer = BytesIO()
    imagem.save(buffer, format=formato)
    buffer.seek(0)
    return buffer


class TestValidarPeso:
    def test_5mb_exato_valido(self):
        arquivo = SimpleUploadedFile("foto.jpg", b"x" * 5 * 1024 * 1024)
        validar_peso(arquivo)

    def test_5mb_mais_1_byte_invalido(self):
        arquivo = SimpleUploadedFile("foto.jpg", b"x" * (5 * 1024 * 1024 + 1))
        with pytest.raises(ValidationError):
            validar_peso(arquivo)

    def test_2kb_exato_valido(self):
        arquivo = SimpleUploadedFile("foto.jpg", b"x" * 2 * 1024)
        validar_peso(arquivo)

    def test_1_byte_menor_que_2kb_invalido(self):
        arquivo = SimpleUploadedFile("foto.jpg", b"x")
        with pytest.raises(ValidationError):
            validar_peso(arquivo)

    def test_0_bytes_invalido(self):
        arquivo = SimpleUploadedFile("foto.jpg", b"")
        with pytest.raises(ValidationError):
            validar_peso(arquivo)

    def test_1mb_valido(self):
        arquivo = SimpleUploadedFile("foto.jpg", b"x" * 1024 * 1024)
        validar_peso(arquivo)

    def test_erro_max_menciona_5mb(self):
        arquivo = SimpleUploadedFile("foto.jpg", b"x" * (5 * 1024 * 1024 + 1))
        with pytest.raises(ValidationError) as exc:
            validar_peso(arquivo)
        assert "5MB" in str(exc.value)

    def test_erro_min_menciona_2kb(self):
        arquivo = SimpleUploadedFile("foto.jpg", b"x")
        with pytest.raises(ValidationError) as exc:
            validar_peso(arquivo)
        assert "2KB" in str(exc.value)


class TestValidarTipo:
    def test_jpg_valido(self):
        arquivo = SimpleUploadedFile("foto.jpg", b"x")
        validar_tipo(arquivo)

    def test_jpeg_valido(self):
        arquivo = SimpleUploadedFile("foto.jpeg", b"x")
        validar_tipo(arquivo)

    def test_png_valido(self):
        arquivo = SimpleUploadedFile("foto.png", b"x")
        validar_tipo(arquivo)

    def test_webp_valido(self):
        arquivo = SimpleUploadedFile("foto.webp", b"x")
        validar_tipo(arquivo)

    def test_gif_invalido(self):
        arquivo = SimpleUploadedFile("foto.gif", b"x")
        with pytest.raises(ValidationError):
            validar_tipo(arquivo)

    def test_bmp_invalido(self):
        arquivo = SimpleUploadedFile("foto.bmp", b"x")
        with pytest.raises(ValidationError):
            validar_tipo(arquivo)

    def test_svg_invalido(self):
        arquivo = SimpleUploadedFile("foto.svg", b"x")
        with pytest.raises(ValidationError):
            validar_tipo(arquivo)

    def test_png_maiusculo_valido(self):
        arquivo = SimpleUploadedFile("foto.PNG", b"x")
        validar_tipo(arquivo)

    def test_jpeg_misto_valido(self):
        arquivo = SimpleUploadedFile("foto.JpEg", b"x")
        validar_tipo(arquivo)

    def test_sem_extensao_invalido(self):
        arquivo = SimpleUploadedFile("foto", b"x")
        with pytest.raises(ValidationError):
            validar_tipo(arquivo)

    def test_erro_menciona_tipos_permitidos(self):
        arquivo = SimpleUploadedFile("foto.gif", b"x")
        with pytest.raises(ValidationError) as exc:
            validar_tipo(arquivo)
        assert "JPEG" in str(exc.value)
        assert "PNG" in str(exc.value)
        assert "WEBP" in str(exc.value)


class TestValidarDimensoes:
    def test_2000x2000_valido(self):
        buffer = criar_imagem(2000, 2000)
        arquivo = SimpleUploadedFile("foto.jpg", buffer.read())
        validar_dimensoes(arquivo)

    def test_200x200_valido(self):
        buffer = criar_imagem(200, 200)
        arquivo = SimpleUploadedFile("foto.jpg", buffer.read())
        validar_dimensoes(arquivo)

    def test_2001x2000_largura_excede_invalido(self):
        buffer = criar_imagem(2001, 2000)
        arquivo = SimpleUploadedFile("foto.jpg", buffer.read())
        with pytest.raises(ValidationError):
            validar_dimensoes(arquivo)

    def test_2000x2001_altura_excede_invalido(self):
        buffer = criar_imagem(2000, 2001)
        arquivo = SimpleUploadedFile("foto.jpg", buffer.read())
        with pytest.raises(ValidationError):
            validar_dimensoes(arquivo)

    def test_199x200_largura_abaixo_invalido(self):
        buffer = criar_imagem(199, 200)
        arquivo = SimpleUploadedFile("foto.jpg", buffer.read())
        with pytest.raises(ValidationError):
            validar_dimensoes(arquivo)

    def test_200x199_altura_abaixo_invalido(self):
        buffer = criar_imagem(200, 199)
        arquivo = SimpleUploadedFile("foto.jpg", buffer.read())
        with pytest.raises(ValidationError):
            validar_dimensoes(arquivo)

    def test_1500x1500_valido(self):
        buffer = criar_imagem(1500, 1500)
        arquivo = SimpleUploadedFile("foto.jpg", buffer.read())
        validar_dimensoes(arquivo)

    def test_arquivo_pdf_invalido(self):
        arquivo = SimpleUploadedFile("foto.pdf", b"%PDF-1.4")
        with pytest.raises(ValidationError):
            validar_dimensoes(arquivo)

    def test_erro_maximo_menciona_2000x2000(self):
        buffer = criar_imagem(2001, 2000)
        arquivo = SimpleUploadedFile("foto.jpg", buffer.read())
        with pytest.raises(ValidationError) as exc:
            validar_dimensoes(arquivo)
        assert "2000x2000" in str(exc.value)

    def test_erro_minimo_menciona_200x200(self):
        buffer = criar_imagem(199, 200)
        arquivo = SimpleUploadedFile("foto.jpg", buffer.read())
        with pytest.raises(ValidationError) as exc:
            validar_dimensoes(arquivo)
        assert "200x200" in str(exc.value)
