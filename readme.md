## Labore Scrap ##

Separado em 3 arquivos

 - labore_scrap: utilizado para pegar links e nomes de todos os membros do grupo, gera um csv
 - labore_extractor: utilizado para extrair dados de cada membro do grupo, gera um json
 - aux_var: definir diretorio do driver do selenium (geckodriver - firefox), localizacao e nome do arquivo csv gerado no script 'labore_scrap', localizacao e nome do arquivo json gerado no script 'labore_extractor'


  Necessario Firefox e o driver do selenium [https://github.com/mozilla/geckodriver/releases](https://github.com/mozilla/geckodriver/releases)

  OBS:
    - 'labore_scrap' poderia apenas abrir a pagina toda (clicar nos botoes), salvar o HTML para depois ser tratado por um terceiro script que gera o JSON que esta sendo gerado nesse, isso ajudara a implementar restart em caso de erro
