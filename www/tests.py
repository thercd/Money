from django.test import TestCase, Client
import datetime
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import DespesaForm, ContaForm
from .models import Conta, Despesa
from django.forms.models import model_to_dict
from freezegun import freeze_time


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

    def test_cadastrar_despesa_logado_deve_cadastrar(self):
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

    def test_alterar_despesa_sem_logar_deve_redirecionar_para_login(self):
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
        response = c.post(reverse('alteracao_despesa', args=[0]), despesa, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], reverse('login'))

    def test_alterar_despesa_de_outro_usuario_deve_dar_erro(self):
        user = User.objects.create_user(username='username', password='password')
        user2 = User.objects.create_user(username='username1', password='password1')
        c = Client()
        c.force_login(user2)
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
        form = DespesaForm(data=despesa)
        d = form.save(commit=False)
        d.usuario = user
        d.save()
        response = c.post(reverse('alteracao_despesa', args=[d.id]), despesa, follow=True)
        self.assertContains(response, 'Operaçao nao disponivel')

    def test_alterar_despesa_de_outro_usuario_deve_dar_erro(self):
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
        form = DespesaForm(data=despesa)
        d = form.save(commit=False)
        d.usuario = user
        d.save()
        response = c.post(reverse('alteracao_despesa', args=[d.id]), despesa, follow=True)
        self.assertContains(response, 'nada mudou')

    def test_alterar_despesa_deve_alterar(self):
        user = User.objects.create_user(username='username', password='password')
        c = Client()
        c.force_login(user)
        despesa = Despesa()
        despesa.nome = 'Teste'
        despesa.valor = 100
        despesa.dia_vencimento = 5
        despesa.mes_inicio = 1
        despesa.mes_termino = 2
        despesa.cor = 'blue'
        despesa.icone = 'fa-times'
        despesa.categoria = 'teste'
        despesa.periodica = True
        despesa.repeticao_anual = True
        despesa.usuario = user
        despesa.save()
        despesa.observacao = 'Troquei'
        response = c.post(reverse('alteracao_despesa', args=[despesa.id]), model_to_dict(despesa), follow=True)
        desp = Despesa.objects.get(id=despesa.id)
        self.assertEqual(model_to_dict(desp), model_to_dict(despesa))
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
        self.assertFalse(any(c.referente == datetime.date(2018, 1, 1) for c in sujeito))
        self.assertTrue(any(c.referente == datetime.date(2018, 1, 5) for c in sujeito))
        self.assertTrue(any(c.referente == datetime.date(2018, 2, 5) for c in sujeito))
        self.assertTrue(any(c.referente == datetime.date(2018, 3, 5) for c in sujeito))
        self.assertTrue(any(c.referente == datetime.date(2018, 4, 5) for c in sujeito))
        self.assertTrue(any(c.referente == datetime.date(2018, 5, 5) for c in sujeito))
        self.assertTrue(any(c.referente == datetime.date(2018, 6, 5) for c in sujeito))
        self.assertTrue(any(c.referente == datetime.date(2018, 7, 5) for c in sujeito))
        self.assertTrue(any(c.referente == datetime.date(2018, 8, 5) for c in sujeito))
        self.assertTrue(any(c.referente == datetime.date(2018, 9, 5) for c in sujeito))
        self.assertTrue(any(c.referente == datetime.date(2018, 10, 5) for c in sujeito))
        self.assertTrue(any(c.referente == datetime.date(2018, 11, 5) for c in sujeito))
        self.assertTrue(any(c.referente == datetime.date(2018, 12, 5) for c in sujeito))

    def test_criar_contas_ano_inteiro_com_contas_vencidas_deve_criar_12_contas_no_ano_seguinte(self):
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
        sujeito = despesa_model.criar_contas(datetime.date(2018,12,6))
        self.assertEqual(len(sujeito), 12)
        self.assertFalse(any(c.referente == datetime.date(2019, 1, 1) for c in sujeito))
        self.assertTrue(any(c.referente == datetime.date(2019, 1, 5) for c in sujeito))
        self.assertTrue(any(c.referente == datetime.date(2019, 2, 5) for c in sujeito))
        self.assertTrue(any(c.referente == datetime.date(2019, 3, 5) for c in sujeito))
        self.assertTrue(any(c.referente == datetime.date(2019, 4, 5) for c in sujeito))
        self.assertTrue(any(c.referente == datetime.date(2019, 5, 5) for c in sujeito))
        self.assertTrue(any(c.referente == datetime.date(2019, 6, 5) for c in sujeito))
        self.assertTrue(any(c.referente == datetime.date(2019, 7, 5) for c in sujeito))
        self.assertTrue(any(c.referente == datetime.date(2019, 8, 5) for c in sujeito))
        self.assertTrue(any(c.referente == datetime.date(2019, 9, 5) for c in sujeito))
        self.assertTrue(any(c.referente == datetime.date(2019, 10, 5) for c in sujeito))
        self.assertTrue(any(c.referente == datetime.date(2019, 11, 5) for c in sujeito))
        self.assertTrue(any(c.referente == datetime.date(2019, 12, 5) for c in sujeito))

    def test_criar_contas_janeiro_fev_com_contas_sem_vencer_deve_criar_2_contas(self):
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
        despesa['repeticao_anual'] = False
        form = DespesaForm(data=despesa)
        despesa_model = form.save(commit=False)
        sujeito = despesa_model.criar_contas(datetime.date(2018, 2, 5))
        self.assertEqual(len(sujeito), 2)
        self.assertFalse(any(c.referente == datetime.date(2018, 1, 1) for c in sujeito))
        self.assertTrue(any(c.referente == datetime.date(2018, 1, 5) for c in sujeito))
        self.assertTrue(any(c.referente == datetime.date(2018, 2, 5) for c in sujeito))
        self.assertFalse(any(c.referente == datetime.date(2018, 3, 5) for c in sujeito))
        self.assertFalse(any(c.referente == datetime.date(2018, 4, 5) for c in sujeito))
        self.assertFalse(any(c.referente == datetime.date(2018, 5, 5) for c in sujeito))
        self.assertFalse(any(c.referente == datetime.date(2018, 6, 5) for c in sujeito))
        self.assertFalse(any(c.referente == datetime.date(2018, 7, 5) for c in sujeito))
        self.assertFalse(any(c.referente == datetime.date(2018, 8, 5) for c in sujeito))
        self.assertFalse(any(c.referente == datetime.date(2018, 9, 5) for c in sujeito))
        self.assertFalse(any(c.referente == datetime.date(2018, 10, 5) for c in sujeito))
        self.assertFalse(any(c.referente == datetime.date(2018, 11, 5) for c in sujeito))
        self.assertFalse(any(c.referente == datetime.date(2018, 12, 5) for c in sujeito))


    def test_criar_contas_sem_existir_e_logar_deve_dar_erro(self):
        c = Client()
        # c.force_login(user)
        response = c.post(reverse('cadastro_conta', args=[0]),follow=True)
        self.assertTemplateUsed(response, 'login.html')

    def test_criar_contas_sem_logar_deve_dar_erro(self):
        user = User.objects.create_user(username='username', password='password')
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
        form = DespesaForm(data=despesa)
        d = form.save(commit=False)
        d.usuario = user
        d.save()
        c = Client()
        # c.force_login(user)
        response = c.post(reverse('cadastro_conta', args=[d.id]), despesa, follow=True)
        self.assertTemplateUsed(response, 'login.html')

    def test_criar_contas_logado_sem_existir_despesa_deve_dar_erro(self):
        user = User.objects.create_user(username='username', password='password')
        c = Client()
        c.force_login(user)
        response = c.post(reverse('cadastro_conta', args=[0]),  follow=True)
        self.assertContains(response, 'Operaçao nao disponivel')

    def test_criar_contas_logado_sem_existir_despesa_deve_dar_erro(self):
        user = User.objects.create_user(username='username', password='password')
        c = Client()
        c.force_login(user)
        response = c.post(reverse('cadastro_conta', args=[0]),  follow=True)
        self.assertContains(response, 'Operaçao nao disponivel')

    def test_criar_contas_logado_com_despesa_existente_deve_dar_certo(self):
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
        form = DespesaForm(data=despesa)
        d = form.save(commit=False)
        d.usuario = user
        d.save()
        conta = {}
        conta['form-0-valor'] = 100
        conta['form-0-dia_vencimento'] = 5
        conta['form-0-referente'] = datetime.date(2018, 1, 1)
        conta['form-0-paga'] = False
        conta['form-0-observacao'] = 'Teste'
        conta['form-TOTAL_FORMS'] = 1
        conta['form-INITIAL_FORMS'] = 0
        conta['form-MAX_NUM_FORMS'] = ''
        response = c.post(reverse('cadastro_conta', args=[d.id]),conta,  follow=True)
        self.assertTemplateUsed(response, 'contas_cadastradas_sucesso.html')

    def test_criar_contas_logado_com_outro_usuario_com_despesa_existente_deve_dar_erro(self):
        user = User.objects.create_user(username='username', password='password')
        user2 = User.objects.create_user(username='username1', password='password1')
        c = Client()
        c.force_login(user2)
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
        form = DespesaForm(data=despesa)
        d = form.save(commit=False)
        d.usuario = user
        d.save()
        conta = {}
        conta['form-0-valor'] = 100
        conta['form-0-dia_vencimento'] = 5
        conta['form-0-referente'] = datetime.date(2018, 1, 1)
        conta['form-0-paga'] = False
        conta['form-0-observacao'] = 'Teste'
        conta['form-TOTAL_FORMS'] = 1
        conta['form-INITIAL_FORMS'] = 0
        conta['form-MAX_NUM_FORMS'] = ''
        response = c.post(reverse('cadastro_conta', args=[d.id]), conta, follow=True)
        self.assertContains(response, 'Operaçao nao disponivel')

    def test_pagar_conta_sem_logar_deve_dar_erro(self):
        user = User.objects.create_user(username='username', password='password')
        despesa = Despesa()
        despesa.nome = 'Teste'
        despesa.valor = 100
        despesa.dia_vencimento = 5
        despesa.mes_inicio = 1
        despesa.mes_termino = 2
        despesa.cor = 'blue'
        despesa.icone = 'fa-times'
        despesa.categoria = 'teste'
        despesa.periodica = True
        despesa.repeticao_anual = True
        despesa.usuario = user
        despesa.save()
        conta = despesa.criar_conta(datetime.date(2018, 1, 1))
        conta.save()
        c = Client()
        # c.force_login(user)
        response = c.post(reverse('pagar_conta', args=[despesa.id, conta.id]), follow=True)
        self.assertTemplateUsed(response, 'login.html')

    def test_pagar_conta_logado_sem_existir_conta_deve_dar_erro(self):
        user = User.objects.create_user(username='username', password='password')
        c = Client()
        c.force_login(user)
        despesa = Despesa()
        despesa.nome = 'Teste'
        despesa.valor = 100
        despesa.dia_vencimento = 5
        despesa.mes_inicio = 1
        despesa.mes_termino = 2
        despesa.cor = 'blue'
        despesa.icone = 'fa-times'
        despesa.categoria = 'teste'
        despesa.periodica = True
        despesa.repeticao_anual = True
        despesa.usuario = user
        despesa.save()
        response = c.post(reverse('pagar_conta', args=[despesa.id, 0]), follow=True)
        self.assertContains(response, 'Operaçao nao disponivel')

    def test_pagar_conta_logado_sem_existir_despesa_deve_dar_erro(self):
        user = User.objects.create_user(username='username', password='password')
        c = Client()
        c.force_login(user)
        response = c.post(reverse('cadastro_conta', args=[0]),  follow=True)
        self.assertContains(response, 'Operaçao nao disponivel')

    def test_pagar_conta_nao_paga_logado_com_despesa_existente_deve_dar_alterar_status_para_pago(self):
        user = User.objects.create_user(username='username', password='password')
        despesa = Despesa()
        despesa.nome = 'Teste'
        despesa.valor = 100
        despesa.dia_vencimento = 5
        despesa.mes_inicio = 1
        despesa.mes_termino = 2
        despesa.cor = 'blue'
        despesa.icone = 'fa-times'
        despesa.categoria = 'teste'
        despesa.periodica = True
        despesa.repeticao_anual = True
        despesa.usuario = user
        despesa.save()
        conta = despesa.criar_conta(datetime.date(2018, 1, 1))
        conta.save()
        c = Client()
        c.force_login(user)
        response = c.post(reverse('pagar_conta', args=[despesa.id, conta.id]), follow=True)
        self.assertTrue(Conta.objects.get(id=conta.id).paga)

    def test_pagar_conta_paga_logado_com_despesa_existente_deve_dar_alterar_status_para_nao_pago(self):
        user = User.objects.create_user(username='username', password='password')
        despesa = Despesa()
        despesa.nome = 'Teste'
        despesa.valor = 100
        despesa.dia_vencimento = 5
        despesa.mes_inicio = 1
        despesa.mes_termino = 2
        despesa.cor = 'blue'
        despesa.icone = 'fa-times'
        despesa.categoria = 'teste'
        despesa.periodica = True
        despesa.repeticao_anual = True
        despesa.usuario = user
        despesa.save()
        conta = despesa.criar_conta(datetime.date(2018, 1, 1))
        conta.paga = True
        conta.save()
        c = Client()
        c.force_login(user)
        response = c.post(reverse('pagar_conta', args=[despesa.id, conta.id]), follow=True)
        self.assertFalse(Conta.objects.get(id=conta.id).paga)

