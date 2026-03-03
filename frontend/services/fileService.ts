// frontend/services/fileService.ts
import { apiService } from './api';
import { File } from '../types/file.types';

class FileService {
  async uploadFile(file: File, onProgress?: (progress: number) => void): Promise<File> {
    return await apiService.uploadFile('/files/upload', file, onProgress);
  }

  async getUserFiles(): Promise<File[]> {
    return await apiService.get<File[]>('/files/my-files');
  }

  async deleteFile(fileId: number): Promise<void> {
    await apiService.post(`/files/${fileId}/delete`, {});
  }

  async downloadFile(fileId: number): Promise<Blob> {
    // Implementar download
    const response = await fetch(`/api/files/${fileId}/download`);
    return await response.blob();
  }
}

export const fileService = new FileService();
