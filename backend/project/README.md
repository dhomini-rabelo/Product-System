# Teste Dev

Esse teste visa avaliar o conhecimento sobre os recursos disponíveis no framework Django entre outras tecnologias voltadas para desenvolvimento web. Por isso, utilize o máximo de recursos presentes deste framework.

## Sistema de cadastro de produtos e fornecedores


Crie uma aplicação para cadastro de produtos, onde o mesmo deverá conter uma **categoria** e poderá ter vários **fornecedores**. Em cada fornecedor o preço de cada produto poderá variar. Sendo assim, junto com a informação de qual fornecedor oferece determinado produto, precisamos também saber o preço do mesmo com este fornecedor.

Tenha cuidado de não permitir que nenhum nome de **categoria** ou **produto** seja duplicado nesta aplicação. Da mesma forma, não queremos CNPJ incompletos ou inválidos sendo cadastrados na base de dados. 

Precisamos que os dados sejam retornados em *endpoints* específicos para cada uma das entidades citadas. O retorno deve ser em JSON. 

Lembre-se de manter um padrão, para que os dados sejam facilmente consumidos em qualquer aplicação.


**NOTA**: Esteja livre para usar quaisquer recursos do Django, bem como instalar bibliotecas para auxiliar na criação da sua aplicação.

### Seu objetivo


- Criar endpoints para CRUD de **produtos**. O produto deve conter nome, data de cadastro, data de atualização e descrição. O `nome` do **produto** deve ser único e não pode ultrapassar 200 caracteres, porém a `descrição` é opcional e deve permitir inserir um texto longo.

- Um **produto** sempre deverá ter uma **categoria**.


- Um **produto** deverá ter vários **fornecedores**. E em cada **fornecedor**, deverá ser informado o preço de custo do produto com este fornecedor. Da mesma forma, o **fornecedor** poderá conter vários **produtos**.

- Criar endpoints para CRUD de **categorias**. A categoria deve conter nome, data de cadastro e data de atualização. O nome da categoria deve ser única.

- Criar endpoins para CRUD de **fornecedores**, com Nome Fantasia, Razão Social, Endereço, CNPJ e Telefones para contato. A forma de organização do endereço e telefones fica a seu critério em relação a estrutura de dados (tabelas adicionais ou campos separados). Porém, os mesmos precisam sempre ser retornados junto com os dados fornecedor.


- Quando houver algum erro na validação dos dados, isso precisa ser informado no endpoint em que ocorreu.


**NOTA**: Ao finalizar o teste manda para o github e nos encaminha o link.