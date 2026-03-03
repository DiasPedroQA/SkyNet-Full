// frontend/pages/LoginPage.tsx
/**
 * PAGES: Páginas completas da aplicação
 * Combinam múltiplos componentes
 * Contêm a lógica específica da página
 */

import React, { ChangeEvent, FormEvent, useState } from 'react';
import { NavigateFunction, useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import Button from '../components/Button';
import Input from '../components/Input';

const LoginPage: React.FC = () => {
  const navigate: NavigateFunction = useNavigate();
  const { login, loading, error } = useAuth();

  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });

  const handleChange: (e: ChangeEvent<HTMLInputElement>) => Promise<void> = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit: (e: FormEvent<Element>) => Promise<void> = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      await login(formData);
      navigate('/dashboard');
    } catch (err) {
      // Erro já está no estado do hook
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Entrar no Sistema
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Ou{' '}
            <a href="/register" className="font-medium text-blue-600 hover:text-blue-500">
              crie uma conta gratuita
            </a>
          </p>
        </div>

        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div className="rounded-md shadow-sm space-y-4">
            <Input
              label="Email"
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              error={error ? ' ' : undefined}
            />

            <Input
              label="Senha"
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
              error={error ? ' ' : undefined}
            />
          </div>

          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
              {error}
            </div>
          )}

          <div>
            <Button
              type="submit"
              fullWidth
              loading={loading}
            >
              Entrar
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default LoginPage;
