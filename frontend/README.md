# React + TypeScript + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) (or [oxc](https://oxc.rs) when used in [rolldown-vite](https://vite.dev/guide/rolldown)) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type-aware lint rules:

```js
export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...

      // Remove tseslint.configs.recommended and replace with this
      tseslint.configs.recommendedTypeChecked,
      // Alternatively, use this for stricter rules
      tseslint.configs.strictTypeChecked,
      // Optionally, add this for stylistic rules
      tseslint.configs.stylisticTypeChecked,

      // Other configs...
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
```

You can also install [eslint-plugin-react-x](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-x) and [eslint-plugin-react-dom](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-dom) for React-specific lint rules:

```js
// eslint.config.js
import reactX from 'eslint-plugin-react-x'
import reactDom from 'eslint-plugin-react-dom'

export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...
      // Enable lint rules for React
      reactX.configs['recommended-typescript'],
      // Enable lint rules for React DOM
      reactDom.configs.recommended,
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
```

# Frontend Documentation for SkyNet

Este diretório contém a aplicação frontend do projeto SkyNet, que é construída utilizando React e TypeScript. Abaixo estão as informações sobre a estrutura do projeto e como configurar e executar a aplicação.

## Estrutura do Projeto

```
frontend
├── src
│   ├── index.tsx                # Ponto de entrada da aplicação React
│   ├── app
│   │   ├── components            # Componentes reutilizáveis da aplicação
│   │   │   └── FavoriteList.tsx  # Componente que exibe a lista de favoritos
│   │   ├── pages                 # Páginas da aplicação
│   │   │   └── Dashboard.tsx     # Página principal do aplicativo
│   │   └── services              # Serviços para interagir com a API
│   │       └── api.ts            # Funções para chamadas à API do backend
│   └── tests                     # Testes da aplicação
│       └── App.test.tsx         # Testes para o aplicativo frontend
├── public
│   └── index.html                # HTML principal que carrega a aplicação React
├── package.json                  # Configuração do npm, incluindo dependências e scripts
├── tsconfig.json                 # Configuração do TypeScript
├── jest.config.js                # Configuração do Jest para testes
├── cypress
│   └── integration
│       └── e2e_spec.ts           # Testes de ponta a ponta utilizando Cypress
└── README.md                     # Documentação do frontend
```

## Configuração do Ambiente

1. **Instalação de Dependências**: Navegue até o diretório `frontend` e execute o seguinte comando para instalar as dependências:

   ```
   npm install
   ```

2. **Executar a Aplicação**: Após a instalação das dependências, você pode iniciar a aplicação com o comando:

   ```
   npm start
   ```

   A aplicação estará disponível em `http://localhost:3000`.

## Testes

Para executar os testes, utilize o comando:

```
npm test
```

Isso executará os testes unitários e de integração definidos na pasta `tests`.

## Contribuição

Sinta-se à vontade para contribuir com melhorias ou correções. Para isso, crie um fork do repositório, faça suas alterações e envie um pull request.

## Licença

Este projeto está licenciado sob a MIT License. Veja o arquivo LICENSE para mais detalhes.