class ContaFormTest(TestCase):
    def test_conta_sem_valor_deve_ser_invalido(self):
        conta = {}
        # conta['valor'] = 100
        conta['dia_vencimento'] = 5
        conta['referente'] = datetime.date(2018, 1, 1)
        conta['paga'] = False
        conta['observacao'] = 'Teste'
        contaForm = ContaForm(data=conta)
        self.assertFalse(contaForm.is_valid())
        self.assertEqual(len(contaForm.errors), 1)
        self.assertIsNotNone(contaForm.errors.get('valor', None))


    def test_conta_sem_dia_vencimento_deve_ser_invalido(self):
        conta = {}
        conta['valor'] = 100
        # conta['dia_vencimento'] = 5
        conta['referente'] = datetime.date(2018, 1, 1)
        conta['paga'] = False
        conta['observacao'] = 'Teste'
        contaForm = ContaForm(data=conta)
        self.assertFalse(contaForm.is_valid())
        self.assertEqual(len(contaForm.errors), 1)
        self.assertIsNotNone(contaForm.errors.get('dia_vencimento', None))

    def test_conta_sem_referente_deve_ser_invalido(self):
        conta = {}
        conta['valor'] = 100
        conta['dia_vencimento'] = 5
        # conta['referente'] = datetime.date(2018, 1, 1)
        conta['paga'] = False
        conta['observacao'] = 'Teste'
        contaForm = ContaForm(data=conta)
        self.assertFalse(contaForm.is_valid())
        self.assertEqual(len(contaForm.errors), 1)
        self.assertIsNotNone(contaForm.errors.get('referente', None))


    def test_conta_sem_pagamento_e_sem_data_deve_ser_valido(self):
        conta = {}
        conta['valor'] = 100
        conta['dia_vencimento'] = 5
        conta['referente'] = datetime.date(2018, 1, 1)
        conta['paga'] = False
        conta['observacao'] = 'Teste'
        contaForm = ContaForm(data=conta)
        self.assertTrue(contaForm.is_valid())

    def test_conta_com_pagamento_e_sem_data_deve_ser_invalido(self):
        conta = {}
        conta['valor'] = 100
        conta['dia_vencimento'] = 5
        conta['referente'] = datetime.date(2018, 1, 1)
        conta['paga'] = True
        conta['observacao'] = 'Teste'
        contaForm = ContaForm(data=conta)
        self.assertFalse(contaForm.is_valid())
        self.assertEqual(len(contaForm.errors), 1)
        self.assertIsNotNone(contaForm.errors.get('data_pagamento', None))

    def test_conta_com_pagamento_e_com_data_ser_valido(self):
        conta = {}
        conta['valor'] = 100
        conta['dia_vencimento'] = 5
        conta['referente'] = datetime.date(2018, 1, 1)
        conta['paga'] = True
        conta['data_pagamento'] = datetime.date(2018, 1, 1)
        conta['observacao'] = 'Teste'
        contaForm = ContaForm(data=conta)
        self.assertTrue(contaForm.is_valid())

    def test_conta_sem_pagamento_e_com_data_ser_invalido(self):
        conta = {}
        conta['valor'] = 100
        conta['dia_vencimento'] = 5
        conta['referente'] = datetime.date(2018, 1, 1)
        conta['paga'] = False
        conta['data_pagamento'] = datetime.date(2018, 1, 1)
        conta['observacao'] = 'Teste'
        contaForm = ContaForm(data=conta)
        self.assertFalse(contaForm.is_valid())
        self.assertEqual(len(contaForm.errors), 1)
        self.assertIsNotNone(contaForm.errors.get('data_pagamento', None))

    def test_conta_sem_observacao_deve_ser_valida(self):
        conta = {}
        conta['valor'] = 100
        conta['dia_vencimento'] = 5
        conta['referente'] = datetime.date(2018, 1, 1)
        conta['paga'] = False
        # conta['observacao'] = 'Teste'
        contaForm = ContaForm(data=conta)
        self.assertTrue(contaForm.is_valid())

    def test_conta_com_observacao_deve_ser_valida(self):
        conta = {}
        conta['valor'] = 100
        conta['dia_vencimento'] = 5
        conta['referente'] = datetime.date(2018, 1, 1)
        conta['paga'] = False
        conta['observacao'] = 'Teste'
        contaForm = ContaForm(data=conta)
        self.assertTrue(contaForm.is_valid())

