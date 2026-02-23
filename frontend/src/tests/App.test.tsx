import React from 'react';
import { render, screen } from '@testing-library/react';
import App from '../app/App';

describe('App Component', () => {
  test('renders the dashboard', () => {
    render(<App />);
    const linkElement = screen.getByText(/Dashboard/i);
    expect(linkElement).toBeInTheDocument();
  });

  test('renders the favorite list', () => {
    render(<App />);
    const listElement = screen.getByText(/Favorite List/i);
    expect(listElement).toBeInTheDocument();
  });
});