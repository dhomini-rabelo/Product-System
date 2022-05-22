<h1>Sistema de produtos</h1>
<p>API para gerenciar sistema de produtos</p>

<br>
<h2>🔗 Tópicos</h2>
<ul>
<li><a href="#tools">Ferramentas</a></li>
<li><a href="#db">Banco de dados</a></li>
<li><a href="#doc">Documentação</a></li>
<ul>
    <li><a href="#organization">Organização</a></li>
    <li><a href="#serializers">Serializers</a></li>
    <li><a href="#routes">Rotas</a></li>
</ul>
<li><a href="#use">Como usar na sua máquina</a></li>
</ul>

<br>
<h2 id="tools">🛠️ Ferramentas</h2>

<ul>
<li><a href="https://docs.djangoproject.com/en/4.0/">Django</a></li>
<li><a href="https://www.django-rest-framework.org/">Django Rest Framework</a></li>
<li><a href="https://github.com/dhomini-rabelo/Fast">Fast</a></li>
<li><a href="https://github.com/dhomini-rabelo/Rest-Full-Control">Rest-Full-Control</a></li>
</ul>

<br>
<h2 id="db">🏷️ Modelagem do banco de dados</h2>

<br>
<h2 id="doc">📖 Documentação</h2>
<br>
<h3 id="organization">Organização</h2>

<ul>
<li>
Os padrões principais do projeto estão na pasta project/Core
</li>
<li>
Os apps estão na pasta project/backend
</li>
<li>
PRODUCTS é onde está a configuração do projeto
</li>
</ul>
<br>
<h3 id="serializers">Serializers</h3>
<br>
<h3 id="routes">Rotas</h3>

<br>
<br>
<h2 id="use">🚀 Como usar na sua máquina</h2>

<h3>Depois de clonar o projeto basta apenas seguir os comandos abaixo.</h3>
<br>

```
cd backend
python -m venv venv
venv/Scripts/Activate.ps1 # if use PowerShell
pip install -r requirements.txt
pip freeze > requirements.txt
cd project
python manage.py runserver
```