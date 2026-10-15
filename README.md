# Plugins Claude — Grupo IVM

Marketplace privado de plugins para o app Claude, com recortes **revisados** de projetos open source.

| Plugin | Origem | Conteúdo |
|---|---|---|
| `oh-my-claudecode` | [Yeachan-Heo/oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode) (MIT) | 12 skills de método + 19 agentes. Sem hooks, CLI `omc` ou MCP. |
| `supabase` | [supabase/agent-skills](https://github.com/supabase/agent-skills) (MIT) | Guia Supabase + 31 regras de Postgres |
| `vercel` | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) (MIT) | 9 skills (React/Next.js, deploy, otimização, design) |
| `rea` | [morluto/rea](https://github.com/morluto/rea) (MIT) | Skill `reverse-engineer-anything` + servidor MCP `rea-agents@6.5.0` (fixado na tag). Binários, Electron/JS, APK, .NET, firmware, PCAP/HAR. |

O Chrome DevTools fica fora daqui: usa o marketplace oficial `ChromeDevTools/chrome-devtools-mcp`.

## Instalar no app

**Plugins → + Adicionar → Adicionar marketplace** → `VoIPMundoTelecom/claude-plugins`, com sincronização automática ligada.

## Como as atualizações chegam

1. Toda segunda, a Action **Sincronizar upstreams** puxa os repositórios originais e recorta de novo.
2. Se algo mudou, abre (ou atualiza) um PR `sync/upstream` com a varredura de segurança no corpo.
3. **Nada chega ao app sem você aprovar o merge.** Depois do merge, o app sincroniza sozinho.

Para rodar na hora: aba **Actions → Sincronizar upstreams → Run workflow**.

## Revisando um PR

- **Padrões de risco** (pipe para shell, `rm -rf`, `eval`, caminhos de credenciais, injeção de prompt): investigar qualquer ⚠️ novo.
- **⚙️ Código executável**: hoje só `deploy-to-vercel` e `vercel-optimize`. Arquivo novo nessa lista merece leitura.
- **🔌 Servidores MCP**: hoje só `rea` (`npx -y rea-agents@6.5.0 mcp`). A versão é fixada em `sources.json` (`ref` + `mcp_servers`); subir de versão é mudança deliberada, nunca automática. Servidor novo ou versão `@latest` = não aprovar.
- **🌐 Endpoints**: `deploy-to-vercel` envia o projeto para o endpoint de deploy "claimable" da Vercel. Endpoint novo, desconhecido ou fora dos domínios do fornecedor = não aprovar.

## Mudar o que entra

Edite `sources.json` (lista de skills por plugin) e rode:

```bash
python3 -I scripts/sync.py --repo-root .
python3 -I scripts/validate.py .
```

O script só copia `.md`, `.json`, `.txt` e código-fonte em texto; binários e arquivos compactados são descartados e listados na varredura.

## REA (engenharia reversa)

- O plugin registra o servidor MCP `rea`, que roda **na máquina de quem instala** via `npx`. Precisa de Node.js 22.19+/24.11+.
- Análise de JavaScript/Electron, pacotes, APK e capturas não exige motor extra. Análise nativa (Mach-O/PE/ELF) usa Ghidra, Hopper ou IDA já instalados; `npx -y rea-agents@6.5.0 doctor --client claude_code --json` mostra o que falta.
- Não é sandbox: analisar binário suspeito roda o parser do motor com as permissões do usuário. Amostras desconhecidas vão para VM.
- Frida e o hook do Electron injetam código em processos vivos: só em software nosso ou com autorização. Ver [DISCLAIMER](https://github.com/morluto/rea/blob/main/DISCLAIMER.md).
