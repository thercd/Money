from django.test import TestCase, Client
import datetime
from django.urls import reverse
from django.contrib.auth.models import User
from . forms import DespesaForm
from .models import Conta
from django.forms.models import model_to_dict
from mock import patch


class DespesaFormTest(TestCase):
    def test_criar_despesa_sem_nome_deve_dar_erro(self):
        despesa = {}
        despesa['valor'] = 100
        despesa['dia_vencimento'] = '5'
        despesa['mes_inicio'] = '1'
        despesa['mes_termino'] = '2'
        despesa['cor'] = 'blue'
        despesa['icone'] = 'fa-times'
        despesa['categoria'] = 'teste'
        despesa['periodica'] = True
        despesa['repeticao_anual'] = True
        form = DespesaForm(data=despesa)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertIsNotNone(form.errors.get('nome', None))


    def test_criar_despesa_sem_valor_deve_dar_erro(self):
        despesa = {}
        despesa['nome'] = 'Teste'
        despesa['dia_vencimento'] = '5'
        despesa['mes_inicio'] = '1'
        despesa['mes_termino'] = '2'
        despesa['cor'] = 'blue'
        despesa['icone'] = 'fa-times'
        despesa['categoria'] = 'teste'
        despesa['periodica'] = True
        despesa['repeticao_anual'] = True
        form = DespesaForm(data=despesa)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertIsNotNone(form.errors.get('valor', None))

    def test_criar_despesa_sem_vencimento_deve_dar_erro(self):
        despesa = {}
        despesa['nome'] = 'Teste'
        despesa['valor'] = 100
        # despesa['dia_vencimento'] = '5'
        despesa['mes_inicio'] = '1'
        despesa['mes_termino'] = '2'
        despesa['cor'] = 'blue'
        despesa['icone'] = 'fa-times'
        despesa['categoria'] = 'teste'
        despesa['periodica'] = True
        despesa['repeticao_anual'] = True
        form = DespesaForm(data=despesa)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertIsNotNone(form.errors.get('dia_vencimento', None))


    def test_criar_despesa_sem_mes_inicio_e_periodica_deve_dar_erro(self):
        despesa = {}
        despesa['nome'] = 'Teste'
        despesa['valor'] = 100
        despesa['dia_vencimento'] = '5'
        # despesa['mes_inicio'] = '1'
        despesa['mes_termino'] = '2'
        despesa['cor'] = 'blue'
        despesa['icone'] = 'fa-times'
        despesa['categoria'] = 'teste'
        despesa['periodica'] = True
        despesa['repeticao_anual'] = True
        form = DespesaForm(data=despesa)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertIsNotNone(form.errors.get('mes_inicio', None))


    def test_criar_despesa_sem_mes_inicio_e_mes_filme_e_periodica_deve_dar_erro(self):
        despesa = {}
        despesa['nome'] = 'Teste'
        despesa['valor'] = 100
        despesa['dia_vencimento'] = '5'
        # despesa['mes_inicio'] = '1'
        # despesa['mes_termino'] = '2'
        despesa['cor'] = 'blue'
        despesa['icone'] = 'fa-times'
        despesa['categoria'] = 'teste'
        despesa['periodica'] = True
        despesa['repeticao_anual'] = True
        form = DespesaForm(data=despesa)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)
        self.assertIsNotNone(form.errors.get('mes_inicio', None))
        self.assertIsNotNone(form.errors.get('mes_termino', None))

    def test_criar_despesa_sem_mes_inicio_e_nao_periodica_deve_dar_erro(self):
        despesa = {}
        despesa['nome'] = 'Teste'
        despesa['valor'] = 100
        despesa['dia_vencimento'] = '5'
        # despesa['mes_inicio'] = '1'
        despesa['mes_termino'] = '2'
        despesa['cor'] = 'blue'
        despesa['icone'] = 'fa-times'
        despesa['categoria'] = 'teste'
        despesa['periodica'] = False
        despesa['repeticao_anual'] = True
        form = DespesaForm(data=despesa)
        self.assertTrue(form.is_valid())


    def test_criar_despesa_sem_mes_inicio_e_mes_filme_e_nao_periodica_deve_dar_erro(self):
        despesa = {}
        despesa['nome'] = 'Teste'
        despesa['valor'] = 100
        despesa['dia_vencimento'] = '5'
        # despesa['mes_inicio'] = '1'
        # despesa['mes_termino'] = '2'
        despesa['cor'] = 'blue'
        despesa['icone'] = 'fa-times'
        despesa['categoria'] = 'teste'
        despesa['periodica'] = False
        despesa['repeticao_anual'] = True
        form = DespesaForm(data=despesa)
        self.assertTrue(form.is_valid())


    def test_criar_despesa_sem_cor_deve_dar_nao_erro(self):
        despesa = {}
        despesa['nome'] = 'Teste'
        despesa['valor'] = 100
        despesa['dia_vencimento'] = '5'
        despesa['mes_inicio'] = '1'
        despesa['mes_termino'] = '2'
        # despesa['cor'] = 'blue'
        despesa['icone'] = 'fa-times'
        despesa['categoria'] = 'teste'
        despesa['periodica'] = True
        despesa['repeticao_anual'] = True
        form = DespesaForm(data=despesa)
        self.assertTrue(form.is_valid())

    def test_criar_despesa_sem_icone_deve_dar_nao_erro(self):
        despesa = {}
        despesa['nome'] = 'Teste'
        despesa['valor'] = 100
        despesa['dia_vencimento'] = '5'
        despesa['mes_inicio'] = '1'
        despesa['mes_termino'] = '2'
        despesa['cor'] = 'blue'
        # despesa['icone'] = 'fa-times'
        despesa['categoria'] = 'teste'
        despesa['periodica'] = True
        despesa['repeticao_anual'] = True
        form = DespesaForm(data=despesa)
        self.assertTrue(form.is_valid())


    def test_criar_despesa_sem_categoria_nao_deve_dar_erro(self):
        despesa = {}
        despesa['nome'] = 'Teste'
        despesa['valor'] = 100
        despesa['dia_vencimento'] = '5'
        despesa['mes_inicio'] = '1'
        despesa['mes_termino'] = '2'
        despesa['cor'] = 'blue'
        despesa['icone'] = 'fa-times'
        # despesa['categoria'] = 'teste'
        despesa['periodica'] = True
        despesa['repeticao_anual'] = True
        form = DespesaForm(data=despesa)
        self.assertTrue(form.is_valid())




