# Dicas de Performance para Hardware Limitado

## Otimizações do Sistema
- Desative serviços não essenciais
- Use um ambiente Linux leve (ex: Lubuntu, Xubuntu)
- Mantenha o sistema atualizado apenas com pacotes necessários

## Desenvolvimento
- Use editores de texto leves (VS Code com extensões mínimas, Sublime, Vim)
- Trabalhe com branches pequenos no git
- Evite IDEs pesadas quando possível

## Python
- Prefira `uv` sobre `pip` para gestão de pacotes
- Mantenha ambientes virtuais separados por projeto
- Use `python -OO` para otimizar bytecode
- Considere pypy para scripts CPU-intensivos

## Testes
- Execute testes em grupos menores
- Use `pytest -k` para rodar testes específicos
- Aproveite `pytest-xdist` para paralelismo quando possível