class ListarContas(TestCase):
    def test_contas_cadastradas_sucesso_deve_listar_todas_contas_daquela_despesa(self):
        user = User.objects.create_user(username='username', password='password')
        despesa = Despesa()
        despesa.nome = 'Teste'
        despesa.valor = 100
        despesa.dia_vencimento = 5
        despesa.mes_inicio = 1
        despesa.mes_termino = 12
        despesa.cor = 'blue'
        despesa.icone = 'fa-times'
        despesa.categoria = 'teste'
        despesa.periodica = True
        despesa.repeticao_anual = True
        despesa.usuario = user
        despesa.save()
        contas = despesa.criar_contas(datetime.date(2018, 1, 1))
        for conta in contas:
            conta.save()
        c = Client()
        c.force_login(user)
        response = c.get(reverse('contas_cadastradas_sucesso', args=[despesa.id]), follow=True)
        self.assertEqual(len(response.context['contas']), 12)

    def test_contas_cadastradas_sucesso_deve_sem_logar_deve_redirecionar_para_login(self):
        user = User.objects.create_user(username='username', password='password')
        despesa = Despesa()
        despesa.nome = 'Teste'
        despesa.valor = 100
        despesa.dia_vencimento = 5
        despesa.mes_inicio = 1
        despesa.mes_termino = 12
        despesa.cor = 'blue'
        despesa.icone = 'fa-times'
        despesa.categoria = 'teste'
        despesa.periodica = True
        despesa.repeticao_anual = True
        despesa.usuario = user
        despesa.save()
        contas = despesa.criar_contas(datetime.date(2018, 1, 1))
        for conta in contas:
            conta.save()
        c = Client()
        # c.force_login(user)
        response = c.get(reverse('contas_cadastradas_sucesso', args=[despesa.id]), follow=True)
        self.assertTemplateUsed(response, 'login.html')

    def test_contas_cadastradas_sucesso_de_outro_usuario_deve_dar_erro(self):
        user = User.objects.create_user(username='username', password='password')
        user2 = User.objects.create_user(username='username2', password='password2')
        despesa = Despesa()
        despesa.nome = 'Teste'
        despesa.valor = 100
        despesa.dia_vencimento = 5
        despesa.mes_inicio = 1
        despesa.mes_termino = 12
        despesa.cor = 'blue'
        despesa.icone = 'fa-times'
        despesa.categoria = 'teste'
        despesa.periodica = True
        despesa.repeticao_anual = True
        despesa.usuario = user
        despesa.save()
        contas = despesa.criar_contas(datetime.date(2018, 1, 1))
        for conta in contas:
            conta.save()
        c = Client()
        c.force_login(user2)
        response = c.get(reverse('contas_cadastradas_sucesso', args=[despesa.id]), follow=True)
        self.assertContains(response, 'Operaçao nao disponivel')


    @freeze_time("2018-01-05")
    def test_listar_contas_deve_listar_todas_contas(self):
        user = User.objects.create_user(username='username', password='password')
        despesa = Despesa()
        despesa.nome = 'Teste'
        despesa.valor = 100
        despesa.dia_vencimento = 5
        despesa.mes_inicio = 1
        despesa.mes_termino = 3
        despesa.cor = 'blue'
        despesa.icone = 'fa-times'
        despesa.categoria = 'teste'
        despesa.periodica = True
        despesa.repeticao_anual = True
        despesa.usuario = user
        despesa.save()
        contas = despesa.criar_contas(datetime.date(2018, 1, 1))
        for conta in contas:
            conta.save()
        despesa1 = Despesa()
        despesa1.nome = 'Teste'
        despesa1.valor = 100
        despesa1.dia_vencimento = 5
        despesa1.mes_inicio = 1
        despesa1.mes_termino = 3
        despesa1.cor = 'blue'
        despesa1.icone = 'fa-times'
        despesa1.categoria = 'teste'
        despesa1.periodica = True
        despesa1.repeticao_anual = True
        despesa1.usuario = user
        despesa1.save()
        contas2 = despesa.criar_contas(datetime.date(2018, 1, 1))
        for conta in contas2:
            conta.save()
        c = Client()
        c.force_login(user)
        response = c.post(reverse('index'))
        self.assertEqual(len(response.context['contas']), 2)
        self.assertEqual(len(response.context['proximas_contas']), 4)


    def test_listar_contas_depesa_deve_sem_logar_deve_redirecionar_para_login(self):
        user = User.objects.create_user(username='username', password='password')
        despesa = Despesa()
        despesa.nome = 'Teste'
        despesa.valor = 100
        despesa.dia_vencimento = 5
        despesa.mes_inicio = 1
        despesa.mes_termino = 12
        despesa.cor = 'blue'
        despesa.icone = 'fa-times'
        despesa.categoria = 'teste'
        despesa.periodica = True
        despesa.repeticao_anual = True
        despesa.usuario = user
        despesa.save()
        contas = despesa.criar_contas(datetime.date(2018, 1, 1))
        for conta in contas:
            conta.save()
        c = Client()
        # c.force_login(user)
        response = c.get(reverse('listar_contas_depesa', args=[despesa.id]), follow=True)
        self.assertTemplateUsed(response, 'login.html')


    def test_contas_cadastradas_sucesso_deve_listar_todas_contas_daquela_despesa(self):
        user = User.objects.create_user(username='username', password='password')
        despesa = Despesa()
        despesa.nome = 'Teste'
        despesa.valor = 100
        despesa.dia_vencimento = 5
        despesa.mes_inicio = 1
        despesa.mes_termino = 12
        despesa.cor = 'blue'
        despesa.icone = 'fa-times'
        despesa.categoria = 'teste'
        despesa.periodica = True
        despesa.repeticao_anual = True
        despesa.usuario = user
        despesa.save()
        contas = despesa.criar_contas(datetime.date(2018, 1, 1))
        for conta in contas:
            conta.save()
        c = Client()
        c.force_login(user)
        response = c.get(reverse('contas_cadastradas_sucesso', args=[despesa.id]), follow=True)
        self.assertEqual(len(response.context['contas']), 12)

    def test_contas_cadastradas_sucesso_deve_sem_logar_deve_redirecionar_para_login(self):
        user = User.objects.create_user(username='username', password='password')
        despesa = Despesa()
        despesa.nome = 'Teste'
        despesa.valor = 100
        despesa.dia_vencimento = 5
        despesa.mes_inicio = 1
        despesa.mes_termino = 12
        despesa.cor = 'blue'
        despesa.icone = 'fa-times'
        despesa.categoria = 'teste'
        despesa.periodica = True
        despesa.repeticao_anual = True
        despesa.usuario = user
        despesa.save()
        contas = despesa.criar_contas(datetime.date(2018, 1, 1))
        for conta in contas:
            conta.save()
        c = Client()
        # c.force_login(user)
        response = c.get(reverse('listar_contas_depesa', args=[despesa.id]), follow=True)
        self.assertTemplateUsed(response, 'login.html')

    def test_contas_cadastradas_sucesso_de_outro_usuario_deve_dar_erro(self):
        user = User.objects.create_user(username='username', password='password')
        user2 = User.objects.create_user(username='username2', password='password2')
        despesa = Despesa()
        despesa.nome = 'Teste'
        despesa.valor = 100
        despesa.dia_vencimento = 5
        despesa.mes_inicio = 1
        despesa.mes_termino = 12
        despesa.cor = 'blue'
        despesa.icone = 'fa-times'
        despesa.categoria = 'teste'
        despesa.periodica = True
        despesa.repeticao_anual = True
        despesa.usuario = user
        despesa.save()
        contas = despesa.criar_contas(datetime.date(2018, 1, 1))
        for conta in contas:
            conta.save()
        c = Client()
        c.force_login(user2)
        response = c.get(reverse('listar_contas_depesa', args=[despesa.id]), follow=True)
        self.assertTemplateUsed(response, 'lista_contas_despesa.html')
        self.assertEqual(len(response.context.get('contas', 0)), 0)