class DespesaTest(TestCase):
    def test_cadastrar_despesa_sem_logar_deve_redirecionar_para_login(self):
        # user = User.objects.create_user(username='username', password='password')
        c = Client()
        #         c.force_login(user)
        despesa = {}
        despesa['nome'] = 'Teste'
        despesa['valor'] = 100
        despesa['dia_vencimento'] = '5'
        despesa['mes_inicio'] = '1'
        despesa['mes_termino'] = '2'
        despesa['cor'] = 'blue'
        despesa['icone'] = 'fa-times'
        despesa['categoria'] = 'teste'
        despesa['periodica'] = True
        despesa['repeticao_anual'] = True
        response = c.post(reverse('cadastro_despesa'), despesa, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], reverse('login'))

    def test_cadastrar_despesa_logado_deve_redirecionar_para_login(self):
        user = User.objects.create_user(username='username', password='password')
        c = Client()
        c.force_login(user)
        despesa = {}
        despesa['nome'] = 'Teste'
        despesa['valor'] = 100
        despesa['dia_vencimento'] = '5'
        despesa['mes_inicio'] = '1'
        despesa['mes_termino'] = '2'
        despesa['cor'] = 'blue'
        despesa['icone'] = 'fa-times'
        despesa['categoria'] = 'teste'
        despesa['periodica'] = True
        despesa['repeticao_anual'] = True
        response = c.post(reverse('cadastro_despesa'), despesa, follow=True)
        self.assertRedirects(response, reverse('cadastro_conta', args=[1]))
        self.assertTemplateUsed(response, 'parametrizar_contas.html')

class ContaTest(TestCase):
    def test_criar_conta(self):
        despesa = {}
        despesa['nome'] = 'Teste'
        despesa['valor'] = 100
        despesa['dia_vencimento'] = '5'
        despesa['mes_inicio'] = '1'
        despesa['mes_termino'] = '2'
        despesa['cor'] = 'blue'
        despesa['icone'] = 'fa-times'
        despesa['categoria'] = 'teste'
        despesa['periodica'] = False
        despesa['repeticao_anual'] = False
        form = DespesaForm(data=despesa)
        despesa_model = form.save(commit=False)
        referencia = datetime.date(2018, 3, 8)
        sujeito = despesa_model.criar_conta(referencia)
        conta = Conta()
        conta.despesa = despesa_model
        conta.valor = despesa_model.valor
        conta.dia_vencimento = despesa_model.dia_vencimento
        conta.referente = referencia
        self.assertEqual(model_to_dict(sujeito), model_to_dict(conta))

    def test_criar_contas_ano_inteiro_com_contas_sem_vencer_deve_criar_12_contas(self):
        despesa = {}
        despesa['nome'] = 'Teste'
        despesa['valor'] = 100
        despesa['dia_vencimento'] = '5'
        despesa['mes_inicio'] = '1'
        despesa['mes_termino'] = '12'
        despesa['cor'] = 'blue'
        despesa['icone'] = 'fa-times'
        despesa['categoria'] = 'teste'
        despesa['periodica'] = True
        despesa['repeticao_anual'] = False
        form = DespesaForm(data=despesa)
        despesa_model = form.save(commit=False)
        sujeito = despesa_model.criar_contas(datetime.date(2018,1,1))
        self.assertEqual(len(sujeito), 12)