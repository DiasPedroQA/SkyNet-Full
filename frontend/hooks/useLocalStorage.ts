// frontend/hooks/useLocalStorage.ts
import { useState, useEffect } from 'react';

export function useLocalStorage<T>(key: string, initialValue: T): [T, (value: T) => void] {
  // Função para ler do localStorage
  const readValue: () => T = (): T => {
    try {
      const item: string | null = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.warn(`Erro ao ler localStorage key "${key}":`, error);
      return initialValue;
    }
  };

  const [storedValue, setStoredValue] = useState<T>(readValue);

  // Função para atualizar localStorage e estado
  const setValue: (value: T) => void = (value: T) => {
    try {
      // Salva no localStorage
      window.localStorage.setItem(key, JSON.stringify(value));
      // Atualiza estado
      setStoredValue(value);
      // Dispara evento para outros componentes
      window.dispatchEvent(new Event('local-storage-change'));
    } catch (error) {
      console.warn(`Erro ao salvar localStorage key "${key}":`, error);
    }
  };

  // Sincroniza entre abas
  useEffect(() => {
    const handleStorageChange: () => void = () => {
      setStoredValue(readValue());
    };

    window.addEventListener('storage', handleStorageChange);
    window.addEventListener('local-storage-change', handleStorageChange);

    return () => {
      window.removeEventListener('storage', handleStorageChange);
      window.removeEventListener('local-storage-change', handleStorageChange);
    };
  }, []);

  return [storedValue, setValue];
}
