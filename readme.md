## Labore Scrap ##

Separado em 3 arquivos

 - labore_scrap: utilizado para pegar links e nomes de todos os membros do grupo, gera um csv
 - labore_extractor: utilizado para extrair dados de cada membro do grupo, gera um json
 - aux_var: definir diretorio do driver do selenium (geckodriver - firefox), localizacao e nome do arquivo csv gerado no script 'labore_scrap', localizacao e nome do arquivo json gerado no script 'labore_extractor'


  Necessario Firefox e o driver do selenium [https://github.com/mozilla/geckodriver/releases](https://github.com/mozilla/geckodriver/releases)

  OBS:
    - 'labore_scrap' poderia apenas abrir a pagina toda (clicar nos botoes), salvar o HTML para depois ser tratado por um terceiro script que gera o JSON que esta sendo gerado nesse, isso ajudara a implementar restart em caso de erro


    - Formato do json exportado:

    ```{js}
      [{
        id: uri do usuario
        content {
          experience: [{
            tittle: "\n      TTC do Brasil\n        Full-time\n",
            date_range: "Oct 2019 – Present",
            description: "- Definição de Perfil de cliente;- Criação de Cold mails;- Captação de Leads via Outbound Marketing;- Contato com o cliente;- Pré-venda (Capitação, ligação, agendamento de reunião)\n\n",
            duration: "6 mos",
            location: "Rio de Janeiro e Região, Brasil"
          },...],
          totalConnections: "\n\n                  110 connections\n                \n",
          education: [{
            date_range: "Nov 2016 – Present",
            course: "Gestão de Marketing",
            degree: "Marketing",
            shcool: "Universidade Estácio de Sá",
            description: "\n  Cursando 3º período de Marketing\n\n"
          },...],
          name: "Nome do usuario",
          about: null,
          ocupation: "\n            Outbound Marketing & sales \n          ",
          localization: "\n              São João de Meriti, Rio de Janeiro, Brazil\n            "
        }
        ...
        }]
    ```
