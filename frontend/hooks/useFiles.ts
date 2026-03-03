// frontend/hooks/useFiles.ts
import { useState, useEffect, useCallback } from 'react';
import { fileService } from '../services/fileService';
import { File } from '../types/file.types';

export const useFiles: () => {files: File[]; loading: boolean; error: string|null; uploadProgress: number; uploadFile: (file: File) => Promise<File>; deleteFile: (fileId: number) => Promise<void>; refreshFiles: () => Promise<void>} = () => {
  const [files, setFiles] = useState<File[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [uploadProgress, setUploadProgress] = useState<number>(0);
  const [error, setError] = useState<string | null>(null);

  const loadFiles: () => Promise<void> = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const userFiles: File[] = await fileService.getUserFiles();
      setFiles(userFiles);
    } catch (err: any) {
      setError('Erro ao carregar arquivos');
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadFiles();
  }, [loadFiles]);

  const uploadFile: (file: File) => Promise<File> = useCallback(async (file: File) => {
    setError(null);
    setUploadProgress(0);

    try {
      const uploadedFile: File = await fileService.uploadFile(
        file,
        (progress) => setUploadProgress(progress)
      );

      setFiles(prev => [uploadedFile, ...prev]);
      setUploadProgress(0);
      return uploadedFile;
    } catch (err: any) {
      setError('Erro ao fazer upload');
      throw err;
    }
  }, []);

  const deleteFile: (fileId: number) => Promise<void> = useCallback(async (fileId: number) => {
    try {
      await fileService.deleteFile(fileId);
      setFiles(prev => prev.filter(f => f.id !== fileId));
    } catch (err: any) {
      setError('Erro ao deletar arquivo');
      throw err;
    }
  }, []);

  return {
    files,
    loading,
    error,
    uploadProgress,
    uploadFile,
    deleteFile,
    refreshFiles: loadFiles
  };
};
