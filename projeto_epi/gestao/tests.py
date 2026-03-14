from django.test import TestCase

# Create your tests here.

#def test_configuracao_inicial():
#   assert 1 + 1 == 2

import pytest
from django.utils import timezone
from django.db import IntegrityError
from gestao.models import Colaborador, Equipamento, Emprestimo

# ==============================
# TESTE COLABORADOR
# ==============================

@pytest.mark.django_db
def test_criar_colaborador():
    colaborador = Colaborador.objects.create(
        nome="João da Silva",
        matricula="12345",
        cargo="Operador"
    )

    assert colaborador.nome == "João da Silva"
    assert colaborador.matricula == "12345"
    assert colaborador.ativo is True


# ==============================
# TESTE EQUIPAMENTO
# ==============================

@pytest.mark.django_db
def test_criar_equipamento():
    equipamento = Equipamento.objects.create(
        nome="Capacete",
        ca="CA1234",
        quantidade_total=10,
        quantidade_disponivel=10,
        data_validade="2030-12-31"
    )

    assert equipamento.nome == "Capacete"
    assert equipamento.quantidade_total == 10
    assert equipamento.quantidade_disponivel == 10


# ==============================
# TESTE EMPRÉSTIMO
# ==============================

@pytest.mark.django_db
def test_criar_emprestimo():
    colaborador = Colaborador.objects.create(
        nome="Maria",
        matricula="999",
        cargo="Técnica"
    )

    equipamento = Equipamento.objects.create(
        nome="Luva",
        ca="CA5678",
        quantidade_total=5,
        quantidade_disponivel=5,
        data_validade="2030-12-31"
    )

    emprestimo = Emprestimo.objects.create(
        colaborador=colaborador,
        equipamento=equipamento
    )

    assert emprestimo.colaborador.nome == "Maria"
    assert emprestimo.equipamento.nome == "Luva"
    assert emprestimo.data_devolucao is None


# ==============================
# TESTE DEVOLUÇÃO
# ==============================

@pytest.mark.django_db
def test_devolucao_emprestimo():
    colaborador = Colaborador.objects.create(
        nome="Carlos",
        matricula="888",
        cargo="Supervisor"
    )

    equipamento = Equipamento.objects.create(
        nome="Óculos",
        ca="CA9999",
        quantidade_total=3,
        quantidade_disponivel=3,
        data_validade="2030-12-31"
    )

    emprestimo = Emprestimo.objects.create(
        colaborador=colaborador,
        equipamento=equipamento
    )

    # Simula devolução
    emprestimo.data_devolucao = timezone.now()
    emprestimo.save()

    assert emprestimo.data_devolucao is not None

# ==============================
# TESTE MATRICULA UNICA
# ==============================

@pytest.mark.django_db
def test_matricula_unica_colaborador():
    Colaborador.objects.create(
        nome="João",
        matricula="123",
        cargo="Operador"
    )

    with pytest.raises(IntegrityError):
        Colaborador.objects.create(
            nome="Maria",
            matricula="123",
            cargo="Técnica"
        )

# ==============================
# TESTE STR COLABORADOR
# ==============================

@pytest.mark.django_db
def test_str_colaborador():
    colaborador = Colaborador.objects.create(
        nome="Ana Souza",
        matricula="777",
        cargo="Engenheira"
    )

    assert str(colaborador) == "Ana Souza (777)"

    # ==============================
# TESTE COLABORADOR INICIA ATIVO
# ==============================

@pytest.mark.django_db
def test_colaborador_inicia_ativo():
    colaborador = Colaborador.objects.create(
        nome="Roberto Lima",
        matricula="555",
        cargo="Analista"
    )

    assert colaborador.ativo is True