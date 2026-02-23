import { defineConfig } from 'cypress';

export default defineConfig({
  e2e: {
    baseUrl: 'http://localhost:3000', // URL do frontend
    setupNodeEvents(on, config) {
      // implement node event listeners here
    },
  },
});

// Teste de exemplo
describe('E2E Testes', () => {
  it('Visita a página inicial e verifica o título', () => {
    cy.visit('/');
    cy.title().should('include', 'Título da Página'); // Substitua pelo título real da sua página
  });

  it('Verifica a lista de favoritos', () => {
    cy.visit('/dashboard'); // Acesse a página do dashboard
    cy.get('.favorite-list') // Seletor para a lista de favoritos
      .should('exist')
      .and('be.visible');
  });
});