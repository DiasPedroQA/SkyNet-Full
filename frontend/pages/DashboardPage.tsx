// frontend/pages/DashboardPage.tsx
import React from 'react';
import { useAuth } from '../hooks/useAuth';
import { useFiles } from '../hooks/useFiles';
import FileCard from '../components/FileCard';
import Button from '../components/Button';

const DashboardPage: React.FC = () => {
  const { user, logout } = useAuth();
  const { files, loading, error, uploadFile, deleteFile } = useFiles();

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file: File | undefined = e.target.files?.[0];
    if (file) {
      try {
        await uploadFile(file);
        e.target.value = ''; // Limpa o input
      } catch (err) {
        console.error('Erro no upload:', err);
      }
    }
  };

  const handleDownload: (fileId: number) => Promise<void> = async (fileId: number) => {
    // Implementar download
    console.log('Download file:', fileId);
  };

  const handleDelete: (fileId: number) => Promise<void> = async (fileId: number) => {
    if (window.confirm('Tem certeza que deseja deletar este arquivo?')) {
      try {
        await deleteFile(fileId);
      } catch (err) {
        console.error('Erro ao deletar:', err);
      }
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-semibold">File Manager</h1>
            </div>

            <div className="flex items-center space-x-4">
              <span className="text-gray-700">
                Olá, {user?.username}
              </span>
              <Button
                size="small"
                variant="secondary"
                onClick={logout}
              >
                Sair
              </Button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          {/* Área de upload */}
          <div className="mb-8 p-6 bg-white rounded-lg shadow">
            <h2 className="text-lg font-medium mb-4">Upload de Arquivo</h2>

            <div className="flex items-center space-x-4">
              <input
                type="file"
                onChange={handleFileUpload}
                className="block w-full text-sm text-gray-500
                  file:mr-4 file:py-2 file:px-4
                  file:rounded-md file:border-0
                  file:text-sm file:font-semibold
                  file:bg-blue-50 file:text-blue-700
                  hover:file:bg-blue-100"
              />
            </div>
          </div>

          {/* Lista de arquivos */}
          <div>
            <h2 className="text-lg font-medium mb-4">Meus Arquivos</h2>

            {loading && (
              <div className="text-center py-8">
                <div className="inline-block animate-spin rounded-full h-8 w-8 border-4 border-blue-500 border-t-transparent"></div>
                <p className="mt-2 text-gray-600">Carregando arquivos...</p>
              </div>
            )}

            {error && (
              <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
                {error}
              </div>
            )}

            {!loading && !error && files.length === 0 && (
              <div className="text-center py-12 bg-white rounded-lg shadow">
                <p className="text-gray-500">Nenhum arquivo encontrado</p>
                <p className="text-sm text-gray-400 mt-2">
                  Faça upload do seu primeiro arquivo!
                </p>
              </div>
            )}

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {files.map((file) => (
                <FileCard
                  key={file.id}
                  file={file}
                  onDownload={handleDownload}
                  onDelete={handleDelete}
                />
              ))}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default DashboardPage;
